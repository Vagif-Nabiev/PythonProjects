<details>
<summary>1. Country Guessing Game</summary>

## How It Works:
- A random country is selected from a list of all the countries in the world using the `pycountry` library.
- The player has 7 guesses to figure out the country's name, one letter at a time.
- For each correct letter, the letter is revealed in its correct position.
- For each incorrect guess, the number of remaining guesses decreases.
- The game ends when either the player correctly guesses all the letters of the country's name, or they run out of guesses.

## Libraries Used:
- `random` – to select a random country.
- `pycountry` – to retrieve a list of country names.
- `pandas` – to create a DataFrame of the country names (optional for data handling).

## How to Play:
1. Run the program.
2. Guess one letter at a time.
3. Try to guess the entire country's name before running out of guesses.
4. You win if you guess the country's name, and lose if you make 7 incorrect guesses.

Enjoy the [game](https://github.com/Vagif-Nabiev/PythonProjects/blob/main/geoguess.py)!

</details>

<details>
<summary>2. WriteLikeMe</summary>

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
1. Navigate to the [WriteLikeMe folder](https://github.com/Vagif-Nabiev/PythonProjects/tree/main/WriteLikeMe)
2. Install requirements: `pip install flask pillow`
3. Run the application: `python app.py`
4. Open http://127.0.0.1:5000 in your browser
5. Start drawing your letters and generating handwritten text!

</details>

<details>
<summary>3. Caesar Cipher</summary>

## How It Works:
- A classic encryption/decryption tool that implements the Caesar Cipher algorithm.
- Users can encode or decode messages by shifting letters and numbers by a specified amount.
- The program maintains a history of all encoding and decoding operations.
- Supports both uppercase and lowercase letters, numbers, and preserves special characters.

## Features:
- Encrypt messages with a custom shift value (1-25)
- Decrypt messages using the same shift value
- View operation history
- Support for letters, numbers, and special characters
- Case-sensitive encryption/decryption

## How to Use:
1. Run the [program](https://github.com/Vagif-Nabiev/PythonProjects/blob/main/caesar_cipher.py)
2. Choose to either 'encode' or 'decode'
3. Enter your message
4. Specify the shift amount (1-25)
5. View the result
6. Optionally check the history of operations
7. Continue or exit the program

</details>
