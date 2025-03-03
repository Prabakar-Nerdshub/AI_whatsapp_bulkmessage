import json
import logging
import requests
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)

INSTANCE_ID = "cm7k3vaj81vtdsyhmoscd4af3"  # Ensure this token is correct


def send_whatsapp_message(phone_number, message):
    url = f"https://whatsapp.myappstores.com/api/sendText?token={INSTANCE_ID}&phone={phone_number}&message={message}"

    try:
        response = requests.get(url, timeout=10)
        response_data = response.json()

        logger.info(f"API Response for {phone_number}: {response_data}")

        # Print response for debugging
        print(f"Response for {phone_number}: {response_data}")

        if response.status_code == 200 and response_data.get("status") == "success":
            return True
        else:
            logger.error(f"Failed to send to {phone_number}: {response_data}")
            return False

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for {phone_number}: {str(e)}")
        return False


@csrf_exempt
@api_view(['POST'])
def send_bulk_messages(request):
    if request.method == "POST":
        try:
            raw_data = request.body.decode('utf-8')
            logger.info(f"Raw Request Body: {raw_data}")

            data = json.loads(raw_data)
            message = data.get("message", "").strip()
            phone_numbers = data.get("phoneNumbers", [])
            country_code = "91"  # Fixed country code without '+'

            if not message or not phone_numbers:
                return JsonResponse({"error": "Message and phone numbers are required."}, status=400)

            formatted_phone_numbers = []
            for num in phone_numbers:
                num_str = str(num).strip()

                # Remove any non-numeric characters
                num_str = re.sub(r"[^\d]", "", num_str)

                # Ensure 91 prefix
                if not num_str.startswith("91"):
                    num_str = f"{country_code}{num_str}"

                # Explicitly remove spaces
                num_str = num_str.replace(" ", "")

                if re.match(r"^91\d{10}$", num_str):  # Validate format
                    formatted_phone_numbers.append(num_str)
                else:
                    logger.warning(f"Invalid phone number format: {num_str}")

            if not formatted_phone_numbers:
                return JsonResponse({"error": "No valid phone numbers found."}, status=400)

            logger.info(f"Final List of Phone Numbers: {formatted_phone_numbers}")

            success_numbers = []
            failed_numbers = []

            for number in formatted_phone_numbers:
                if send_whatsapp_message(number, message):
                    success_numbers.append(number)
                else:
                    failed_numbers.append(number)

            return JsonResponse({
                "success": f"Messages sent to {len(success_numbers)} numbers!",
                "sent": success_numbers,
                "failed": failed_numbers,
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
