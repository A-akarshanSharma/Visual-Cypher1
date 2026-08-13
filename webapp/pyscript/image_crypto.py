from rubikencryptor.rubikencryptor import RubikCubeCrypto
from PIL import Image
from io import BytesIO
import base64
from pyscript import when, document


def set_status(message):
    status = document.getElementById("status-message")

    if status:
        status.innerText = message


def set_transform_state(disabled, text):
    button = document.getElementById("transform-img-btn")

    if button:
        button.disabled = disabled
        button.innerText = text


@when("click", "#transform-img-btn")
def click_handler(event):
    action = document.getElementById("transform-img-btn").innerText

    if action == "Encrypt":
        set_transform_state(True, "Encrypting...")
        set_status("Encrypting image... Please wait.")
        encrypt_image()

    elif action == "Decrypt":
        set_transform_state(True, "Decrypting...")
        set_status("Decrypting image... Please wait.")
        decrypt_image()


def encrypt_image():
    try:
        set_transform_state(True, "Encrypting...")
        set_status("Encrypting image... Please wait.")

        image_prefix, image_data = (
            document.getElementById("input-img")
            .src
            .split("base64,")
        )

        image_bytes = base64.b64decode(image_data)

        input_image = Image.open(BytesIO(image_bytes))

        encryptor = RubikCubeCrypto(input_image)

        encrypted_image = encryptor.encrypt(
            alpha=8,
            iter_max=1
        )

        output_buffer = BytesIO()

        encrypted_image.save(
            output_buffer,
            format=input_image.format
        )

        encoded_image = base64.b64encode(
            output_buffer.getvalue()
        ).decode("utf-8")

        document.getElementById("output-img").src = (
            image_prefix + "base64," + encoded_image
        )

        document.getElementById("crypto-key").innerText = (
            str(encryptor.encoded_key)
        )

        document.getElementById(
            "img-key-downloader"
        ).style.display = "flex"

        set_status("Encryption completed successfully.")

    except Exception as error:
        print(error)
        set_status("Encryption failed. Please check your image.")

    finally:
        set_transform_state(False, "Encrypt")


def decrypt_image():
    try:
        set_transform_state(True, "Decrypting...")
        set_status("Decrypting image... Please wait.")

        image_prefix, image_data = (
            document.getElementById("input-img")
            .src
            .split("base64,")
        )

        image_bytes = base64.b64decode(image_data)

        input_image = Image.open(BytesIO(image_bytes))

        decryptor = RubikCubeCrypto(input_image)

        key_text = document.getElementById(
            "crypto-key"
        ).textContent.strip()

        if not key_text:
            raise ValueError("No encryption key provided.")

        # Convert the stored key representation back to bytes
        key_bytes = bytes(
            int(value)
            for value in key_text.strip("[]").split(",")
            if value.strip()
        )

        decrypted_image = decryptor.decrypt_with_key(
            key_bytes
        )

        output_buffer = BytesIO()

        decrypted_image.save(
            output_buffer,
            format=input_image.format
        )

        encoded_image = base64.b64encode(
            output_buffer.getvalue()
        ).decode("utf-8")

        document.getElementById("output-img").src = (
            image_prefix + "base64," + encoded_image
        )

        set_status("Decryption completed successfully.")

    except Exception as error:
        print(error)
        set_status(
            "Decryption failed. Please check the image and key."
        )

    finally:
        set_transform_state(False, "Decrypt")