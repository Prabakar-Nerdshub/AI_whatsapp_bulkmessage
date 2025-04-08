import base64
import json
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad, pad
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .views import send_whatsapp_message  # Your custom message sender function

# Load your private key for decrypting AES key
with open(r'D:/meta_api_implement/backend/AI_Chatbot_api/pem_file/new_private.pem', "rb") as f:
    PRIVATE_KEY = RSA.import_key(f.read())

# Function to decrypt the incoming payload
def decrypt_request(encrypted_data_b64, encrypted_aes_key_b64, iv_b64):
    encrypted_data = base64.b64decode(encrypted_data_b64)
    encrypted_aes_key = base64.b64decode(encrypted_aes_key_b64)
    iv = base64.b64decode(iv_b64)

    cipher_rsa = PKCS1_OAEP.new(PRIVATE_KEY)
    aes_key = cipher_rsa.decrypt(encrypted_aes_key)

    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher_aes.decrypt(encrypted_data), AES.block_size)

    return json.loads(decrypted_data), aes_key, iv

# Function to encrypt the outgoing response
def encrypt_response(response_data, aes_key, iv):
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(json.dumps(response_data).encode(), AES.block_size))
    return base64.b64encode(encrypted_data)

# Handle POST requests to /webhook/
@csrf_exempt
def webhook(request):
    if request.method == "POST":
        return handle_message_response(request)
    return JsonResponse({"error": "Only POST requests allowed"}, status=405)

# Main handler logic
def handle_message_response(request):
    try:
        body = json.loads(request.body)

        # ✅ Handle interactive response (e.g. user taps button in WhatsApp Flow)
        if "messages" in body:
            print("📨 Received WhatsApp Flow Response (interactive):", json.dumps(body, indent=2))

            for message in body.get("messages", []):
                if message.get("type") == "interactive" and message.get("interactive", {}).get("type") == "nfm_reply":
                    user_phone = message.get("from")
                    response_json = message["interactive"]["nfm_reply"].get("response_json")

                    if response_json:
                        response_data = json.loads(response_json)
                        flow_token = response_data.get("flow_token")
                        selected_option = response_data.get("screen_0_Senaria_Pilihan_0")

                        response_messages = {
                            "0_Semak_Bantuan": "Anda telah memilih Semak Bantuan. Sila tunggu sebentar.",
                            "1_Senarai_Pasaraya": "Berikut adalah senarai pasaraya yang mengambil bahagian: [Link]",
                            "2_Program_SARA": "Maklumat mengenai Program SARA boleh didapati di sini: [Link]",
                            "3_Cara_Tebus_Bantuan": "Ikuti langkah ini untuk menebus bantuan: [Link]",
                            "4_Mewakilkan_Ahli_Keluarga": "Maklumat lanjut mengenai mewakilkan ahli keluarga: [Link]",
                            "5_Barang_Bantuan": "Barang bantuan yang tersedia: [List]",
                            "6_Jumlah_Bantuan": "Jumlah bantuan yang boleh anda terima bergantung kepada kelayakan anda.",
                            "7_Waktu_Tebus_Bantuan": "Anda boleh menebus bantuan dalam waktu berikut: [Time]",
                            "8__Hubungi_Kami": "Sila hubungi kami di nombor berikut: +60123456789",
                            "9__IC_Hilang_/_Rosak": "Sekiranya IC anda hilang atau rosak, sila rujuk kepada Jabatan Pendaftaran Negara."
                        }

                        response_message = response_messages.get(selected_option, "Pilihan tidak sah.")

                        send_whatsapp_message({
                            "contacts": [{"phone_numbers": user_phone}],
                            "template_name": response_message,
                            "language_code": "ms"
                        })

                        print(f"✅ Replied to {user_phone} with: {response_message}")

            return JsonResponse({"status": "interactive handled"}, status=200)

        # ✅ Handle encrypted INIT or data_exchange
        encrypted_flow_data_b64 = body.get("encrypted_flow_data")
        encrypted_aes_key_b64 = body.get("encrypted_aes_key")
        iv_b64 = body.get("initial_vector")

        if not all([encrypted_flow_data_b64, encrypted_aes_key_b64, iv_b64]):
            return JsonResponse({"error": "Missing encryption fields"}, status=400)

        decrypted_data, aes_key, iv = decrypt_request(encrypted_flow_data_b64, encrypted_aes_key_b64, iv_b64)
        print("🔓 Decrypted Flow Data:", json.dumps(decrypted_data, indent=2))

        action = decrypted_data.get("action")
        flow_token = "flows-builder-7797319f"

        if action == "INIT":
            response_payload = {
                "screen": "DETAILS",
                "data": {}
            }

        elif action == "data_exchange":
            # This is where you handle selections (only if needed within flow)
            response_payload = {
                "screen": "SUCCESS",
                "data": {
                    "extension_message_response": {
                        "params": {
                            "flow_token": flow_token,
                            "response_message": "Pilihan anda telah direkodkan."
                        }
                    }
                }
            }

        elif action == "BACK":
            response_payload = {"screen": "DETAILS", "data": {}}

        else:
            response_payload = {"data": {"status": "active"}}

        encrypted_response = encrypt_response(response_payload, aes_key, iv)
        return HttpResponse(encrypted_response, content_type="text/plain", status=200)

    except Exception as e:
        print(f"❌ Error in webhook: {e}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)
