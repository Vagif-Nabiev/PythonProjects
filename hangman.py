import random
import pycountry
import pandas as pd

country_names = [country.name for country in pycountry.countries]

df = pd.DataFrame(country_names, columns=["Country Name"])

correct_letters = []

random_index = random.randint(0, len(country_names) - 1)
chosen_word = country_names[random_index].lower()
print("chosen word: " + chosen_word)

guesses = 0
while guesses < 7:
    placeholder = ""
    guess = input("Guess a letter: ").lower()

    if len(guess) != 1 or not guess.isalpha():
        print("Invalid input. Please guess a single letter.")
        continue

    if guess in correct_letters:
        print(f"You've already guessed '{guess}'. Try a different letter.")
        continue

    if guess in chosen_word:
        correct_letters.append(guess)
    else:
        guesses += 1

    for letter in chosen_word:
        if letter in correct_letters:
            placeholder += letter
        elif letter == " ":
            placeholder += " "
        else:
            placeholder += "_"

    print(placeholder)
    print(f"Guesses left: {7 - guesses}")

    if "_" not in placeholder:
        print("You won!")
        break
else:
    print("You lost")