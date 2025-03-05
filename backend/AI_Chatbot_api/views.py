# api/views.py

import json
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import gridfs
from io import BytesIO
from django.conf import settings
from pymongo.server_api import ServerApi
from django.middleware.csrf import get_token
from bson import ObjectId
import logging
import requests

# Setup Logging
logger = logging.getLogger(__name__)

# ✅ MongoDB Setup
db_password = "prabavj1503"
uri = f"mongodb+srv://vedhamaniprabakar:{db_password}@cluster0.bnrac.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["whatsapp_broadcast"]
fs = gridfs.GridFS(db)

# ✅ CSRF Token Endpoint
def get_csrf_token(request):
    return JsonResponse({"csrfToken": get_token(request)})

# ✅ Upload CSV/Excel to GridFS
@csrf_exempt
def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        try:
            file = request.FILES["file"]

            # ✅ Validate File Type
            if not file.name.endswith((".csv", ".xls", ".xlsx")):
                return JsonResponse({"error": "Unsupported file format"}, status=400)

            file_id = fs.put(file.read(), filename=file.name)
            return JsonResponse({"message": "File uploaded successfully", "file_id": str(file_id)})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "No file provided"}, status=400)

# ✅ Fetch phone numbers from uploaded file
def get_phone_numbers(request, file_id):
    try:
        file_obj_id = ObjectId(file_id)
        grid_out = fs.get(file_obj_id)
        file_content = BytesIO(grid_out.read())

        # ✅ Read CSV/Excel
        if grid_out.filename.endswith(".csv"):
            df = pd.read_csv(file_content)
        else:
            df = pd.read_excel(file_content, engine="openpyxl")
        #--Need to work on this logic
        numbers = df.iloc[:, 1].dropna().astype(str).tolist()
        phone_numbers = []
        for i in numbers:
            phone_numbers.append('91' + str(i))

        return JsonResponse({"phone_numbers": phone_numbers})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# ✅ Send bulk messages
#@csrf_exempt
'''def send_bulk_messages(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            message = data.get("message")

            if not message:
                return JsonResponse({"error": "Message is required"}, status=400)

            return JsonResponse({"message": "Message received successfully."}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
'''
# ✅ Send WhatsApp messages via API
INSTANCE_ID = "cm7k3vaj81vtdsyhmoscd4af3"

@csrf_exempt
def send_whatsapp_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            file_id = data.get("file_id")
            message = data.get("message")


            if not file_id or not message:
                return JsonResponse({"error": "File ID and message are required."}, status=400)

            # ✅ Fetch phone numbers
            response = get_phone_numbers(request, file_id)
            phone_numbers = json.loads(response.content).get("phone_numbers", [])

            if response.status_code == 200:
                print(file_id, message, phone_numbers)

            if not phone_numbers:
                return JsonResponse({"error": "No phone numbers found in the file."}, status=400)

            # ✅ Send messages via API
            results = []
            for phone_number in phone_numbers:
                url = f"https://whatsapp.myappstores.com/api/sendText?token={INSTANCE_ID}&phone={phone_number}&message={message}"
                response = requests.get(url)
                results.append({"phone_number": phone_number, "status": "Sent" if response.status_code == 200 else "Failed"})

            return JsonResponse({"results": results})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
