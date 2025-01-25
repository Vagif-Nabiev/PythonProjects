alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def encrypt(original_text, shift_amount):
    hidden_text = ''
    for char in original_text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.lower()
            shifted_position = alphabet.index(char) + shift_amount
            shifted_position %= len(alphabet)
            new_char = alphabet[shifted_position]
            if is_upper:
                hidden_text += new_char.upper()
            else:
                hidden_text += new_char
        elif char.isdigit():
            shifted_position = numbers.index(char) + shift_amount
            shifted_position %= len(numbers)
            hidden_text += numbers[shifted_position]
        else:
            hidden_text += char
    return hidden_text

def decrypt(original_text, shift_amount):
    hidden_text = ''
    for char in original_text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.lower()
            shifted_position = alphabet.index(char) - shift_amount
            shifted_position %= len(alphabet)
            new_char = alphabet[shifted_position]
            if is_upper:
                hidden_text += new_char.upper()
            else:
                hidden_text += new_char
        elif char.isdigit():
            shifted_position = numbers.index(char) - shift_amount
            shifted_position %= len(numbers)
            hidden_text += numbers[shifted_position]
        else:
            hidden_text += char
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

history = []
while True:
    direction = input("Type 'encode' to encrypt, 'decode' to decrypt, 'exit' to quit, or 'history' to check operation history:\n").lower()

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

        continue_choice = input("Do you want to encode, decode or check history again? (yes/no):\n").lower()
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
