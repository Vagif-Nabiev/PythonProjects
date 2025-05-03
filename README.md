# Python Projects Collection

This repository contains three Python projects that demonstrate different aspects of programming and web development.

## 1. Caesar Cipher

A classic encryption technique implementation that allows users to encrypt and decrypt messages using the Caesar cipher method.

### Features:
- Encrypt text by shifting letters by a specified number
- Decrypt text using the same shift value
- Simple command-line interface
- Handles both uppercase and lowercase letters
- Preserves spaces and special characters

### Usage:
```python
python caesar_cipher.py
```

## 2. GeoGuess

A geography quiz game that tests your knowledge of countries and their capitals.

### Features:
- Multiple-choice questions about countries and capitals
- Score tracking
- Random question selection
- User-friendly interface
- Educational and fun

### Usage:
```python
python geoguess.py
```

## 3. WriteLikeMe

A web application that allows users to create their own handwriting style and generate text in that style.

### Features:
- Draw and save individual letters
- Generate text using your saved letters
- Three page styles: blank, lined, and grid
- Letter management system
- Web-based interface using Flask
- Real-time preview of generated text

### Setup:
1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
cd WriteLikeMe
python app.py
```

3. Access the application at `http://127.0.0.1:5000`

### How to Use WriteLikeMe:
1. **Draw Letters Tab**:
   - Draw a letter on the canvas
   - Enter the corresponding letter in the input field
   - Save the letter for future use

2. **Generate Text Tab**:
   - Choose a page style (blank, lined, or grid)
   - Enter the text you want to generate
   - Click "Generate" to see your text in your handwriting style

3. **Manage Letters Tab**:
   - View all your saved letters
   - Delete letters if needed
   - Organize letters by case (uppercase/lowercase)

## Requirements
- Python 3.x
- Flask
- Pillow (for WriteLikeMe)
- Other dependencies listed in requirements.txt

## License
This project is open source and available under the MIT License. 