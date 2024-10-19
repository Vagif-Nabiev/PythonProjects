alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
direction = input("Type 'encode' to encrypt or 'decode' to decrypt:\n ").lower()
text = input("Type your message:\n")
shift = int(input("Type the shift:\n"))

if direction == 'encode':
    def encrypt(original_text, shift_amount):
        hidden_text = ''
        for letter in original_text:
            if letter in alphabet:
                shifted_position = alphabet.index(letter) + shift_amount
                shifted_position %= len(alphabet)
                hidden_text += alphabet[shifted_position]
        print('Encoded text: '+hidden_text, end='')
    encrypt(text, shift)

elif direction == 'decode':
    def decrypt(original_text, shift_amount):
        hidden_text = ''
        for letter in original_text:
            if letter in alphabet:
                shifted_position = alphabet.index(letter) - shift_amount
                shifted_position %= len(alphabet)
                hidden_text += alphabet[shifted_position]
        print('Decoded text: '+hidden_text, end='')
    decrypt(text, shift)