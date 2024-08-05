from flask import Blueprint, request, send_file
import cv2
import numpy as np
import io
from models.steganography import LSBSteg

bp = Blueprint('encode', __name__)

@bp.route('/encode', methods=['POST'])
def encode():
    image_file = request.files['image']
    watermark_text = request.form['text']
    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    steg = LSBSteg(image)
    result = steg.encode_text(watermark_text)
    _, encoded_image = cv2.imencode('.png', result)
    return send_file(
        io.BytesIO(encoded_image.tobytes()),
        mimetype='image/png',
        as_attachment=True,
        download_name='encoded_image.png'
    )
