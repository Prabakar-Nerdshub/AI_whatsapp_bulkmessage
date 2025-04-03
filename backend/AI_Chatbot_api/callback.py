from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import os

PRIVATE_KEY = os.environ.get('PRIVATE_KEY')

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        return handle_post_request(request)
    elif request.method == "GET":
        return handle_get_request(request)
    else:
        return HttpResponse("Method Not Allowed", status=405)

def handle_post_request(request):
    try:
        # Parse the incoming JSON body
        body = json.loads(request.body)
        
        # Extract the encrypted data from the request
        encrypted_flow_data_b64 = body.get('encrypted_flow_data')
        encrypted_aes_key_b64 = body.get('encrypted_aes_key')
        iv_b64 = body.get('initial_vector')

        if not all([encrypted_flow_data_b64, encrypted_aes_key_b64, iv_b64]):
            return HttpResponse("Bad Request", status=400)

        # Decrypt the incoming data
        decrypted_data, aes_key, iv = decrypt_request(
            encrypted_flow_data_b64, encrypted_aes_key_b64, iv_b64)
        
        print(decrypted_data)

        # Create a response to send back to Meta
        response = {"data": {"status": "active"}}

        # Encrypt the response and return it to Meta
        encrypted_response = encrypt_response(response, aes_key, iv)
        return HttpResponse(encrypted_response, content_type="text/plain", status=200)

    except Exception as e:
        print(f"Error: {e}")
        return HttpResponse("Internal Server Error", status=500)

def handle_get_request(request):
    # This can be a health check or status request
    return JsonResponse({"status": "ok"}, status=200)

def decrypt_request(encrypted_flow_data_b64, encrypted_aes_key_b64, iv_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(iv_b64)

    # Decrypt the AES encryption key using your private RSA key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    private_key_path = 'D:/meta_api_implement/backend/AI_Chatbot_api/pem_file/new_private.pem'

    # Correct indentation here
    with open(private_key_path, 'rb') as key_file:
        private_key = load_pem_private_key(key_file.read(), password=None)
    
    aes_key = private_key.decrypt(
        encrypted_aes_key, OAEP(mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    # Decrypt the flow data (AES-GCM)
    encrypted_flow_data_body = flow_data[:-16]
    encrypted_flow_data_tag = flow_data[-16:]
    decryptor = Cipher(algorithms.AES(aes_key), modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))

    return decrypted_data, aes_key, iv

def encrypt_response(response, aes_key, iv):
    # Flip the initialization vector (XOR each byte with 0xFF)
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response using the AES key and flipped IV
    encryptor = Cipher(algorithms.AES(aes_key), modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")
