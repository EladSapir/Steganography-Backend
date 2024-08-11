
# Steganography Tool Backend

This is the backend service for the Steganography Tool, which provides APIs to encode and decode images with watermarks using LSB (Least Significant Bit) steganography.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Encode text watermarks into images.
- Decode text watermarks from images.

## Requirements

- Python 3.8+
- Flask
- Flask-CORS

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/steganography-backend.git
    cd steganography-backend
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Environment Variables

Create a `.env` file in the root directory and set the following variables:

```
FLASK_APP=app.py
FLASK_ENV=development
```

## Running the Application

To start the development server, run:

```bash
flask run
```

The server will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Encode

- **URL:** `/encode`
- **Method:** `POST`
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `image`: The image file to encode.
  - `text`: The text to encode into the image.
- **Response:** Returns the encoded image as a binary blob.

### Decode

- **URL:** `/decode`
- **Method:** `POST`
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `image`: The image file to decode.
- **Response:** Returns a JSON object with the decoded watermark text.

## Usage

### Encode a Watermark

```bash
curl -X POST -F "image=@/path/to/your/image.png" -F "text=Your watermark text" http://127.0.0.1:5000/encode --output encoded_image.png
```

### Decode a Watermark

```bash
curl -X POST -F "image=@/path/to/your/encoded_image.png" http://127.0.0.1:5000/decode
```

## Contributing

Contributions are welcome! Please read the contributing guidelines first.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
