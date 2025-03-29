import os
import json
import base64
from dotenv import load_dotenv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# Retrieve AES key from environment variable
AES_SECRET_KEY_B64 = os.getenv("AES_SECRET_KEY")
if not AES_SECRET_KEY_B64:
    raise ValueError("Missing AES_SECRET_KEY in environment variables.")

try:
    AES_SECRET_KEY = base64.b64decode(AES_SECRET_KEY_B64)
    if len(AES_SECRET_KEY) not in [16, 24, 32]:
        raise ValueError(f"Invalid AES Key: Must be 16, 24, or 32 bytes, got {len(AES_SECRET_KEY)} bytes.")
except Exception as e:
    raise ValueError(f"Invalid AES_SECRET_KEY format: {str(e)}")

def encrypt_data(data, key):
    """Encrypts data using AES-GCM."""
    iv = os.urandom(12)  # Generate a 12-byte IV for AES-GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    encryptor = cipher.encryptor()

    encrypted_data = encryptor.update(json.dumps(data).encode()) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_data + encryptor.tag).decode()

def decrypt_data(encrypted_b64, key):
    """Decrypts AES-GCM encrypted data."""
    try:
        encrypted_bytes = base64.b64decode(encrypted_b64)
        iv, encrypted_body, tag = encrypted_bytes[:12], encrypted_bytes[12:-16], encrypted_bytes[-16:]

        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()

        decrypted_data = decryptor.update(encrypted_body) + decryptor.finalize()
        return json.loads(decrypted_data.decode("utf-8"))

    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")

# Example usage
if __name__ == "__main__":
    sample_data = {"message": "Hello, AES-GCM Encryption!"}

    encrypted_text = encrypt_data(sample_data, AES_SECRET_KEY)
    print("Encrypted:", encrypted_text)

    decrypted_text = decrypt_data(encrypted_text, AES_SECRET_KEY)
    print("Decrypted:", decrypted_text)
