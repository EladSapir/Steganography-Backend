from flask import Blueprint, request, send_file
import cv2
import numpy as np
import io
from models.steganography import LSBSteg

bp = Blueprint('encode', __name__)

@bp.route('/encode', methods=['POST'])
def encode():
    image_file = request.files['image']
    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    steg = LSBSteg(image)
    
    if 'text' in request.form:
        watermark_text = request.form['text']
        print(f"Received image: {image_file.filename}")
        print(f"Watermark text: {watermark_text}")
        result = steg.encode_text(watermark_text)
    elif 'hiddenImage' in request.files:
        hidden_image_file = request.files['hiddenImage']
        hidden_image = cv2.imdecode(np.frombuffer(hidden_image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        print(f"Received image to hide: {hidden_image_file.filename}")
        result = steg.encode_image(hidden_image)
    else:
        return "No valid data provided for encoding", 400

    _, encoded_image = cv2.imencode('.png', result)
    return send_file(
        io.BytesIO(encoded_image.tobytes()),
        mimetype='image/png',
        as_attachment=True,
        download_name='encoded_image.png'
    )
