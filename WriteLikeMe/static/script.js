document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d');
    const letterInput = document.getElementById('letterInput');
    const saveButton = document.getElementById('saveLetter');
    const clearButton = document.getElementById('clearCanvas');
    const generateButton = document.getElementById('generateText');
    const textInput = document.getElementById('textInput');
    const previewContainer = document.getElementById('previewContainer');
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const brushSizeInput = document.getElementById('brushSize');
    const brushPreview = document.getElementById('brushPreview');
    const brushSizeValue = document.getElementById('brushSizeValue');
    const lettersGrid = document.getElementById('lettersGrid');

    // Load saved brush size from localStorage
    const savedBrushSize = localStorage.getItem('brushSize');
    if (savedBrushSize) {
        brushSizeInput.value = savedBrushSize;
        updateBrushPreview(savedBrushSize);
    }

    // Set canvas size for letter drawing
    const canvasWidth = 128;
    const canvasHeight = 128;
    canvas.width = canvasWidth;
    canvas.height = canvasHeight;
    canvas.style.width = '128px';
    canvas.style.height = '128px';
    canvas.style.border = '2px solid #000';
    canvas.style.background = '#fff';

    // Initialize brush size
    ctx.lineWidth = brushSizeInput.value * 2;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.strokeStyle = '#000';

    function updateBrushPreview(size) {
        const previewSize = Math.min(size * 2, 20); // Cap the preview size at 20px
        brushPreview.style.width = `${previewSize}px`;
        brushPreview.style.height = `${previewSize}px`;
        brushSizeValue.textContent = `${size * 2}px`;
    }

    // Update brush size and preview when slider changes
    brushSizeInput.addEventListener('input', () => {
        const size = brushSizeInput.value;
        ctx.lineWidth = size * 2;
        updateBrushPreview(size);
        // Save to localStorage
        localStorage.setItem('brushSize', size);
    });

    // Initialize brush preview
    updateBrushPreview(brushSizeInput.value);

    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;

    function getMousePos(canvas, evt) {
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        
        // Handle both mouse and touch events
        let clientX, clientY;
        if (evt.type.includes('touch')) {
            // Get the first touch point
            const touch = evt.touches[0] || evt.changedTouches[0];
            clientX = touch.clientX;
            clientY = touch.clientY;
        } else {
            clientX = evt.clientX;
            clientY = evt.clientY;
        }
        
        return {
            x: (clientX - rect.left) * scaleX,
            y: (clientY - rect.top) * scaleY
        };
    }

    // Mouse events
    canvas.addEventListener('mousedown', (e) => {
        isDrawing = true;
        const pos = getMousePos(canvas, e);
        [lastX, lastY] = [pos.x, pos.y];
    });

    canvas.addEventListener('mousemove', (e) => {
        if (!isDrawing) return;
        const pos = getMousePos(canvas, e);
        drawLine(lastX, lastY, pos.x, pos.y);
        [lastX, lastY] = [pos.x, pos.y];
    });

    // Touch events with improved handling
    canvas.addEventListener('touchstart', (e) => {
        e.preventDefault(); // Prevent scrolling
        isDrawing = true;
        const pos = getMousePos(canvas, e);
        [lastX, lastY] = [pos.x, pos.y];
    }, { passive: false });

    canvas.addEventListener('touchmove', (e) => {
        e.preventDefault(); // Prevent scrolling
        if (!isDrawing) return;
        const pos = getMousePos(canvas, e);
        drawLine(lastX, lastY, pos.x, pos.y);
        [lastX, lastY] = [pos.x, pos.y];
    }, { passive: false });

    function drawLine(x1, y1, x2, y2) {
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.strokeStyle = '#000';
        ctx.lineWidth = brushSizeInput.value * 2;
        ctx.stroke();
    }

    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);
    canvas.addEventListener('touchend', stopDrawing);
    canvas.addEventListener('touchcancel', stopDrawing);

    function stopDrawing() {
        isDrawing = false;
    }

    clearButton.addEventListener('click', () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // Do NOT fill with white, keep transparent
    });

    // Do NOT fill background on load, keep transparent

    // Save letter
    saveButton.addEventListener('click', async () => {
        const letter = letterInput.value;
        if (!letter || !/^[a-zA-Z]$/.test(letter)) {
            alert('Please enter a valid letter (A-Z or a-z)');
            return;
        }

        const imageData = canvas.toDataURL('image/png');
        try {
            const response = await fetch('/save_letter', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    letter: letter,
                    image: imageData
                })
            });

            if (response.ok) {
                alert('Letter saved successfully!');
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                // Do NOT fill with white, keep transparent
                letterInput.value = '';
            } else {
                alert('Error saving letter');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error saving letter');
        }
    });

    // Generate text
    generateButton.addEventListener('click', async () => {
        const text = textInput.value;
        if (!text) {
            alert('Please enter some text');
            return;
        }

        // Get selected page style
        const pageStyle = document.querySelector('input[name="pageStyle"]:checked').value;

        try {
            const response = await fetch('/generate_text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    text: text,
                    pageStyle: pageStyle 
                })
            });

            if (response.ok) {
                const data = await response.json();
                let warningHtml = '';
                if (data.warning) {
                    warningHtml = `<div style="color: #b30000; background: #fff3cd; border: 1px solid #ffeeba; padding: 10px; margin-bottom: 10px; border-radius: 6px; font-weight: bold;">${data.warning}</div>`;
                }
                previewContainer.innerHTML = `${warningHtml}<img src="${data.image}" alt="Generated text" style="max-width: 100%;">`;
            } else {
                alert('Error generating text');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error generating text');
        }
    });

    // --- Manage Letters Tab Logic ---
    async function loadLetters() {
        const lowercaseGrid = document.getElementById('lettersGrid');
        const uppercaseGrid = document.getElementById('uppercaseGrid');
        
        lowercaseGrid.innerHTML = '<p>Loading...</p>';
        uppercaseGrid.innerHTML = '<p>Loading...</p>';
        
        try {
            const response = await fetch('/list_letters');
            if (!response.ok) throw new Error('Failed to fetch letters');
            const data = await response.json();
            
            if (!data.letters.length) {
                lowercaseGrid.innerHTML = '<p>No letters saved yet.</p>';
                uppercaseGrid.innerHTML = '<p>No letters saved yet.</p>';
                return;
            }

            // Clear grids
            lowercaseGrid.innerHTML = '';
            uppercaseGrid.innerHTML = '';

            // Sort letters into lowercase and uppercase
            const lowercaseLetters = data.letters.filter(letter => letter.letter === letter.letter.toLowerCase());
            const uppercaseLetters = data.letters.filter(letter => letter.letter === letter.letter.toUpperCase());

            // Function to create letter item
            const createLetterItem = (letterObj) => {
                const div = document.createElement('div');
                div.className = 'letter-item';
                div.innerHTML = `
                    <div class="letter-label">${letterObj.letter}</div>
                    <img src="/letters/${letterObj.filename}" alt="${letterObj.letter}">
                    <button data-filename="${letterObj.filename}" class="delete-letter-btn">Delete</button>
                `;
                return div;
            };

            // Add letters to respective grids
            lowercaseLetters.forEach(letterObj => {
                lowercaseGrid.appendChild(createLetterItem(letterObj));
            });

            uppercaseLetters.forEach(letterObj => {
                uppercaseGrid.appendChild(createLetterItem(letterObj));
            });

            // Add delete handlers
            document.querySelectorAll('.delete-letter-btn').forEach(btn => {
                btn.onclick = async (e) => {
                    const filename = btn.getAttribute('data-filename');
                    if (!confirm('Delete this letter?')) return;
                    const resp = await fetch('/delete_letter', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ filename })
                    });
                    if (resp.ok) {
                        loadLetters();
                    } else {
                        alert('Failed to delete letter.');
                    }
                };
            });

        } catch (err) {
            lowercaseGrid.innerHTML = '<p>Error loading letters.</p>';
            uppercaseGrid.innerHTML = '<p>Error loading letters.</p>';
        }
    }

    // Attach group-header event listeners ONCE, after DOM is loaded
    document.querySelectorAll('.group-header').forEach(header => {
        header.addEventListener('click', () => {
            const group = header.dataset.group;
            const content = document.getElementById(`${group}-letters`);
            const arrow = header.querySelector('.arrow');
            header.classList.toggle('collapsed');
            content.classList.toggle('active');
        });
    });

    // Tab switching (add manage tab logic)
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tab = button.dataset.tab;
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            tabContents.forEach(content => {
                content.style.display = content.id === `${tab}-tab` ? 'block' : 'none';
            });
            if (tab === 'manage') {
                loadLetters();
            }
        });
    });
}); 