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
    
    if request.form.get('mode') == 'text':
        watermark_text = steg.decode_text()
        return {'watermark': watermark_text}
    elif request.form.get('mode') == 'image':
        hidden_image = steg.decode_image()
        _, decoded_image = cv2.imencode('.png', hidden_image)
        return send_file(
            io.BytesIO(decoded_image.tobytes()),
            mimetype='image/png',
            as_attachment=True,
            download_name='hidden_image.png'
        )
    else:
        return "No valid mode provided for decoding", 400
