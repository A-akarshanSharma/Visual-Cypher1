from pathlib import Path
import sys

import numpy as np
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from rubikencryptor.rubikencryptor import RubikCubeCrypto

TEST_IMAGE = BASE_DIR / "examples" / "test-image.jpg"


def main():
    print("Running Visual Cypher encryption test...\n")

    # Load original image
    original = Image.open(TEST_IMAGE)
    print("✓ Image loaded")

    # Encrypt
    encryptor = RubikCubeCrypto(original)
    encrypted = encryptor.encrypt(alpha=8, iter_max=1)
    print("✓ Encryption completed")

    # Decrypt using the generated key
    decryptor = RubikCubeCrypto(encrypted)
    decrypted = decryptor.decrypt_with_key(encryptor.encoded_key)
    print("✓ Decryption completed")

    # Compare pixel data
    original_array = np.array(original)
    decrypted_array = np.array(decrypted)

    if np.array_equal(original_array, decrypted_array):
        print("✓ Original and decrypted images are identical")
        print("\nAll tests passed!")
    else:
        print("✗ Original and decrypted images are NOT identical")
        raise AssertionError("Encryption/decryption test failed")


if __name__ == "__main__":
    main()