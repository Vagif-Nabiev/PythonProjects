import os
import random
import base64
from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image, ImageDraw, ImageEnhance
from io import BytesIO

app = Flask(__name__)

# Create letters directory if it doesn't exist
if not os.path.exists('letters'):
    os.makedirs('letters')

def save_base64_image(base64_string, filename):
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data)).convert('RGBA')

    orig_w, orig_h = image.size

    # Crop to content
    bbox = image.getbbox()
    if bbox:
        cropped = image.crop(bbox)
        # Resize cropped letter to fill the original box
        cropped = cropped.resize((orig_w, orig_h), Image.Resampling.LANCZOS)
        image = cropped

    image.save(filename, 'PNG')

# Define offsets for specific letters that need to be placed lower
letter_offsets = {
    "f": 10, "p": 10, "q": 10, "g": 10, "j": 15, "y": 10
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_letter', methods=['POST'])
def save_letter():
    data = request.json
    letter = data['letter']
    image_data = data['image']
    
    # Generate a unique filename for the letter
    count = len([f for f in os.listdir('letters') if f.startswith(letter)])
    filename = f"letters/{letter}{count + 1}_{count + 1}.png"
    
    # Save the image
    save_base64_image(image_data, filename)
    
    return jsonify({'success': True})

@app.route('/generate_text', methods=['POST'])
def generate_text():
    data = request.json
    text = data['text']

    # Canvas settings
    canvas_width = 1000
    canvas_height = 1000
    line_spacing = 40
    margin_x = 50
    x, y = margin_x, 50

    # Create a blank canvas with lines
    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(canvas)

    # Draw lines for the blank paper
    for line_y in range(0, canvas_height, line_spacing):
        draw.line([(0, line_y), (canvas_width, line_y)], fill="lightgray", width=1)

    # Target height to fit letters between the lines
    line_height = line_spacing - 10

    for char in text:
        if char == " ":
            space_width = int(line_height * 0.5)
            x += space_width
            continue

        letter_files = [f for f in os.listdir('letters') if f.startswith(char.lower())]
        if not letter_files:
            continue

        img_path = f"letters/{random.choice(letter_files)}"
        letter_img = Image.open(img_path).convert("RGBA")

        # Resize letter to fit between lines
        aspect_ratio = letter_img.width / letter_img.height
        target_width = int(line_height * aspect_ratio)
        letter_img = letter_img.resize((target_width, line_height), Image.Resampling.LANCZOS)

        # Paste letter at current position
        canvas.paste(letter_img, (x, y), mask=letter_img)

        x += target_width

        # Move to next line if needed
        if x + target_width > canvas_width:
            x = margin_x
            y += line_spacing
            if y + line_height > canvas_height:
                break

    # Convert to base64 for web
    buffered = BytesIO()
    canvas.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return jsonify({'image': f"data:image/png;base64,{img_str}"})

@app.route('/letters/<path:filename>')
def serve_letter_image(filename):
    return send_from_directory('letters', filename)

@app.route('/list_letters')
def list_letters():
    files = [f for f in os.listdir('letters') if f.lower().endswith('.png')]
    letters = []
    for f in files:
        # Try to extract the letter from the filename
        letter = f[0]
        letters.append({'filename': f, 'letter': letter})
    return jsonify({'letters': letters})

@app.route('/delete_letter', methods=['POST'])
def delete_letter():
    data = request.json
    filename = data.get('filename')
    if not filename:
        return jsonify({'success': False, 'error': 'No filename provided'}), 400
    file_path = os.path.join('letters', filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True) 