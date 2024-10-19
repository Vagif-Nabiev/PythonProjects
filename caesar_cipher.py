alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']


def encrypt(original_text, shift_amount):
    hidden_text = ''
    for letter in original_text:
        if letter in alphabet:
            shifted_position = alphabet.index(letter) + shift_amount
            shifted_position %= len(alphabet)
            hidden_text += alphabet[shifted_position]
        else:
            hidden_text += letter  # Keep non-alphabet characters unchanged
    return hidden_text


def decrypt(original_text, shift_amount):
    hidden_text = ''
    for letter in original_text:
        if letter in alphabet:
            shifted_position = alphabet.index(letter) - shift_amount
            shifted_position %= len(alphabet)
            hidden_text += alphabet[shifted_position]
        else:
            hidden_text += letter  # Keep non-alphabet characters unchanged
    return hidden_text


while True:
    direction = input("Type 'encode' to encrypt or 'decode' to decrypt, or 'exit' to quit:\n").lower()

    if direction in ['encode', 'decode']:
        text = input("Type your message:\n")
        shift = int(input("Type the shift:\n"))

        if direction == 'encode':
            encoded_text = encrypt(text, shift)
            print('Encoded text: ' + encoded_text)
        elif direction == 'decode':
            decoded_text = decrypt(text, shift)
            print('Decoded text: ' + decoded_text)

        # Ask if the user wants to continue
        continue_choice = input("Do you want to encode or decode again? (yes/no):\n").lower()
        if continue_choice != 'yes':
            print("Goodbye!")
            break

    elif direction == 'exit':
        print("Goodbye!")
        break

    else:
        print("Invalid input. Please try again.")
