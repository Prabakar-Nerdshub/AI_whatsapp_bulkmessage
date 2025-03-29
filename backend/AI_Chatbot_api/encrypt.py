import os
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key

# Load RSA public key
PUBLIC_KEY_PATH = "D:/meta_api_implement/backend/AI_Chatbot_api/public.pem"

def load_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as key_file:
        return load_pem_public_key(key_file.read())

PUBLIC_KEY = load_public_key()

def encrypt_data(plaintext_json):
    # Ensure JSON string format
    plaintext = json.dumps(plaintext_json) if isinstance(plaintext_json, dict) else plaintext_json

    # Generate AES key and IV
    aes_key = os.urandom(32)  # AES-256 key
    iv = os.urandom(12)  # IV for GCM mode

    print(f"✅ IV Length: {len(iv)} bytes (Should be 12)")

    # Encrypt data using AES-GCM
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(plaintext.encode()) + encryptor.finalize()

    # Append authentication tag
    encrypted_payload = encrypted_data + encryptor.tag

    # Encrypt AES key using RSA-OAEP
    encrypted_aes_key = PUBLIC_KEY.encrypt(
        aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    # Encode in Base64
    return json.dumps({
        "encrypted_flow_data": base64.b64encode(encrypted_payload).decode(),
        "encrypted_aes_key": base64.b64encode(encrypted_aes_key).decode(),
        "initial_vector": base64.b64encode(iv).decode()
    })

# Example usage
json_payload = encrypt_data({"message": "Hello, this is secure data!"})
print("📩 Encrypted JSON Payload:", json_payload)
