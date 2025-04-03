from base64 import b64decode
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key

# ✅ Define the private key path & passphrase
private_key_path = r"D:/meta_api_implement/backend/AI_Chatbot_api/pem_file/new_private.pem"
passphrase = "Nerdshub@123"

# ✅ Full encrypted AES key
encrypted_aes_key_b64 = (
    "yP07EhILTYC4Kl4gwd3V9fRaAg7E7hcGIY21OOAyK2YIXYBn6CnkU/rhyzMe90yzkUubbL83IG2XUip5AfN22b1rGZJPKwLi+"
    "ABRwIUE/9GAZWqE4riBKWXhzo3XKYNDjsx+LU0SepzelcohAeoeMLky/Oc9em24vps0snUriRXEsjWlAHZKqTqOyDHHN2x58ssi"
    "IjHfe7h4/gDEAneG09MuUweKP88MI8VpZfX8lCEemP2mlU7ZjtDsIdiOM1lac99Fr8fIHtqV0eGwXVz5eHk0uSbAv75gG/SLxus"
    "jRafWpPoVlDVBgaHcBfb3IpHXh+jealOA1hSY3eQrvYXEIw=="
)

try:
    # ✅ Load the RSA Private Key
    with open(private_key_path, "rb") as key_file:
        private_key = load_pem_private_key(key_file.read(), passphrase.encode())

    # ✅ Decode Base64
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print(f"🔹 Encrypted AES Key Length: {len(encrypted_aes_key)} bytes")

    # ✅ Decrypt AES Key using RSA
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        OAEP(
            mgf=MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # ✅ Check AES Key Length (Should be 32 bytes for AES-256)
    print(f"✅ Decrypted AES Key: {aes_key.hex()} (Length: {len(aes_key)} bytes)")
    if len(aes_key) != 32:
        print("❌ Warning: AES Key length is incorrect! Expected 32 bytes (256 bits).")

except Exception as e:
    print(f"❌ Error: {e}")
