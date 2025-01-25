alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']


def encrypt(original_text, shift_amount):
    hidden_text = ''
    for letter in original_text:
        if letter.isalpha():
            # Handle both lowercase and uppercase
            is_upper = letter.isupper()
            letter = letter.lower()
            shifted_position = alphabet.index(letter) + shift_amount
            shifted_position %= len(alphabet)
            new_letter = alphabet[shifted_position]
            if is_upper:
                hidden_text += new_letter.upper()
            else:
                hidden_text += new_letter
        else:
            hidden_text += letter  # Keep non-alphabet characters unchanged
    return hidden_text


def decrypt(original_text, shift_amount):
    hidden_text = ''
    for letter in original_text:
        if letter.isalpha():
            # Handle both lowercase and uppercase
            is_upper = letter.isupper()
            letter = letter.lower()
            shifted_position = alphabet.index(letter) - shift_amount
            shifted_position %= len(alphabet)
            new_letter = alphabet[shifted_position]
            if is_upper:
                hidden_text += new_letter.upper()
            else:
                hidden_text += new_letter
        else:
            hidden_text += letter  # Keep non-alphabet characters unchanged
    return hidden_text


def get_valid_shift():
    while True:
        try:
            shift = int(input("Type the shift (1-25):\n"))
            if 1 <= shift <= 25:
                return shift
            else:
                print("Please enter a shift between 1 and 25.")
        except ValueError:
            print("Please enter a valid number.")


history = []  # To store history of encoded and decoded messages

while True:
    direction = input("Type 'encode' to encrypt, 'decode' to decrypt, 'exit' to quit,or 'hisotry' to check operation history:\n").lower()

    if direction in ['encode', 'decode']:
        text = input("Type your message:\n")
        shift = get_valid_shift()

        if direction == 'encode':
            encoded_text = encrypt(text, shift)
            print('Encoded text: ' + encoded_text)
            history.append(f"Encoded: {text} -> {encoded_text} with shift {shift}")
        elif direction == 'decode':
            decoded_text = decrypt(text, shift)
            print('Decoded text: ' + decoded_text)
            history.append(f"Decoded: {text} -> {decoded_text} with shift {shift}")

        # Ask if the user wants to continue
        continue_choice = input("Do you want to encode, decode again? or check history (yes/no):\n").lower()
        if continue_choice == 'no':
            print("Goodbye!")
            break

    elif direction == 'history':
        if history:
            print("History of operations:")
            for entry in history:
                print(entry)
        else:
            print("No history available.")
        continue_choice = input("Do you want to continue? (yes/no):\n").lower()
        if continue_choice == 'no':
            print("Goodbye!")
            break

    elif direction == 'exit':
        print("Goodbye!")
        break

    else:
        print("Invalid input. Please try again.")
