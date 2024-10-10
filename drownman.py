import random

word_list = ["ayhan", "melih", "emre"]
correct_letters = []

random_index = random.randint(0, len(word_list) - 1)
chosen_word = word_list[random_index]
print("chosen word: " + chosen_word)

guesses = 0
while guesses < 7 :
    placeholder = ""
    guess = input("Guess a letter: ")

    if len(guess) != 1 or not guess.isalpha():
        print("Invalid input")
        continue

    if guess in chosen_word:
        if guess not in correct_letters:
            correct_letters.append(guess)
    else:
        guesses += 1

    for letter in chosen_word:
        if letter in correct_letters:
            placeholder += letter
        else:
            placeholder += "_"

    print(placeholder)
    print(f"Guesses left: {7 - guesses}")

    if "_" not in placeholder:
        print("you won")
        break
else:
    print("You lost")