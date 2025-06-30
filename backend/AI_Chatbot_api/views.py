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
            file_name = request.POST.get("file_name", file.name)  # Retrieve file name from frontend

            # ✅ Validate File Type
            if not file.name.endswith((".csv", ".xls", ".xlsx")):
                return JsonResponse({"error": "Unsupported file format"}, status=400)

            file_id = fs.put(file.read(), filename=file_name)  # Store file with provided name

            return JsonResponse({"message": "File uploaded successfully", "file_id": str(file_id), "file_name": file_name})

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

@csrf_exempt
def file_groups(request):
    try:
        files = db.fs.files.find({}, {"_id": 1, "filename": 1})  # Fetch all uploaded files
        groups = [{"id": str(f["_id"]), "name": f["filename"]} for f in files]
        return JsonResponse({"groups": groups})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_contacts(request, file_id):
    try:
        file_id = file_id.strip()  # Remove leading/trailing spaces
        file_id = file_id.replace("%20", " ")  # Handle URL encoding of spaces

        # ✅ Fetch file by name
        grid_out = db.fs.files.find_one({"filename": file_id})
        if not grid_out:
            return JsonResponse({"error": f"File '{file_id}' not found"}, status=404)

        file_obj_id = grid_out["_id"]  # Extract file ID
        grid_out = fs.get(file_obj_id)  # Get the file from GridFS
        file_content = BytesIO(grid_out.read())

        # ✅ Read CSV/Excel
        if grid_out.filename.endswith(".csv"):
            df = pd.read_csv(file_content)
        else:
            df = pd.read_excel(file_content, engine="openpyxl")

        if df.empty:
            return JsonResponse({"contacts": [], "message": "No contacts found in file."})

        # Convert dataframe to list of dictionaries
        contacts = df.to_dict(orient="records")

        return JsonResponse({"contacts": contacts})

    except Exception as e:
        logger.error(f"Error in get_contacts: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)



# ✅ Send WhatsApp messages via API
@csrf_exempt
def send_whatsapp_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            contacts = data.get("contacts", [])
            
            template_name = data.get("template_name", "sara_list_message") #nerdshub_sara , sara_list_message
            language_code = data.get("language_code", "ms")  # Default to English if not provided
            print("Received template_name:", data.get("template_name"))

            if not contacts:
                return JsonResponse({"error": "No contacts selected"}, status=400)

            ACCESS_TOKEN = "EAAYgHPHSE6MBO4sSEZCcZASaZAYyVtMUj97AR36girXjcHq1Na7Y8aQ6etfaEKImTnrdwcPnx7zZBieBkXWBVISuzgQ9mUBtDGacCaUFbBz5ZAzOcRKZBfuphySmr0Wx3ABNVt23zggR1vhUa4VH0lr6bRihfr0cxdDDGHprL04h9cQLCQKi3RFwZB3SLhJ6DB3egZCHX7WQVam51xiU"
            WHATSAPP_API_URL = "https://graph.facebook.com/v22.0/627644197089809/messages"
            #Nerdshub : https://graph.facebook.com/v22.0/627644197089809/messages
            #custom number : https://graph.facebook.com/v22.0/610411742154061/messages

            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }

            results = []
            for contact in contacts:
                phone_number = str(contact.get("phone_numbers"))
                if not phone_number.isdigit() :
                    results.append({"phone_number": phone_number, "status": "Invalid number"})
                    continue

                phone_number = f"91{phone_number}"
                payload = {
                    "messaging_product": "whatsapp",
                    "to": phone_number,
                    "type": "template",
                    "template": {
                        "name": template_name,
                        "language": {"code": language_code},
                        "components": [
                            {
                                "type": "button",
                                "sub_type": "flow",
                                "index": "0",
                                "parameters": [
                                    {
                                        "type": "payload",
                                        "payload": "1403483110693196"  # Replace with your actual Flow ID 550407894833698,1403483110693196
                                        
                                    }
                                ]
                            }
                        ]
                    }
                }
                
                print(template_name)

                try:
                    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload, timeout=10)
                    response_data = response.json()
                    print(f"WhatsApp API Response for {phone_number}: {json.dumps(response_data, indent=2)}")
                    logger.info(f"Response for {phone_number}: {response_data}")

                    results.append({
                        "phone_number": phone_number,
                        "status": "Sent" if response.status_code == 200 else "Failed",
                        "error": response_data  # Change this line to return full response
                    })

                    print(f"Message sent to {phone_number}: Status - {'Sent' if response.status_code == 200 else 'Failed'}")
                except requests.exceptions.RequestException as req_err:
                    logger.error(f"Network error for {phone_number}: {req_err}")
                    logger.error(f"WhatsApp API Response: {json.dumps(response_data, indent=2)}")
                    results.append({
                        "phone_number": phone_number,
                        "status": "Failed",
                        "error": "Network error or timeout"
                    })

            return JsonResponse({"results": results})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
def fetch_whatsapp_insights(request):
    """
    Fetch WhatsApp Message Insights
    """
    ACCESS_TOKEN = "EAAYgHPHSE6MBO4sSEZCcZASaZAYyVtMUj97AR36girXjcHq1Na7Y8aQ6etfaEKImTnrdwcPnx7zZBieBkXWBVISuzgQ9mUBtDGacCaUFbBz5ZAzOcRKZBfuphySmr0Wx3ABNVt23zggR1vhUa4VH0lr6bRihfr0cxdDDGHprL04h9cQLCQKi3RFwZB3SLhJ6DB3egZCHX7WQVam51xiU"
    HEADERS = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    url = "https://graph.facebook.com/v22.0/627644197089809/message_insights"
    params = {
        "metric": "messages_sent,messages_delivered,messages_received",
        "period": "day"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    return JsonResponse(response.json(), safe=False)
