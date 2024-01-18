from PIL import Image

def process_image(input_path, output_path):
    # Open the image
    image = Image.open(input_path)

    # Get the width and height of the image
    width, height = image.size

    # Loop through each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the pixel value
            pixel = image.getpixel((x, y))

            # Check if the pixel is not rgb(127,127,127)
            if pixel[:3] not in [(127, 127, 127),(72,71,68),(88,89,91),(100,101,103),(53,57,61),(55,58,61)]:
                # Set the pixel to white
                image.putpixel((x, y), (255, 255, 255) + pixel[3:])  # Preserve additional channels if any

    # Convert the image to RGB before saving
    image = image.convert("RGB")

    # Save the modified image
    image.save(output_path)

# Example usage
input_image_path = "imgs/100.png"
output_image_path = "output_image.jpg"
process_image(input_image_path, output_image_path)
