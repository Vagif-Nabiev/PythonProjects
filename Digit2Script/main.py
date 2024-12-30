import random
from PIL import Image, ImageDraw, ImageEnhance

# Letter map for mapping letters to their respective images
def generate_paths(letter, count):
    if letter.islower():
        return [f"letters/{letter}{i}_{i}.png" for i in range(1, count + 1)]
    elif letter.isupper():
        return [f"letters/{letter}_{i}.png" for i in range(1, count + 1)]

# Create letter map for uppercase and lowercase letters
letter_map = {
    letter: generate_paths(letter, 3) for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
}
letter_map.update({
    letter.lower(): generate_paths(letter.lower(), 5) for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
})

# Define offsets for specific letters that need to be placed lower
letter_offsets = {
    "f": 10, "p": 10, "q": 10, "g": 10, "j": 15, "y": 10
}

# Input text from the user
user_input = input("Enter a text: ")

# Canvas settings
canvas_width = 1000
canvas_height = 300
line_spacing = 40
margin_x = 50  # Space at the start of each new line
x, y = margin_x, 50  # Initial position

# Create a blank canvas with lines
canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
draw = ImageDraw.Draw(canvas)

# Draw lines for the blank paper
for line_y in range(0, canvas_height, line_spacing):
    draw.line([(0, line_y), (canvas_width, line_y)], fill="lightgray", width=1)

# Target height to fit letters between the lines
line_height = line_spacing - 10  # Slight padding above and below

# Loop through each character in the input
for char in user_input:
    if char == " ":
        # Add space for spaces
        x += int(line_height * 1.1)  # Space for " " (30% of line height)
        continue

    if char in letter_map:
        # Open the corresponding letter image
        img_path = random.choice(letter_map[char])
        letter_img = Image.open(img_path).convert("RGBA")

        # Darken the letter image
        brightness_enhancer = ImageEnhance.Brightness(letter_img)
        letter_img = brightness_enhancer.enhance(1.0)  # Adjust to make it darker

        # Sharpen the letter image
        sharpness_enhancer = ImageEnhance.Sharpness(letter_img)
        letter_img = sharpness_enhancer.enhance(2.0)  # Increase sharpness (2.0 is stronger)

        # Resize the letter image to fit the line height
        aspect_ratio = letter_img.width / letter_img.height
        target_width = int(line_height * aspect_ratio)
        letter_img = letter_img.resize((target_width, line_height))

        # Check if the letter fits in the current line
        if x + target_width > canvas_width:
            x = margin_x  # Reset x for the new line, start with margin
            y += line_spacing  # Move to the next line

            # Stop if the canvas height is exceeded
            if y + line_height > canvas_height:
                print("Text exceeds the canvas height!")
                break

        # Adjust y position for specific letters
        y_offset = letter_offsets.get(char, 0) if char.islower() else 0
        canvas.paste(letter_img, (x, y + y_offset), mask=letter_img)

        # Update x position without adding extra spacing
        x += target_width

# Show or save the result
canvas.show()
canvas.save("handwritten_text_with_offsets.png", format="PNG")
