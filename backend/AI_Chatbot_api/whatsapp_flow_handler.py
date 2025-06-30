from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import os
import time
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from .utils import encrypt_flow_response


PRIVATE_KEY_PATH = r'D:/meta_api_implement/backend/AI_Chatbot_api/pem_file/new_private.pem'

# Response map for flow options 0_Semak_Bantuan, 1_Senarai_Pasaraya
responses = {
    "0_Semak_Bantuan": '''Sila layari pautan berikut untuk Semak Status Bantuan anda.
Pautan: https://app.mykasih.net/sara2/checkstatus (TEKAN)
Nota Penting: Anda TIDAK BOLEH memohon untuk Program SARA. Kelayakan
SARA 2025 adalah secara automatik berdasarkan data Miskin
Tegar dan Miskin eKasih sehingga 31 Oktober 2024. SARA 2025 turut diperluas
kepada semua penerima STR 2025 kategori Isi Rumah dan Warga Emas Tiada
Pasangan.
Untuk sebarang pertanyaan sila hubungi talian MyKasih di +60377201800 (Isnin -
Jumaat @ 9am - 5pm)''',

    "1_Senarai_Pasaraya": '''Penerima yang layak akan diberi penerangan mengenai kedai runcit terdekat
untuk membeli barangan keperluan asas. MyKasih mempunyai lebih daripada
1,200 rakan niaga di seluruh negara termasuk Mydin, Giant, Econsave, The Store,
Pacific, Milimewa, 99 Speedmart, Lotus Stores (Tesco), serta pasar raya dan
pasar mini bebas. Sila layari pautan berikut untuk dapatkan senarai pasaraya
terpilih MyKasih berdekatan anda.
Senarai pasaraya: https://app.mykasih.net/sara2/merchant-list''',

    "2_Program_SARA": '''Sumbangan Asas Rahmah (SARA) merupakan program bantuan bersasar
kepada rakyat yang paling terkesan dengan gelumang kos sara hidup. Program
sumbangan ini adalah untuk mengangkat taraf ekonomi golongan rentan dan
menjunjung prinsip kesaksamaan yang menjadi teras kepada kerangka Ekonomi
MADANI.
Penerima STR 2025 yang telah disahkan daripada data Miskin Tegar dan Miskin
eKasih layak SARA 2025 berjumlah RM100 / RM50 setiap bulan bagi tempoh 12
bulan (Januari 2025 - Disember 2025).
Manakala kadar tambahan kepada semua penerima STR 2025 kategori Isi
Rumah dan Warga Emas Tiada Pasangan adalah RM100 / RM50 setiap bulan
bagi tempoh 9 bulan (April 2025 - Disember 2025).''',

    "3_Cara_Tebus_Bantuan": '''Sila layari pautan berikut untuk mengetahui cara menebus bantuan anda.
CARA TEBUS BANTUAN (TONTON):
https://www.youtube.com/watch?v=hxYmi0OZPEg/
Untuk sebarang pertanyaan sila hubungi talian MyKasih di +60377201800 (Isnin -
Jumaat @ 9am - 5pm)''',

    "4_Mewakilkan_Ahli_Keluarga": '''Penerima boleh menghantar ahli keluarga sebagai wakil untuk buat pembelian
namun, sebarang pembelian yang dibuat oleh individu selain penerima adalah di
bawah tanggungjawab penerima itu sendiri. Sila bawa bersama IC asal penerima
semasa / untuk tebus bantuan.''',

    "5_Barang_Bantuan": '''Penerima boleh membeli barangan keperluan asas daripada 13 kategori
produk yang diluluskan iaitu beras, roti, telur, minyak masak, tepung, biskut, mi
segera, minuman, makanan dalam tin, bahan perasa, produk kebersihan,
ubat-ubatan dan barangan persekolahan.''',

    "6_Jumlah_Bantuan": '''Penerima akan menerima elaun bulanan melalui MyKad mereka untuk
membeli barang keperluan asas terpilih.
Pembayaran kepada penerima SARA 2025 adalah seperti jadual berikut:
Penerima STR 2025 yang telah disahkan daripada data Miskin Tegar dan Miskin
eKasih layak SARA 2025 berjumlah RM100 / RM50 setiap bulan bagi tempoh 12
bulan (Januari 2025 - Disember 2025). Sila rujuk jadual diatas.''',

    "7_Waktu_Tebus_Bantuan": '''Anda boleh menebus bantuan pada bila-bila masa di pasaraya terpilih
MyKasih terdekatan anda.
Sila pilih "Senarai Pasaraya" di Menu Utama untuk senarai pasaraya.''',

    "8__Hubungi_Kami": '''Sila hubungi talian hotline MyKasih di +60377201800 (Isnin - Jumaat @ 9am - 5pm)''',
    "9__IC_Hilang_/_Rosak": '''Sila hubungi Talian Bantuan MyKasih.
Pengecualian pembelian secara manual akan diberikan hanya bagi satu transaksi
pembelian. Pembelian seterusnya hanya boleh dibuat menggunakan MyKad
baharu anda.
Hubungi Talian Bantuan MyKasih: 03-7720 1800 (Isnin - Jumaat @ 9am - 5pm)'''
    }

WHATSAPP_API_URL = "https://graph.facebook.com/v22.0/627644197089809/messages"
WHATSAPP_ACCESS_TOKEN = "EAAYgHPHSE6MBO4sSEZCcZASaZAYyVtMUj97AR36girXjcHq1Na7Y8aQ6etfaEKImTnrdwcPnx7zZBieBkXWBVISuzgQ9mUBtDGacCaUFbBz5ZAzOcRKZBfuphySmr0Wx3ABNVt23zggR1vhUa4VH0lr6bRihfr0cxdDDGHprL04h9cQLCQKi3RFwZB3SLhJ6DB3egZCHX7WQVam51xiU"

# Simple in-memory cache to prevent duplicate messages
message_cache = {}
CACHE_DURATION = 300  # 5 minutes

def is_duplicate_message(phone, selection, message):
    """Check if this message was recently sent to prevent duplicates"""
    current_time = time.time()
    cache_key = f"{phone}_{selection}_{hash(message)}"
    
    # Clean old entries
    expired_keys = [k for k, v in message_cache.items() if current_time - v > CACHE_DURATION]
    for key in expired_keys:
        del message_cache[key]
    
    # Check if message was recently sent
    if cache_key in message_cache:
        return True
    
    # Add to cache
    message_cache[cache_key] = current_time
    return False

def send_whatsapp_message(phone, message, selection=None):
    """Send WhatsApp message with duplicate prevention"""
    if not phone or not message:
        print("⚠️ Missing phone or message")
        return None
        
    # Check for duplicates
    if is_duplicate_message(phone, selection, message):
        print(f"🚫 Duplicate message prevented for {phone}")
        return None
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }
    
    print(f"📤 Sending message to {phone}: {message[:50]}...")
    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        print(f"🔁 WhatsApp API Response: {response.status_code}")
        return response
    except Exception as e:
        print(f"❌ Error sending WhatsApp message: {e}")
        return None

@csrf_exempt
def webhook(request):
    if request.method == "GET":
        # Handle webhook verification
        verify_token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        if verify_token == 'your_verify_token':  # Replace with your actual verify token
            return HttpResponse(challenge)
        return HttpResponse('Verification failed', status=403)
    
    if request.method == "POST":
        try:
            print(f"📌🔗 Received request to {request.path}")
            
            body = json.loads(request.body)
            print("📥 Webhook Body:", json.dumps(body, indent=2))

            # Determine the type of request and handle accordingly
            if "encrypted_flow_data" in body:
                print("🔒 Handling encrypted flow data")
                return handle_encrypted_flow(body)
            elif "entry" in body:
                print("💬 Handling WhatsApp message entry")
                return handle_whatsapp_entry(body)
            elif body.get("action") == "data_exchange": #data_exchange
                print("🔄 Handling unencrypted data exchange")
                return handle_unencrypted_flow(body)
            else:
                print("❓ Unknown request type")
                return JsonResponse({"status": "ok"})

        except Exception as e:
            print(f"❌ Webhook Error: {e}")
            return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)
    
    return JsonResponse({"status": "ok"})

def handle_encrypted_flow(body):
    """Handle encrypted flow data from WhatsApp Flow"""
    try:
        encrypted_flow_data_b64 = body.get("encrypted_flow_data")
        encrypted_aes_key_b64 = body.get("encrypted_aes_key")
        iv_b64 = body.get("initial_vector")

        if not all([encrypted_flow_data_b64, encrypted_aes_key_b64, iv_b64]):
            return JsonResponse({"error": "Missing encryption fields"}, status=400)

        decrypted_data, aes_key, iv = decrypt_request(encrypted_flow_data_b64, encrypted_aes_key_b64, iv_b64)
        print("🔓 Decrypted Data:", json.dumps(decrypted_data, indent=2))

        action = decrypted_data.get("action")
        phone_number = decrypted_data.get("user", {}).get("wa_id", "")

        # Extract selection
        selected_value = extract_selection(decrypted_data)
        print(f"🔍 Selected value: {selected_value}")

        response_payload = {}

        if action == "INIT":
            response_payload = {
                "screen": "DETAILS",
                "data": {},
                "extension_message_response": {
                    "params": {
                        "keep_active": True,
                        "allow_reentry": True
                    }
                }
            }
            print("✅ Responding to INIT with DETAILS screen (active)")

        elif action == "data_exchange":
            if selected_value and phone_number:
                msg = responses.get(selected_value, f"📌 Anda telah memilih: {selected_value.replace('_', ' ')}")
                send_whatsapp_message(phone_number, msg, selected_value)

            response_payload = {
                "screen": "DETAILS",
                "data": {},
                "extension_message_response": {
                    "params": {
                        "keep_active": True,
                        "allow_reentry": True
                    }
                }
            }
            print("🔁 Responding to data_exchange with DETAILS screen (active)")

        elif action == "complete":
            if selected_value and phone_number:
                msg = responses.get(selected_value, f"📌 Anda telah memilih: {selected_value.replace('_', ' ')}")
                send_whatsapp_message(phone_number, msg, selected_value)

            # Keep the button alive
            response_payload = {
                "screen": "DETAILS",  # 🔁 Loop back to DETAILS screen
                "data": {},
                "extension_message_response": {
                    "params": {
                        "keep_active": True,
                        "allow_reentry": True
                    }
                }
            }
            print("🔁 Responding to complete with DETAILS screen (flow stays active)")

        elif action == "BACK":
            response_payload = {
                "screen": "DETAILS",
                "data": {},
                "extension_message_response": {
                    "params": {
                        "keep_active": True,
                        "allow_reentry": True
                    }
                }
            }
            print("✅ Responding to BACK with DETAILS screen (active)")

        else:
            response_payload = {
                "data": {"status": "active"},
                "extension_message_response": {
                    "params": {
                        "keep_active": True,
                        "allow_reentry": True
                    }
                }
            }
            print(f"✅ Responding to meta whatsapp health check  webhook  action ({action}) with active status")

        encrypted_response = encrypt_flow_response(response_payload, aes_key, iv)
        return HttpResponse(encrypted_response, content_type="text/plain", status=200)

    except Exception as e:
        print(f"❌ handle_encrypted_flow Error: {e}")
        return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)

def handle_whatsapp_entry(body):
    """Handle WhatsApp webhook entries (messages, statuses, etc.)"""
    try:
        entries = body.get("entry", [])
        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                
                # Handle message status updates (delivery, read, etc.)
                if "statuses" in value:
                    print("📊 Received message status update")
                    continue
                
                # Handle interactive messages from flows
                messages = value.get("messages", [])
                for message in messages:
                    if message.get("type") == "interactive":
                        interactive_data = message.get("interactive", {})
                        
                        # Handle NFM (Native Flow Message) replies
                        if interactive_data.get("type") == "nfm_reply":
                            nfm_reply = interactive_data.get("nfm_reply", {})
                            response_json_str = nfm_reply.get("response_json", "{}")
                            
                            try:
                                response_data = json.loads(response_json_str)
                                print(f"🎛️ Flow response data: {response_data}")
                                
                                # Extract user selection
                                user_selection = None
                                for key, value in response_data.items():
                                    if key.startswith("screen_0_"):
                                        user_selection = value
                                        break
                                
                                if user_selection:
                                    # Get user phone number
                                    phone_number = message.get("from", "")
                                    
                                    # Get response message
                                    response_msg = responses.get(user_selection, 
                                        f"📌 Anda telah memilih: {user_selection.replace('_', ' ')}")
                                    
                                    # Send response message
                                    if phone_number:
                                        print(f"📤 Sending flow response to {phone_number}")
                                        send_whatsapp_message(phone_number, response_msg, user_selection)
                                    
                            except json.JSONDecodeError as e:
                                print(f"❌ Error parsing flow response JSON: {e}")
                        
                        # Handle other interactive types (button replies, list replies)
                        elif interactive_data.get("type") in ["button_reply", "list_reply"]:
                            print("🔘 Button/List interaction received")
                            # Handle button/list replies if needed
                
        return JsonResponse({"status": "ok"})
        
    except Exception as e:
        print(f"❌ handle_whatsapp_entry Error: {e}")
        return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)

def handle_unencrypted_flow(body):
    """Handle unencrypted flow data (fallback)"""
    try:
        phone = body.get("phone_number", "")
        user_selection_value = None
        
        # Find selection in body
        for key in body:
            if key.startswith("screen_0_"):
                user_selection_value = body[key]
                break

        if not user_selection_value:
            return JsonResponse({"error": "No button selected"}, status=400)

        response_message = responses.get(user_selection_value, "Terima kasih atas pilihan anda.")
        
        if phone:
            send_whatsapp_message(phone, response_message, user_selection_value)

        return JsonResponse({"status": "ok", "message": response_message})

    except Exception as e:
        print(f"❌ handle_unencrypted_flow Error: {e}")
        return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)

def extract_selection(decrypted_data):
    """Extract user selection from various possible locations in the data"""
    data = decrypted_data.get("data", {})
    payload = decrypted_data.get("payload", {})
    form_data = data.get("form", {})
    
    # Try different possible field names
    possible_fields = [
        "screen_0_Senaria_Pilihan_0",
        "Senaria_Pilihan_3e04aa",
        "selected_option"
    ]
    
    # Check in data
    for field in possible_fields:
        if field in data:
            return data[field]
    
    # Check in form_data
    for field in possible_fields:
        if field in form_data:
            return form_data[field]
    
    # Check in payload
    for field in possible_fields:
        if field in payload:
            return payload[field]
    
    return None

def decrypt_request(encrypted_flow_data_b64, encrypted_aes_key_b64, iv_b64):
    """Decrypt the encrypted flow data"""
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(iv_b64)

    with open(PRIVATE_KEY_PATH, 'rb') as key_file:
        private_key = load_pem_private_key(key_file.read(), password=None)

    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        OAEP(mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    encrypted_body = flow_data[:-16]
    tag = flow_data[-16:]
    decryptor = Cipher(algorithms.AES(aes_key), modes.GCM(iv, tag)).decryptor()
    decrypted_bytes = decryptor.update(encrypted_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_bytes.decode("utf-8"))

    return decrypted_data, aes_key, iv





'''from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import os
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from .utils import encrypt_flow_response

PRIVATE_KEY_PATH = r'D:/meta_api_implement/backend/AI_Chatbot_api/pem_file/new_private.pem'

# Response map for flow options
responses = {
    "0_Semak_Bantuan": Sila layari pautan berikut untuk Semak Status Bantuan anda.
Pautan: https://app.mykasih.net/sara2/checkstatus (TEKAN)
Nota Penting: Anda TIDAK BOLEH memohon untuk Program SARA. Kelayakan
SARA 2025 adalah secara automatik berdasarkan data Miskin
Tegar dan Miskin eKasih sehingga 31 Oktober 2024. SARA 2025 turut diperluas
kepada semua penerima STR 2025 kategori Isi Rumah dan Warga Emas Tiada
Pasangan.
Untuk sebarang pertanyaan sila hubungi talian MyKasih di +60377201800 (Isnin -
Jumaat @ 9am - 5pm),

    "1_Senarai_Pasaraya": Penerima yang layak akan diberi penerangan mengenai kedai runcit terdekat
untuk membeli barangan keperluan asas. MyKasih mempunyai lebih daripada
1,200 rakan niaga di seluruh negara termasuk Mydin, Giant, Econsave, The Store,
Pacific, Milimewa, 99 Speedmart, Lotus Stores (Tesco), serta pasar raya dan
pasar mini bebas. Sila layari pautan berikut untuk dapatkan senarai pasaraya
terpilih MyKasih berdekatan anda.
Senarai pasaraya: https://app.mykasih.net/sara2/merchant-list,

    "2_Program_SARA": Sumbangan Asas Rahmah (SARA) merupakan program bantuan bersasar
kepada rakyat yang paling terkesan dengan gelumang kos sara hidup. Program
sumbangan ini adalah untuk mengangkat taraf ekonomi golongan rentan dan
menjunjung prinsip kesaksamaan yang menjadi teras kepada kerangka Ekonomi
MADANI.
Penerima STR 2025 yang telah disahkan daripada data Miskin Tegar dan Miskin
eKasih layak SARA 2025 berjumlah RM100 / RM50 setiap bulan bagi tempoh 12
bulan (Januari 2025 - Disember 2025).
Manakala kadar tambahan kepada semua penerima STR 2025 kategori Isi
Rumah dan Warga Emas Tiada Pasangan adalah RM100 / RM50 setiap bulan
bagi tempoh 9 bulan (April 2025 - Disember 2025).,

    "3_Cara_Tebus_Bantuan": Sila layari pautan berikut untuk mengetahui cara menebus bantuan anda.
CARA TEBUS BANTUAN (TONTON):
https://www.youtube.com/watch?v=hxYmi0OZPEg/
Untuk sebarang pertanyaan sila hubungi talian MyKasih di +60377201800 (Isnin -
Jumaat @ 9am - 5pm),

    "4_Mewakilkan_Ahli_Keluarga": Penerima boleh menghantar ahli keluarga sebagai wakil untuk buat pembelian
namun, sebarang pembelian yang dibuat oleh individu selain penerima adalah di
bawah tanggungjawab penerima itu sendiri. Sila bawa bersama IC asal penerima
semasa / untuk tebus bantuan.,

    "5_Barang_Bantuan": Penerima boleh membeli barangan keperluan asas daripada 13 kategori
produk yang diluluskan iaitu beras, roti, telur, minyak masak, tepung, biskut, mi
segera, minuman, makanan dalam tin, bahan perasa, produk kebersihan,
ubat-ubatan dan barangan persekolahan.,

    "6_Jumlah_Bantuan": Penerima akan menerima elaun bulanan melalui MyKad mereka untuk
membeli barang keperluan asas terpilih.
Pembayaran kepada penerima SARA 2025 adalah seperti jadual berikut:
Penerima STR 2025 yang telah disahkan daripada data Miskin Tegar dan Miskin
eKasih layak SARA 2025 berjumlah RM100 / RM50 setiap bulan bagi tempoh 12
bulan (Januari 2025 - Disember 2025). Sila rujuk jadual diatas.,

    "7_Waktu_Tebus_Bantuan": Anda boleh menebus bantuan pada bila-bila masa di pasaraya terpilih
MyKasih terdekatan anda.
Sila pilih "Senarai Pasaraya" di Menu Utama untuk senarai pasaraya.,

    "8__Hubungi_Kami": Sila hubungi talian hotline MyKasih di +60377201800 (Isnin - Jumaat @ 9am - 5pm),
    "9__IC_Hilang_/_Rosak": Sila hubungi Talian Bantuan MyKasih.
Pengecualian pembelian secara manual akan diberikan hanya bagi satu transaksi
pembelian. Pembelian seterusnya hanya boleh dibuat menggunakan MyKad
baharu anda.
Hubungi Talian Bantuan MyKasih: 03-7720 1800 (Isnin - Jumaat @ 9am - 5pm)
    }

WHATSAPP_API_URL = "https://graph.facebook.com/v22.0/627644197089809/messages" #Nerdshub Number 
WHATSAPP_ACCESS_TOKEN = "EAAYgHPHSE6MBO4sSEZCcZASaZAYyVtMUj97AR36girXjcHq1Na7Y8aQ6etfaEKImTnrdwcPnx7zZBieBkXWBVISuzgQ9mUBtDGacCaUFbBz5ZAzOcRKZBfuphySmr0Wx3ABNVt23zggR1vhUa4VH0lr6bRihfr0cxdDDGHprL04h9cQLCQKi3RFwZB3SLhJ6DB3egZCHX7WQVam51xiU"

def send_whatsapp_message(phone, message):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }
    print(f"📤 Sending message to {phone}: {message}")
    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
    print(f"🔁 WhatsApp API Response: {response.status_code} - {response.text}")
    return response

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        try:
            print(f"📌 Received request to {request.path}")
            print(f"📄 Request body: {request.body}")
            
            body = json.loads(request.body)
            print("📥 Webhook Body:", json.dumps(body, indent=2))

            if body.get("action") == "data_exchange" and "encrypted_flow_data" not in body:
                return handle_unencrypted_flow(body)

            if "entry" in body:
                return handle_interactive_message(body)

            return handle_post_request(request)

        except Exception as e:
            print(f"❌ Webhook Error: {e}")
            return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)
    
    return JsonResponse({"status": "ok"})

def handle_unencrypted_flow(body):
    try:
        phone = body.get("phone_number", "")
        user_selection_value = None
        for key in body:
            if key.startswith("screen_0_"):
                user_selection_value = body[key]
                break

        if not user_selection_value:
            return JsonResponse({"error": "No button selected"}, status=400)

        response_message = responses.get(user_selection_value, "Terima kasih atas pilihan anda.")
        send_whatsapp_message(phone, response_message)

        return JsonResponse({"status": "ok", "message": response_message})

    except Exception as e:
        print(f"❌ handle_unencrypted_flow Error: {e}")
        return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)

def handle_post_request(request):
    try:
        body = json.loads(request.body)
        print("🌊 Incoming webhook:", request.body)
        
        encrypted_flow_data_b64 = body.get("encrypted_flow_data")
        encrypted_aes_key_b64 = body.get("encrypted_aes_key")
        iv_b64 = body.get("initial_vector")

        if not all([encrypted_flow_data_b64, encrypted_aes_key_b64, iv_b64]):
            return JsonResponse({"error": "Missing encryption fields"}, status=400)

        decrypted_data, aes_key, iv = decrypt_request(encrypted_flow_data_b64, encrypted_aes_key_b64, iv_b64)
        print("🔓 Decrypted Data:", json.dumps(decrypted_data, indent=2))

        action = decrypted_data.get("action")
        phone_number = decrypted_data.get("user", {}).get("wa_id", "")
        response_payload = {}

        # Look for selection in different possible paths
        selected_value = None
        data = decrypted_data.get("data", {})
        
        # Check for direct key in data
        if "screen_0_Senaria_Pilihan_0" in data:
            selected_value = data["screen_0_Senaria_Pilihan_0"]
        elif "Senaria_Pilihan_3e04aa" in data:
            selected_value = data["Senaria_Pilihan_3e04aa"]
            
        # Check in form data if available
        form_data = data.get("form", {})
        if not selected_value and "Senaria_Pilihan_3e04aa" in form_data:
            selected_value = form_data["Senaria_Pilihan_3e04aa"]
            
        # Also check in payload
        payload = decrypted_data.get("payload", {})
        if not selected_value and "screen_0_Senaria_Pilihan_0" in payload:
            selected_value = payload["screen_0_Senaria_Pilihan_0"]

        print(f"🔍 Selected value: {selected_value}")

        if action == "INIT":
            response_payload = {"screen": "DETAILS", "data": {}}
            print("✅ Responding to INIT with DETAILS screen")

        elif action == "data_exchange":
            if selected_value:
                msg = responses.get(selected_value, f"📌 Anda telah memilih: {selected_value.replace('_', ' ')}")
                
                if phone_number:
                    send_whatsapp_message(phone_number, msg)
                else:
                    print("⚠️ No phone number available for sending WhatsApp message")

            response_payload = {
                "screen": "CONFIRMATION",
                "data": {
                    "selected_option": selected_value or "unknown"
                }
            }
            print("✅ Responding to data_exchange with CONFIRMATION screen")

        elif action == "complete":
            print("✅ Flow completed by user")
            
            # Extract selection from multiple possible locations
            selection = selected_value
            
            if not selection:
                # Try to get from payload directly
                selection = payload.get("screen_0_Senaria_Pilihan_0", "")
            
            if not selection:
                # Try to extract from form data if available
                form_data = decrypted_data.get("form", {})
                selection = form_data.get("Senaria_Pilihan_3e04aa", "")
            
            print(f"🔍 Final selected option: {selection}")
            
            response_message = responses.get(selection, "Terima kasih atas pilihan anda.")
            
            if phone_number:
                send_whatsapp_message(phone_number, response_message)
            else:
                print("⚠️ No phone number found in complete action. Trying to find it elsewhere...")
                # Try to find phone number in other parts of the data
                user_data = decrypted_data.get("user", {})
                if "phone" in user_data:
                    phone_number = user_data["phone"]
                    send_whatsapp_message(phone_number, response_message)
                else:
                    print("❌ Cannot find phone number to send message")

            response_payload = {
                "screen": None,
                "data": {
                    "status": "completed"
                }
            }
            print("✅ Responding to complete action with completed status")

        elif action == "BACK":
            response_payload = {"screen": "DETAILS", "data": {}}
            print("✅ Responding to BACK with DETAILS screen")

        else:
            response_payload = {"data": {"status": "active"}}
            print(f"✅ Responding to unknown action {action} with active status")

        encrypted_response = encrypt_flow_response(response_payload, aes_key, iv)
        return HttpResponse(encrypted_response, content_type="text/plain", status=200)

    except Exception as e:
        print(f"❌ handle_post_request Error: {e}")
        return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)

def handle_interactive_message(entry):
    try:
        changes = entry.get("entry", [])[0].get("changes", [])
        for change in changes:
            messages = change.get("value", {}).get("messages", [])
            for message in messages:
                if message.get("type") == "interactive":
                    interactive = message.get("interactive", {})
                    if interactive.get("type") == "nfm_reply":
                        nfm_reply = interactive.get("nfm_reply", {})
                        response_json = json.loads(nfm_reply.get("response_json", "{}"))
                        flow_token = response_json.get("flow_token", "")
                        
                        # Extract phone number
                        phone_number = message.get("from", "")
                        
                        # Extract selected option if available
                        selected_option = response_json.get("screen_0_Senaria_Pilihan_0", "")
                        
                        if selected_option and phone_number:
                            response_message = responses.get(selected_option, "Terima kasih atas pilihan anda.")
                            send_whatsapp_message(phone_number, response_message)
                        
                        screen_response = {
                            "screen": "SUCCESS",
                            "data": {
                                "extension_message_response": {
                                    "params": {
                                        "flow_token": flow_token
                                    }
                                }
                            }
                        }
                        encrypted_response = encrypt_flow_response(screen_response)
                        return JsonResponse(encrypted_response)
    except Exception as e:
        print(f"❌ handle_interactive_message Error: {e}")
    return JsonResponse({"status": "no-action"})

def decrypt_request(encrypted_flow_data_b64, encrypted_aes_key_b64, iv_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(iv_b64)

    with open(PRIVATE_KEY_PATH, 'rb') as key_file:
        private_key = load_pem_private_key(key_file.read(), password=None)

    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        OAEP(mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    encrypted_body = flow_data[:-16]
    tag = flow_data[-16:]
    decryptor = Cipher(algorithms.AES(aes_key), modes.GCM(iv, tag)).decryptor()
    decrypted_bytes = decryptor.update(encrypted_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_bytes.decode("utf-8"))

    return decrypted_data, aes_key, iv '''