from django.http import JsonResponse, HttpResponse
import json
import base64
import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)

# Replace with your actual WhatsApp API secret key
WHATSAPP_API_SECRET = b"75a30aaa275d9f4f52992247f2027478"

def decrypt_data(encrypted_data, encrypted_key, iv):
    """Decrypts WhatsApp webhook data"""
    try:
        aes_key = base64.b64decode(encrypted_key)
        iv = base64.b64decode(iv)
        encrypted_data = base64.b64decode(encrypted_data)

        # 🔹 Validate AES key length
        if len(aes_key) not in (16, 24, 32):  # Valid AES key sizes
            logger.error(f"Invalid AES key size: {len(aes_key)} bytes")
            return None

        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted_data) + decryptor.finalize()

        return json.loads(decrypted.decode("utf-8").rstrip("\x00"))  # Remove padding
    except Exception as e:
        logger.error(f"Decryption error: {str(e)}")
        return None



@csrf_exempt
def webhook(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            encrypted_flow_data = payload.get("encrypted_flow_data")
            encrypted_aes_key = payload.get("encrypted_aes_key")
            initial_vector = payload.get("initial_vector")

            decrypted_request = decrypt_data(encrypted_flow_data, encrypted_aes_key, initial_vector)

            if not decrypted_request:
                return JsonResponse({"error": "Failed to decrypt data"}, status=400)

            action = decrypted_request.get("action")
            screen = decrypted_request.get("screen")

            return JsonResponse({"status": "success", "action": action, "screen": screen}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return HttpResponse("Invalid request", status=400)
