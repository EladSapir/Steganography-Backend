from flask import Blueprint, request
import cv2
import numpy as np
from models.steganography import LSBSteg

bp = Blueprint('decode', __name__)

@bp.route('/decode', methods=['POST'])
def decode():
    image_file = request.files['image']
    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    steg = LSBSteg(image)
    watermark_text = steg.decode_text()
    return {'watermark': watermark_text}
