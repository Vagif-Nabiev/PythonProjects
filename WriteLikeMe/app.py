import os
import random
import base64
from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image, ImageDraw, ImageEnhance
from io import BytesIO

app = Flask(__name__)

# Use absolute path for letters directory
LETTERS_DIR = '/home/Vagifnbv/mysite/letters'
if not os.path.exists(LETTERS_DIR):
    os.makedirs(LETTERS_DIR)

def save_base64_image(base64_string, filename):
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data)).convert('RGBA')

    orig_w, orig_h = image.size

    bbox = image.getbbox()
    if bbox:
        cropped = image.crop(bbox)
        cropped = cropped.resize((orig_w, orig_h), Image.Resampling.LANCZOS)
        image = cropped

    image.save(filename, 'PNG')

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
    
    count = len([f for f in os.listdir(LETTERS_DIR) if f.startswith(letter)])
    filename = os.path.join(LETTERS_DIR, f"{letter}{count + 1}_{count + 1}.png")
    
    save_base64_image(image_data, filename)
    
    return jsonify({'success': True})

@app.route('/generate_text', methods=['POST'])
def generate_text():
    data = request.json
    text = data['text']
    page_style = data.get('pageStyle', 'lined')  # Default to lined if not specified

    canvas_width = 1000
    canvas_height = 1000
    line_spacing = 40
    margin_x = 50
    x, y = margin_x, 50

    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(canvas)

    # Draw page style based on selection
    if page_style == 'lined':
        # Draw horizontal lines
        for line_y in range(0, canvas_height, line_spacing):
            draw.line([(0, line_y), (canvas_width, line_y)], fill="lightgray", width=1)
    elif page_style == 'grid':
        # Draw both horizontal and vertical lines
        for line_y in range(0, canvas_height, line_spacing):
            draw.line([(0, line_y), (canvas_width, line_y)], fill="lightgray", width=1)
        for line_x in range(0, canvas_width, line_spacing):
            draw.line([(line_x, 0), (line_x, canvas_height)], fill="lightgray", width=1)
    # For blank style, no lines are drawn

    line_height = line_spacing - 10

    # Collect all available letters
    available_letters = set()
    for f in os.listdir(LETTERS_DIR):
        if f.lower().endswith('.png'):
            available_letters.add(f[0])

    # Find missing letters in the input text (ignore spaces)
    missing_letters = set()
    for char in text:
        if char == ' ':
            continue
        if char not in available_letters and char.lower() not in available_letters and char.upper() not in available_letters:
            missing_letters.add(char)

    # Render text as before, but skip missing letters
    for char in text:
        if char == " ":
            space_width = int(line_height * 0.5)
            x += space_width
            continue

        # Try to find the letter in any case
        letter_files = [f for f in os.listdir(LETTERS_DIR) if f.startswith(char)]
        if not letter_files:
            letter_files = [f for f in os.listdir(LETTERS_DIR) if f.startswith(char.lower())]
        if not letter_files:
            letter_files = [f for f in os.listdir(LETTERS_DIR) if f.startswith(char.upper())]
        if not letter_files:
            continue

        img_path = os.path.join(LETTERS_DIR, random.choice(letter_files))
        letter_img = Image.open(img_path).convert("RGBA")

        aspect_ratio = letter_img.width / letter_img.height
        target_width = int(line_height * aspect_ratio)
        letter_img = letter_img.resize((target_width, line_height), Image.Resampling.LANCZOS)

        canvas.paste(letter_img, (x, y), mask=letter_img)

        x += target_width

        if x + target_width > canvas_width:
            x = margin_x
            y += line_spacing
            if y + line_height > canvas_height:
                break

    buffered = BytesIO()
    canvas.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    response = {'image': f"data:image/png;base64,{img_str}"}
    if not available_letters:
        response['warning'] = 'No letters have been saved yet. Please draw and save some letters first.'
    elif missing_letters:
        response['warning'] = f"The following letters are missing and could not be rendered: {', '.join(sorted(missing_letters))}"
        response['missing_letters'] = sorted(missing_letters)
    return jsonify(response)

@app.route('/letters/<path:filename>')
def serve_letter_image(filename):
    return send_from_directory(LETTERS_DIR, filename)

@app.route('/list_letters')
def list_letters():
    files = [f for f in os.listdir(LETTERS_DIR) if f.lower().endswith('.png')]
    letters = []
    for f in files:
        letter = f[0]
        letters.append({'filename': f, 'letter': letter})
    return jsonify({'letters': letters})

@app.route('/delete_letter', methods=['POST'])
def delete_letter():
    data = request.json
    filename = data.get('filename')
    if not filename:
        return jsonify({'success': False, 'error': 'No filename provided'}), 400
    file_path = os.path.join(LETTERS_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True) 
