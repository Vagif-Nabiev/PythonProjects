# WriteLikeMe

## How It Works:
- A web application that converts typed text into personalized handwritten text using your own drawn letters.
- Users draw each letter in a 128x128px canvas, which gets saved as a transparent PNG.
- The backend assembles these letters onto lined paper, creating natural-looking handwritten text.
- Users can manage their saved letters through a dedicated interface.

## Features:
- Draw and save your own custom letters
- Generate handwritten text using your letters
- Manage (view/delete) saved letters
- Download or copy the generated handwritten text

## Technologies Used:
- Flask – for the web application framework
- Pillow (PIL) – for image processing
- HTML/CSS/JavaScript – for the frontend interface

## How to Use:
1. Navigate to the WriteLikeMe folder
2. Install requirements: `pip install flask pillow`
3. Run the application: `python app.py`
4. Open http://127.0.0.1:5000 in your browser
5. Start drawing your letters and generating handwritten text!
