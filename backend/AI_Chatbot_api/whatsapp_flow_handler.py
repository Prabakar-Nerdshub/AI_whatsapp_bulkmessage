from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from .views import send_whatsapp_message

# Load the RSA private key from a file
PRIVATE_KEY_PATH = 'D:/meta_api_implement/backend/AI_Chatbot_api/pem_file/new_private.pem'

responses = {
    "0_Semak_Bantuan": "Anda telah memilih Semak Bantuan. Sila tunggu sebentar.",
    "1_Senarai_Pasaraya": "Berikut adalah senarai pasaraya yang mengambil bahagian: [Link]",
    "2_Program_SARA": "Maklumat mengenai Program SARA boleh didapati di sini: [Link]",
    "3_Cara_Tebus_Bantuan": "Ikuti langkah ini untuk menebus bantuan: [Link]",
    "4_Mewakilkan_Ahli_Keluarga": "Maklumat lanjut mengenai mewakilkan ahli keluarga: [Link]",
    "5_Barang_Bantuan": "Barang bantuan yang tersedia: [List]",
    "6_Jumlah_Bantuan": "Jumlah bantuan yang boleh anda terima adalah bergantung kepada kelayakan anda.",
    "7_Waktu_Tebus_Bantuan": "Anda boleh menebus bantuan dalam waktu berikut: [Time]",
    "8__Hubungi_Kami": "Sila hubungi kami di nombor berikut: +60123456789",
    "9__IC_Hilang_/_Rosak": "Sekiranya IC anda hilang atau rosak, sila rujuk kepada Jabatan Pendaftaran Negara."
}

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        return handle_post_request(request)
    elif request.method == "GET":
        return JsonResponse({"status": "ok"}, status=200)
    else:
        return HttpResponse("Method Not Allowed", status=405)

def handle_post_request(request):
    try:
        body = json.loads(request.body)

        # Extract encrypted fields from the request
        encrypted_flow_data_b64 = body.get("encrypted_flow_data")
        encrypted_aes_key_b64 = body.get("encrypted_aes_key")
        iv_b64 = body.get("initial_vector")

        if not all([encrypted_flow_data_b64, encrypted_aes_key_b64, iv_b64]):
            return JsonResponse({"error": "Missing encryption fields"}, status=400)

        # Decrypt the request data
        decrypted_data, aes_key, iv = decrypt_request(encrypted_flow_data_b64, encrypted_aes_key_b64, iv_b64)
        print("Decrypted Data:", json.dumps(decrypted_data, indent=2))
        # Extract necessary fields
        action = decrypted_data.get("action")
        flow_token = "flows-builder-7797319f"
        print(action)
        if action == "INIT":
            response_payload = {                
                "screen": "DETAILS",
                "data": {}
            }

        elif action == "data_exchange":
            screen_id = decrypted_data.get("screen")
            user_selection = decrypted_data.get("data", {}).get("selected_option")  # Extract selected option
            print(user_selection)
            
            # Get predefined response
            response_message = responses.get(user_selection, "Pilihan tidak sah.")  # Default message if not found
            print(response_message)

            # ✅ Send WhatsApp message
            send_whatsapp_message({"contacts": [{"phone_numbers": decrypted_data.get("user_phone")}], "template_name": response_message, "language_code": "ms"})
            print(send_whatsapp_message)

            response_payload = {
                "screen": "SUCCESS",
                "data": {
                    "extension_message_response": {
                        "params": {
                            "flow_token": flow_token,
                            "response_message": response_message  # Send predefined response
                        }
                    }
                }
            }


        elif action == "BACK":
            response_payload = {
                "screen": "DETAILS",
                "data": {}
            }

        else:
            response_payload = {"data": {"status": "active"}}

        # Encrypt the response before sending it back
        encrypted_response = encrypt_response(response_payload, aes_key, iv)
        return HttpResponse(encrypted_response, content_type="text/plain", status=200)

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)
 

def decrypt_request(encrypted_flow_data_b64, encrypted_aes_key_b64, iv_b64):
    """
    Decrypts the request payload from Meta using RSA and AES-GCM.
    """
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(iv_b64)

    # Load RSA private key
    with open(PRIVATE_KEY_PATH, 'rb') as key_file:
        private_key = load_pem_private_key(key_file.read(), password=None)
    
    # Decrypt AES key using RSA private key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    aes_key = private_key.decrypt(
        encrypted_aes_key, 
        OAEP(mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    # Decrypt flow data using AES-GCM
    encrypted_flow_data_body = flow_data[:-16]
    encrypted_flow_data_tag = flow_data[-16:]
    decryptor = Cipher(algorithms.AES(aes_key), modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))

    return decrypted_data, aes_key, iv

def encrypt_response(response, aes_key, iv):
    """
    Encrypts the response payload using AES-GCM.
    """
    # Flip IV for response encryption
    flipped_iv = bytearray([byte ^ 0xFF for byte in iv])

    # Encrypt response using AES-GCM
    encryptor = Cipher(algorithms.AES(aes_key), modes.GCM(flipped_iv)).encryptor()
    encrypted_bytes = encryptor.update(json.dumps(response).encode("utf-8")) + encryptor.finalize() + encryptor.tag

    return b64encode(encrypted_bytes).decode("utf-8") 
