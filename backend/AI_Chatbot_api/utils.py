import os
import json
import base64
from dotenv import load_dotenv
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# Load RSA Private Key for AES decryption
RSA_PRIVATE_KEY_PATH = os.getenv("RSA_PRIVATE_KEY_PATH")


if not RSA_PRIVATE_KEY_PATH or not os.path.exists(RSA_PRIVATE_KEY_PATH):
    raise ValueError(f"Missing or invalid RSA_PRIVATE_KEY_PATH: {RSA_PRIVATE_KEY_PATH}")

with open(RSA_PRIVATE_KEY_PATH, "rb") as key_file:
    PRIVATE_KEY = serialization.load_pem_private_key(
        key_file.read(),
        password=None  # Add password if needed
    )

   # encrypted_aes_key = "odhlUnRcn9ANMLTloIgxkzjefYmNr2pThF672hsEnfA4ye8xzgO0/h5WeXAH3DgGTJ8fgiJeSJvv3Kv/CBusf/N4qqJ+BdcngIENpeQrda9JHpVNlSyLYUhOYbsbV0mcbllM+YUlWeaH70Kj5UOwui3i/vDxYbGdhN7CO7V2vcy1xHAovUjFdhOrBAW9P5cAWOohq5FOWTD7s7MW1mlpA1YryA+qyr5PdjtHdOBu4aq7ICmiyF7l5HvPd6dVIi4vLT0NLB/7UOOa0hD2B7nE2Z595N/ki9Vx1LeGp7jC07EohchPqZ4i4hjSPFVFUBxHCvDAFEL3qQiNWzVEL4x7VQ=="

def decrypt_aes_key(encrypted_aes_key):
    """Decrypts AES key using RSA Private Key."""
    print(f"Provate Kye path is: {RSA_PRIVATE_KEY_PATH}")
    try:
        decrypted_aes_key = PRIVATE_KEY.decrypt(
            base64.b64decode(encrypted_aes_key),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_aes_key
    except Exception as e:
        raise ValueError(f"RSA decryption failed: {str(e)}")

def encrypt_data(data, key):
    """Encrypts data using AES-GCM."""
    iv = os.urandom(12)  # Generate a 12-byte IV
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
