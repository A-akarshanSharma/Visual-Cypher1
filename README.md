# Visual Cypher

Visual Cypher is an educational image encryption and decryption project based on a Rubik's Cube-inspired transformation process.

The project applies row shifting, column shifting, XOR-based pixel transformations, and bit rotations to RGB images. A generated key containing the required transformation vectors is used to reverse the process and recover the original image.

It includes a browser-based interface, a Python command-line interface, automated testing, and Docker support.

## Features

- 🔐 Rubik's Cube-inspired image encryption
- 🔓 Image decryption using the generated key
- 🖼️ Browser-based interface
- 💻 Python CLI
- 🔑 Automatic encryption-key generation
- 🧪 Pixel-level encryption/decryption verification
- 🐳 Docker support
- 📦 Pinned Python dependency management

## How It Works

The image is converted into an RGB NumPy array.

### 1. Key Generation

Two key vectors are generated:

- `Kr` — row-related key values
- `Kc` — column-related key values

The generated key also stores `iter_max`. The key is serialized as JSON and Base64 encoded before being stored.

### 2. Row Rolling

Image rows are shifted using NumPy rolling operations. The direction depends on the parity of the RGB channel values.

### 3. Column Shifting

Image columns are shifted using the generated key and channel parity. The shifts are reversed during decryption.

### 4. XOR Pixel Transformation

Each RGB pixel is transformed using XOR operations derived from `Kr` and `Kc`. Selected key values also undergo a 180-degree bit rotation.

### 5. Iteration

The transformation sequence is repeated according to `iter_max`.

Encryption:

```text
Row Rolling
     ↓
Column Shifting
     ↓
XOR Pixel Transformation
     ↓
Repeat
```

Decryption reverses the transformation order:

```text
XOR Pixel Transformation
     ↓
Reverse Column Shifting
     ↓
Reverse Row Rolling
     ↓
Repeat
```

## Web Application

The web interface is built with HTML, CSS, JavaScript, and PyScript.

It allows users to upload images, encrypt them, generate/download the encryption key, and decrypt an encrypted image using its key.

The web application is located in:

```text
webapp/
```

## Running Locally

### Requirements

- Python 3.12+
- pip

### Install

```bash
git clone https://github.com/A-akarshanSharma/Visual-Cypher1.git
cd Visual-Cypher1
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Web Application

```bash
python -m http.server 8000 --directory webapp
```

Open:

```text
http://localhost:8000
```

## Command-Line Interface

The project also provides `crypto_client.py`.

### Encryption

Windows PowerShell:

```powershell
python crypto_client.py --type encrypt --image examples/test-image.jpg --alpha 8 --iter_max 1 --key key.txt --output_image encrypted.png
```

Linux/macOS:

```bash
python crypto_client.py \
  --type encrypt \
  --image examples/test-image.jpg \
  --alpha 8 \
  --iter_max 1 \
  --key key.txt \
  --output_image encrypted.png
```

### Decryption

Windows PowerShell:

```powershell
python crypto_client.py --type decrypt --image encrypted.png --key key.txt --output_image decrypted.png
```

Linux/macOS:

```bash
python crypto_client.py \
  --type decrypt \
  --image encrypted.png \
  --key key.txt \
  --output_image decrypted.png
```

### CLI Arguments

| Argument | Description |
|---|---|
| `--type` | `encrypt` or `decrypt` |
| `--image` | Input image path |
| `--alpha` | Key-generation parameter used during encryption |
| `--iter_max` | Number of transformation iterations |
| `--key` | Key file to store or load |
| `--output_image` | Output image path |

`--alpha` and `--iter_max` are required for encryption.

## Docker

Docker provides a reproducible way to run the web application without installing the Python dependency manually on the host.

### Build

```bash
docker build -t visual-cypher .
```

### Run

```bash
docker run --rm -p 8000:8000 visual-cypher
```

Open:

```text
http://localhost:8000
```

The Docker image uses `python:3.12-slim`, installs dependencies from `requirements.txt`, and serves the `webapp` directory with Python's built-in HTTP server.

## Testing

The project includes an encryption/decryption test:

```text
tests/test_encryption.py
```

Run:

```bash
python tests/test_encryption.py
```

The test:

1. Loads the sample image.
2. Encrypts it.
3. Retrieves the generated key.
4. Decrypts the encrypted image.
5. Converts both images to NumPy arrays.
6. Verifies that the original and decrypted pixel data are identical.

The verification uses:

```python
np.array_equal(original_array, decrypted_array)
```

Example output:

```text
Running Visual Cypher encryption test...

✓ Image loaded
✓ Encryption completed
✓ Decryption completed
✓ Original and decrypted images are identical

All tests passed!
```

## Project Structure

```text
Visual-Cypher1/
│
├── examples/
│   └── test-image.jpg
│
├── rubikencryptor/
│   ├── __init__.py
│   └── rubikencryptor.py
│
├── tests/
│   └── test_encryption.py
│
├── webapp/
│   ├── assets/
│   │   ├── icons/
│   │   │   └── rubik.ico
│   │   └── imgs/
│   │       ├── background.jpg
│   │       ├── image.jpg
│   │       └── placeholder.png
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   ├── pyscript/
│   │   ├── image_crypto.py
│   │   └── pyscript.toml
│   └── index.html
│
├── crypto_client.py
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```

## Technology Stack

**Algorithm / Python**
- Python
- NumPy
- Pillow

**Web**
- HTML5
- CSS3
- JavaScript
- PyScript

**Development / Deployment**
- Git
- Docker
- Docker Desktop

## Configuration

### Alpha

`alpha` controls the range used when generating key-vector values.

For example:

```text
alpha = 8
```

produces values from:

```text
0 → 255
```

### Iterations

`iter_max` controls how many times the transformation sequence is applied.

```text
iter_max = 1
```

performs one complete transformation cycle.

Higher values increase computation time.

## Encryption Key

A generated key contains:

```json
{
    "Kr": [...],
    "Kc": [...],
    "iter_max": 1
}
```

The key is serialized and Base64 encoded before being written to the key file.

**Keep the generated key safe. It is required to decrypt the corresponding encrypted image.**

Generated files such as `key.txt` and `test_key.txt` are excluded from version control through `.gitignore`.

## Limitations

Visual Cypher is an educational and experimental project demonstrating image transformation and encryption concepts.

It should **not be considered a replacement for established cryptographic algorithms or modern cryptographic standards**.

The implementation uses a custom transformation scheme intended for learning, experimentation, and demonstration.

## Future Improvements

- Improve encryption/decryption performance
- Add better progress feedback for large images
- Expand automated test coverage
- Improve web application error handling
- Add additional image-format support
- Add benchmarking
- Further separate the encryption library from the web interface

## License

This project is available for educational and personal use.

See the repository for the current licensing information.
