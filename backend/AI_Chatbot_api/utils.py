import json
from base64 import b64encode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def encrypt_flow_response(response_payload, aes_key, iv):
    """
    Encrypts the response payload using AES-GCM with the given AES key and IV.

    WhatsApp flips the IV bytes before encryption, so we do the same.
    """

    # Flip IV by XOR-ing with 0xFF (used by WhatsApp)
    flipped_iv = bytearray([b ^ 0xFF for b in iv])

    # Set up the AES-GCM cipher
    encryptor = Cipher(
        algorithms.AES(aes_key),
        modes.GCM(bytes(flipped_iv))
    ).encryptor()

    # Convert response to JSON bytes
    payload_bytes = json.dumps(response_payload).encode("utf-8")

    # Encrypt the payload
    ciphertext = encryptor.update(payload_bytes) + encryptor.finalize()

    # Append GCM tag to ciphertext
    encrypted_output = ciphertext + encryptor.tag

    # Return Base64-encoded string
    return b64encode(encrypted_output).decode("utf-8")
