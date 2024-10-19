# Country Guessing Game

This project is a simple command-line guessing game where the player has to guess the letters of a randomly chosen country's name. The game is similar to Hangman but uses country names as the words to guess.

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

Enjoy the game!
