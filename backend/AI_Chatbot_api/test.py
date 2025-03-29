import hashlib
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64

# Load private key
with open(r"D:\meta_api_implement\backend\AI_Chatbot_api\private.pem", "rb") as f:
    private_key = RSA.import_key(f.read())

# Initialize cipher with correct padding
cipher_rsa = PKCS1_OAEP.new(private_key)
aes_key = b'3284a87cb4320c0498d33cda0f58f490ebdd202bc1d20f19e83a8a6a43a7d36e'

# Encrypt AES key using RSA
encrypted_aes_key = cipher_rsa.encrypt(aes_key)
hash_value = hashlib.sha256(encrypted_aes_key).hexdigest()

print(f"🔍 SHA-256 Hash of Encrypted AES Key: {hash_value}")

# Save encrypted key to file
with open("encrypted_aes_key.bin", "wb") as f:
    f.write(encrypted_aes_key)
