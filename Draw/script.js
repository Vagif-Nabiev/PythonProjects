// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get all required elements
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d', { alpha: true }); // Enable alpha channel for transparency
    const colorPicker = document.getElementById('color');
    const sizePicker = document.getElementById('size');
    const clearButton = document.getElementById('clear');
    const saveButton = document.getElementById('save');

    // Set canvas size and DPI
    const targetWidth = 431;
    const targetHeight = 1000;
    const dpi = 96;
    
    // Set physical size in pixels
    canvas.width = targetWidth;
    canvas.height = targetHeight;
    
    // Set display size (CSS pixels)
    canvas.style.width = `${targetWidth}px`;
    canvas.style.height = `${targetHeight}px`;

    // Set initial drawing style
    ctx.strokeStyle = colorPicker.value;
    ctx.lineWidth = sizePicker.value;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    // Drawing state
    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;
    let drawingBounds = {
        minX: Infinity,
        minY: Infinity,
        maxX: -Infinity,
        maxY: -Infinity
    };

    // Drawing functions
    function startDrawing(e) {
        isDrawing = true;
        [lastX, lastY] = getMousePos(e);
        updateDrawingBounds(lastX, lastY);
    }

    function draw(e) {
        if (!isDrawing) return;

        const [x, y] = getMousePos(e);
        updateDrawingBounds(x, y);
        
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(x, y);
        ctx.strokeStyle = colorPicker.value;
        ctx.lineWidth = sizePicker.value;
        ctx.stroke();

        [lastX, lastY] = [x, y];
    }

    function stopDrawing() {
        isDrawing = false;
    }

    function getMousePos(e) {
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        return [
            (e.clientX - rect.left) * scaleX,
            (e.clientY - rect.top) * scaleY
        ];
    }

    function updateDrawingBounds(x, y) {
        drawingBounds.minX = Math.min(drawingBounds.minX, x);
        drawingBounds.minY = Math.min(drawingBounds.minY, y);
        drawingBounds.maxX = Math.max(drawingBounds.maxX, x);
        drawingBounds.maxY = Math.max(drawingBounds.maxY, y);
    }

    function resizeAndCenterDrawing() {
        // Get the current drawing data
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        
        // Calculate the drawing dimensions
        const drawingWidth = drawingBounds.maxX - drawingBounds.minX;
        const drawingHeight = drawingBounds.maxY - drawingBounds.minY;
        
        // Add some padding to the drawing bounds
        const padding = 20; // pixels of padding
        const paddedWidth = drawingWidth + (padding * 2);
        const paddedHeight = drawingHeight + (padding * 2);
        
        // Calculate the scale factor to fit the canvas with padding
        const scaleX = (canvas.width - (padding * 2)) / paddedWidth;
        const scaleY = (canvas.height - (padding * 2)) / paddedHeight;
        const scale = Math.min(scaleX, scaleY);
        
        // Calculate the new position to center the drawing
        const newWidth = paddedWidth * scale;
        const newHeight = paddedHeight * scale;
        const offsetX = (canvas.width - newWidth) / 2;
        const offsetY = (canvas.height - newHeight) / 2;
        
        // Clear the canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Create a temporary canvas to store the original drawing
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = canvas.width;
        tempCanvas.height = canvas.height;
        const tempCtx = tempCanvas.getContext('2d', { alpha: true });
        tempCtx.putImageData(imageData, 0, 0);
        
        // Draw the resized and centered image with padding
        ctx.drawImage(tempCanvas, 
            drawingBounds.minX - padding, drawingBounds.minY - padding, 
            paddedWidth, paddedHeight,
            offsetX, offsetY, newWidth, newHeight
        );
        
        // Reset drawing bounds
        drawingBounds = {
            minX: Infinity,
            minY: Infinity,
            maxX: -Infinity,
            maxY: -Infinity
        };
    }

    // Event listeners
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);

    // Touch support
    canvas.addEventListener('touchstart', (e) => {
        e.preventDefault();
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent('mousedown', {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        canvas.dispatchEvent(mouseEvent);
    });

    canvas.addEventListener('touchmove', (e) => {
        e.preventDefault();
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent('mousemove', {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        canvas.dispatchEvent(mouseEvent);
    });

    canvas.addEventListener('touchend', (e) => {
        e.preventDefault();
        const mouseEvent = new MouseEvent('mouseup', {});
        canvas.dispatchEvent(mouseEvent);
    });

    // Clear canvas
    clearButton.addEventListener('click', () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawingBounds = {
            minX: Infinity,
            minY: Infinity,
            maxX: -Infinity,
            maxY: -Infinity
        };
    });

    // Save as PNG
    saveButton.addEventListener('click', () => {
        // Resize and center the drawing before saving
        resizeAndCenterDrawing();
        
        // Create a new canvas with exact specifications
        const exportCanvas = document.createElement('canvas');
        exportCanvas.width = targetWidth;
        exportCanvas.height = targetHeight;
        const exportCtx = exportCanvas.getContext('2d', { alpha: true });
        
        // Copy the drawing to the export canvas
        exportCtx.drawImage(canvas, 0, 0);
        
        // Create the download link
        const link = document.createElement('a');
        link.download = 'handwriting.png';
        
        // Convert to PNG with 32-bit depth
        const pngData = exportCanvas.toDataURL('image/png', 1.0);
        link.href = pngData;
        link.click();
    });
});