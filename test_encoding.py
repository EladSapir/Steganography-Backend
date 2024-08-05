import cv2
import numpy as np
from models.steganography import LSBSteg

def main():
    image_path = 'dog.jpg'
    output_path = 'encodedDog.jpg'
    watermark_text = 'Your watermark text'

    # Read the image
    image = cv2.imread(image_path)
    steg = LSBSteg(image)

    # Encode the text
    encoded_image = steg.encode_text(watermark_text)

    # Save the encoded image
    cv2.imwrite(output_path, encoded_image)
    print(f"Encoded image saved to {output_path}")

    # Decode the text
    steg = LSBSteg(encoded_image)
    decoded_text = steg.decode_text()
    print(f"Decoded text: {decoded_text}")

if __name__ == '__main__':
    main()
