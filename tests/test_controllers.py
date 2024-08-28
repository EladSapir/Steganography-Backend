import unittest
import cv2
import sys
import os
import numpy as np
from flask import Flask
from controllers.encode_controller import bp as encode_bp
from controllers.decode_controller import bp as decode_bp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class SteganographyControllerTest(unittest.TestCase):
    
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(encode_bp)
        self.app.register_blueprint(decode_bp)
        self.client = self.app.test_client()

        # Paths to provided images and expected results
        self.image_to_encode_path = 'tests/carrier.png'  # Carrier image path
        self.hidden_image_path = 'tests/hidden_image.png'  # Hidden image path
        self.text_to_encode = 'Elad and Solal Steganography'  # Text to encode
        self.expected_encoded_text_image_path = 'tests/text_in_image.png'
        self.expected_encoded_image_image_path = 'tests/image_in_image.png'
        self.expected_hidden_image_path = 'tests/hidden_image.png'  # Expected extracted image

    def compare_images(self, image1_path, image2_path):
        image1 = cv2.imread(image1_path)
        image2 = cv2.imread(image2_path)
        # Compare the images
        return np.array_equal(image1, image2)

    def test_encode_text(self):
        with open(self.image_to_encode_path, 'rb') as img:
            data = {
                'image': (img, 'carrier_image.png'),
                'text': self.text_to_encode
            }
            response = self.client.post('/encode', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'image/png')
            
            # Save encoded image for comparison
            encoded_image_path = 'tests/encoded_with_text.png'
            with open(encoded_image_path, 'wb') as f:
                f.write(response.data)
            
            # Compare the encoded image with the expected image
            self.assertTrue(self.compare_images(encoded_image_path, self.expected_encoded_text_image_path))

    def test_decode_text(self):
        with open(self.expected_encoded_text_image_path, 'rb') as encoded_img:
            decode_data = {
                'image': (encoded_img, 'encoded_image.png'),
                'mode': 'text'
            }
            decode_response = self.client.post('/decode', data=decode_data, content_type='multipart/form-data')
            self.assertEqual(decode_response.status_code, 200)
            self.assertIn('watermark', decode_response.json)
            self.assertEqual(decode_response.json['watermark'], self.text_to_encode)
    
    def test_encode_image(self):
        with open(self.image_to_encode_path, 'rb') as carrier_img, open(self.hidden_image_path, 'rb') as hidden_img:
            data = {
                'image': (carrier_img, 'carrier_image.png'),
                'hiddenImage': (hidden_img, 'hidden_image.png')
            }
            response = self.client.post('/encode', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'image/png')
            
            # Save encoded image for comparison
            encoded_image_path = 'tests/encoded_with_image.png'
            with open(encoded_image_path, 'wb') as f:
                f.write(response.data)
            
            # Compare the encoded image with the expected image
            self.assertTrue(self.compare_images(encoded_image_path, self.expected_encoded_image_image_path))
    
    def test_decode_image(self):
        with open(self.expected_encoded_image_image_path, 'rb') as encoded_img:
            decode_data = {
                'image': (encoded_img, 'encoded_image.png'),
                'mode': 'image'
            }
            decode_response = self.client.post('/decode', data=decode_data, content_type='multipart/form-data')
            self.assertEqual(decode_response.status_code, 200)
            self.assertEqual(decode_response.content_type, 'image/png')
            
            # Save decoded image for comparison
            decoded_image_path = 'tests/decoded_hidden_image.png'
            with open(decoded_image_path, 'wb') as f:
                f.write(decode_response.data)
            
            # Compare the decoded image with the expected hidden image
            self.assertTrue(self.compare_images(decoded_image_path, self.expected_hidden_image_path))

if __name__ == '__main__':
    unittest.main()
