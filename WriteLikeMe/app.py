import os
import random
import base64
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, flash, session, send_file, make_response
from PIL import Image, ImageDraw, ImageEnhance
from io import BytesIO
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Writing
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/Vagifnbv/mysite/writelike.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def add_vary_cookie_header(response):
    response.headers['Vary'] = 'Cookie'
    return response

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Use absolute path for letters directory
LETTERS_DIR = '/home/Vagifnbv/mysite/letters'
if not os.path.exists(LETTERS_DIR):
    os.makedirs(LETTERS_DIR)

# Create a temporary directory for session-based letters
TEMP_LETTERS_DIR = os.path.join(os.path.dirname(__file__), 'temp_letters')
if not os.path.exists(TEMP_LETTERS_DIR):
    os.makedirs(TEMP_LETTERS_DIR)

def save_base64_image(base64_string, filename, is_temporary=False):
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

    # Save to either temporary or permanent directory
    save_dir = TEMP_LETTERS_DIR if is_temporary else LETTERS_DIR
    full_path = os.path.join(save_dir, filename)
    image.save(full_path, 'PNG')

    # If temporary, store the filename in session
    if is_temporary:
        if 'temp_letters' not in session:
            session['temp_letters'] = []
        session['temp_letters'].append(filename)
        session.modified = True

letter_offsets = {
    "f": 10, "p": 10, "q": 10, "g": 10, "j": 15, "y": 10
}

@app.route('/')
def index():
    return render_template('index.html', logged_in=current_user.is_authenticated)

@app.route('/save_letter', methods=['POST'])
def save_letter():
    data = request.json
    letter = data['letter']
    image_data = data['image']

    # Generate filename
    count = len([f for f in os.listdir(LETTERS_DIR if current_user.is_authenticated else TEMP_LETTERS_DIR)
                 if f.startswith(letter)])
    filename = f"{letter}{count + 1}_{count + 1}.png"

    # Save based on authentication status
    save_base64_image(image_data, filename, not current_user.is_authenticated)

    return jsonify({'success': True})

@app.route('/generate_text', methods=['POST'])
def generate_text():
    data = request.json
    text = data['text']
    page_style = data.get('pageStyle', 'lined')

    # Check if user has any saved letters
    available_letters = set()
    if current_user.is_authenticated:
        # Get letters from permanent storage
        for f in os.listdir(LETTERS_DIR):
            if f.lower().endswith('.png'):
                available_letters.add(f[0])
    else:
        # Get letters from temporary storage
        temp_letters = session.get('temp_letters', [])
        for f in temp_letters:
            if os.path.exists(os.path.join(TEMP_LETTERS_DIR, f)):
                available_letters.add(f[0])

    # If no letters are saved, return an error
    if not available_letters:
        return jsonify({
            'error': True,
            'message': 'Please draw and save some letters first before generating text.'
        }), 400

    canvas_width = 1000
    canvas_height = 1000
    line_spacing = 40
    margin_x = 50
    x, y = margin_x, 50

    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(canvas)

    # Draw page style based on selection
    if page_style == 'lined':
        for line_y in range(0, canvas_height, line_spacing):
            draw.line([(0, line_y), (canvas_width, line_y)], fill="lightgray", width=1)
    elif page_style == 'grid':
        for line_y in range(0, canvas_height, line_spacing):
            draw.line([(0, line_y), (canvas_width, line_y)], fill="lightgray", width=1)
        for line_x in range(0, canvas_width, line_spacing):
            draw.line([(line_x, 0), (line_x, canvas_height)], fill="lightgray", width=1)

    line_height = line_spacing - 10

    # Find missing letters in the input text (ignore spaces)
    missing_letters = set()
    for char in text:
        if char == ' ':
            continue
        if char not in available_letters and char.lower() not in available_letters and char.upper() not in available_letters:
            missing_letters.add(char)

    # Render text
    for char in text:
        if char == " ":
            space_width = int(line_height * 0.5)
            x += space_width
            continue

        # Try to find the letter in any case
        letter_files = []
        if current_user.is_authenticated:
            # Search in permanent storage first
            letter_files = [f for f in os.listdir(LETTERS_DIR) if f.startswith(char)]
            if not letter_files:
                letter_files = [f for f in os.listdir(LETTERS_DIR) if f.startswith(char.lower())]
            if not letter_files:
                letter_files = [f for f in os.listdir(LETTERS_DIR) if f.startswith(char.upper())]

        if not letter_files:
            # Search in temporary storage
            temp_letters = session.get('temp_letters', [])
            letter_files = [f for f in temp_letters if f.startswith(char) and os.path.exists(os.path.join(TEMP_LETTERS_DIR, f))]
            if not letter_files:
                letter_files = [f for f in temp_letters if f.startswith(char.lower()) and os.path.exists(os.path.join(TEMP_LETTERS_DIR, f))]
            if not letter_files:
                letter_files = [f for f in temp_letters if f.startswith(char.upper()) and os.path.exists(os.path.join(TEMP_LETTERS_DIR, f))]

        if not letter_files:
            continue

        # Get the image path based on storage type
        selected_file = random.choice(letter_files)
        if current_user.is_authenticated:
            img_path = os.path.join(LETTERS_DIR, selected_file)
        else:
            img_path = os.path.join(TEMP_LETTERS_DIR, selected_file)

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
    if missing_letters:
        response['warning'] = f"The following letters are missing and could not be rendered: {', '.join(sorted(missing_letters))}"
        response['missing_letters'] = sorted(missing_letters)
    return jsonify(response)

@app.route('/letters/<path:filename>')
def serve_letter_image(filename):
    # Try permanent directory first, then temporary
    if os.path.exists(os.path.join(LETTERS_DIR, filename)):
        return send_from_directory(LETTERS_DIR, filename)
    elif os.path.exists(os.path.join(TEMP_LETTERS_DIR, filename)):
        return send_from_directory(TEMP_LETTERS_DIR, filename)
    return '', 404

@app.route('/list_letters')
def list_letters():
    # Get permanent letters if logged in
    if current_user.is_authenticated:
        files = [f for f in os.listdir(LETTERS_DIR) if f.lower().endswith('.png')]
    else:
        # Get temporary letters from session
        temp_letters = session.get('temp_letters', [])
        files = [f for f in temp_letters if os.path.exists(os.path.join(TEMP_LETTERS_DIR, f))]

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

    # Delete from appropriate directory
    if current_user.is_authenticated:
        file_path = os.path.join(LETTERS_DIR, filename)
    else:
        file_path = os.path.join(TEMP_LETTERS_DIR, filename)
        # Also remove from session
        if 'temp_letters' in session:
            session['temp_letters'] = [f for f in session['temp_letters'] if f != filename]
            session.modified = True

    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'File not found'}), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    # Clear temporary letters when logging out
    if 'temp_letters' in session:
        for filename in session['temp_letters']:
            file_path = os.path.join(TEMP_LETTERS_DIR, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        session.pop('temp_letters', None)
    logout_user()
    return redirect(url_for('index'))

@app.route('/download/<format>', methods=['POST'])
@login_required
def download_text(format):
    try:
        data = request.json
        text = data['text']
        page_style = data.get('pageStyle', 'lined')

        # Generate the image as before
        canvas_width = 1000
        canvas_height = 1000
        line_spacing = 40
        margin_x = 50
        x, y = margin_x, 50

        # Create image with white background
        canvas_img = Image.new("RGB", (canvas_width, canvas_height), "white")
        draw = ImageDraw.Draw(canvas_img)

        # Draw page style based on selection
        if page_style == 'lined':
            for line_y in range(0, canvas_height, line_spacing):
                draw.line([(0, line_y), (canvas_width, line_y)], fill="lightgray", width=1)
        elif page_style == 'grid':
            for line_y in range(0, canvas_height, line_spacing):
                draw.line([(0, line_y), (canvas_width, line_y)], fill="lightgray", width=1)
            for line_x in range(0, canvas_width, line_spacing):
                draw.line([(line_x, 0), (line_x, canvas_height)], fill="lightgray", width=1)

        line_height = line_spacing - 10

        # Render text
        for char in text:
            if char == " ":
                space_width = int(line_height * 0.5)
                x += space_width
                continue

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

            # Create a new RGB image with white background for the letter
            letter_bg = Image.new('RGB', letter_img.size, 'white')
            letter_bg.paste(letter_img, mask=letter_img.split()[3] if len(letter_img.split()) > 3 else None)

            canvas_img.paste(letter_bg, (x, y))
            x += target_width

            if x + target_width > canvas_width:
                x = margin_x
                y += line_spacing
                if y + line_height > canvas_height:
                    break

        if format == 'png':
            # Save as PNG
            output = BytesIO()
            canvas_img.save(output, format='PNG', optimize=True, quality=95)
            output.seek(0)

            response = make_response(output.getvalue())
            response.headers['Content-Type'] = 'image/png'
            response.headers['Content-Disposition'] = 'attachment; filename=handwritten_text.png'
            return response

        elif format == 'pdf':
            # Create a temporary directory if it doesn't exist
            temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
            os.makedirs(temp_dir, exist_ok=True)

            # Save the image temporarily
            temp_img_path = os.path.join(temp_dir, 'temp_image.png')
            canvas_img.save(temp_img_path, 'PNG', quality=95)

            # Create PDF
            temp_pdf_path = os.path.join(temp_dir, 'temp.pdf')
            c = canvas.Canvas(temp_pdf_path, pagesize=letter)

            # Get the dimensions of the letter size page
            page_width, page_height = letter

            # Calculate scaling to fit the image on the page with margins
            margin = 50  # points
            image_aspect = canvas_width / canvas_height
            page_aspect = (page_width - 2*margin) / (page_height - 2*margin)

            if image_aspect > page_aspect:
                # Image is wider than page ratio
                width = page_width - 2*margin
                height = width / image_aspect
            else:
                # Image is taller than page ratio
                height = page_height - 2*margin
                width = height * image_aspect

            # Center the image on the page
            x = (page_width - width) / 2
            y = (page_height - height) / 2

            # Draw the image
            c.drawImage(temp_img_path, x, y, width=width, height=height)
            c.save()

            # Read the PDF file
            with open(temp_pdf_path, 'rb') as pdf_file:
                pdf_data = pdf_file.read()

            # Clean up temporary files
            os.remove(temp_img_path)
            os.remove(temp_pdf_path)

            response = make_response(pdf_data)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=handwritten_text.pdf'
            return response

        else:
            return jsonify({'error': 'Unsupported format'}), 400

    except Exception as e:
        print(f"Error in download_text: {str(e)}")
        return jsonify({'error': f'Failed to generate file: {str(e)}'}), 500

@app.route('/clear_temp_letters', methods=['POST'])
def clear_temp_letters():
    # Only clear if user is not logged in and this is a real window close
    if not current_user.is_authenticated:
        # Get the referrer to check if this is a navigation
        referrer = request.headers.get('Referer', '')
        if not any(page in referrer for page in ['/login', '/register']):
            # Clear the session's temp_letters list
            session.pop('temp_letters', None)

            # Remove all files from TEMP_LETTERS_DIR
            try:
                for filename in os.listdir(TEMP_LETTERS_DIR):
                    file_path = os.path.join(TEMP_LETTERS_DIR, filename)
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
            except Exception as e:
                print(f"Error clearing temporary letters: {e}")

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=False)
