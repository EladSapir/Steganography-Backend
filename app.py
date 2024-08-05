from flask import Flask
from flask_cors import CORS
from controllers import encode_controller, decode_controller

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(encode_controller.bp)
app.register_blueprint(decode_controller.bp)

if __name__ == '__main__':
    app.run(debug=True)
