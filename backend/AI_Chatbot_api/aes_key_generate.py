import os
import base64

def generate_aes_key(key_size=32):
    """Generates a valid AES key of 16, 24, or 32 bytes and encodes it in Base64."""
    if key_size not in [16, 24, 32]:
        raise ValueError("AES key size must be 16, 24, or 32 bytes.")
    
    key = os.urandom(key_size)
    encoded_key = base64.b64encode(key).decode()
    
    print("New AES Key (Base64):", encoded_key)
    return encoded_key

# Generate a 32-byte AES key (AES-256)
generate_aes_key(32)
