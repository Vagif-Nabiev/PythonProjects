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
    const lettersGrid = document.getElementById('lettersGrid');

    // Set canvas size for letter drawing
    const canvasWidth = 128;
    const canvasHeight = 128;
    canvas.width = canvasWidth;
    canvas.height = canvasHeight;
    canvas.style.width = '128px';
    canvas.style.height = '128px';
    canvas.style.border = '2px solid #000';
    canvas.style.background = '#fff';

    ctx.lineWidth = 10;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.strokeStyle = '#000';

    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;

    function getMousePos(canvas, evt) {
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        return {
            x: (evt.clientX - rect.left) * scaleX,
            y: (evt.clientY - rect.top) * scaleY
        };
    }

    canvas.addEventListener('mousedown', (e) => {
        isDrawing = true;
        const pos = getMousePos(canvas, e);
        [lastX, lastY] = [pos.x, pos.y];
    });

    canvas.addEventListener('mousemove', (e) => {
        if (!isDrawing) return;
        const pos = getMousePos(canvas, e);
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(pos.x, pos.y);
        ctx.strokeStyle = '#000';
        ctx.stroke();
        [lastX, lastY] = [pos.x, pos.y];
    });

    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);

    function stopDrawing() {
        isDrawing = false;
    }

    brushSizeInput.addEventListener('input', () => {
        ctx.lineWidth = brushSizeInput.value * 2;
    });

    clearButton.addEventListener('click', () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // Do NOT fill with white, keep transparent
    });

    // Do NOT fill background on load, keep transparent

    // Save letter
    saveButton.addEventListener('click', async () => {
        const letter = letterInput.value.toLowerCase();
        if (!letter || !/^[a-z]$/.test(letter)) {
            alert('Please enter a valid letter (a-z)');
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

        try {
            const response = await fetch('/generate_text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            if (response.ok) {
                const data = await response.json();
                previewContainer.innerHTML = `<img src="${data.image}" alt="Generated text" style="max-width: 100%;">`;
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
        lettersGrid.innerHTML = '<p>Loading...</p>';
        try {
            const response = await fetch('/list_letters');
            if (!response.ok) throw new Error('Failed to fetch letters');
            const data = await response.json();
            if (!data.letters.length) {
                lettersGrid.innerHTML = '<p>No letters saved yet.</p>';
                return;
            }
            lettersGrid.innerHTML = '';
            data.letters.forEach(letterObj => {
                const div = document.createElement('div');
                div.className = 'letter-item';
                div.innerHTML = `
                    <div><b>${letterObj.letter}</b></div>
                    <img src="/letters/${letterObj.filename}" alt="${letterObj.letter}" style="width:48px;height:48px;background:#fff;border:1px solid #ccc;display:block;margin:4px auto;">
                    <button data-filename="${letterObj.filename}" class="delete-letter-btn">Delete</button>
                `;
                lettersGrid.appendChild(div);
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
            lettersGrid.innerHTML = '<p>Error loading letters.</p>';
        }
    }

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