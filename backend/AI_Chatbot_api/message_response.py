from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .views import send_whatsapp_message

@csrf_exempt
def message_response_webhook(request):
    """
    Webhook to handle user responses from WhatsApp Flow messages.
    """
    try:
        body = json.loads(request.body)
        print("Received WhatsApp Flow Response:", json.dumps(body, indent=2))

        messages = body.get("messages", [])
        if not messages:
            return JsonResponse({"error": "No messages found"}, status=400)

        for message in messages:
            if message.get("type") == "interactive" and message.get("interactive", {}).get("type") == "nfm_reply":
                user_phone = message.get("from")  # Extract user's WhatsApp number
                response_json = message["interactive"]["nfm_reply"].get("response_json")

                # Parse response JSON
                response_data = json.loads(response_json)
                flow_token = response_data.get("flow_token")
                selected_option = response_data.get("optional_param1")  # Change key as needed

                # Define custom responses based on user selection
                response_messages = {
                    "Semak_Bantuan": "Anda telah memilih Semak Bantuan. Sila tunggu sebentar.",
                    "Senarai_Pasaraya": "Berikut adalah senarai pasaraya yang mengambil bahagian: [Link]",
                    "Program_SARA": "Maklumat mengenai Program SARA boleh didapati di sini: [Link]",
                    "Cara_Tebus_Bantuan": "Ikuti langkah ini untuk menebus bantuan: [Link]",
                    "Mewakilkan_Ahli_Keluarga": "Maklumat lanjut mengenai mewakilkan ahli keluarga: [Link]",
                    "Barang_Bantuan": "Barang bantuan yang tersedia: [List]",
                    "Jumlah_Bantuan": "Jumlah bantuan yang boleh anda terima bergantung kepada kelayakan anda.",
                    "Waktu_Tebus_Bantuan": "Anda boleh menebus bantuan dalam waktu berikut: [Time]",
                    "Hubungi_Kami": "Sila hubungi kami di nombor berikut: +60123456789",
                    "IC_Hilang_Rosak": "Sekiranya IC anda hilang atau rosak, sila rujuk kepada Jabatan Pendaftaran Negara."
                }

                # Get the appropriate response message
                response_message = response_messages.get(selected_option, "Pilihan tidak sah.")

                # ✅ Send WhatsApp message back to user
                send_whatsapp_message({
                    "contacts": [{"phone_numbers": user_phone}],
                    "template_name": response_message,
                    "language_code": "ms"
                })

                print(f"Sent response to {user_phone}: {response_message}")

        return JsonResponse({"status": "success"}, status=200)

    except Exception as e:
        print(f"Error processing flow response: {e}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)
