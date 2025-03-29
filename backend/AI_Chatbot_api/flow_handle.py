from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Disable CSRF for testing (use proper authentication in production)
def submit_selection(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON from the request
            selected_option = data.get('Senaria_Pilihan_3e04aa', None)

            if selected_option:
                # Process the selected option (e.g., save to database, trigger workflow)
                response_data = {
                    "status": "success",
                    "message": f"Selection received: {selected_option}"
                }
                return JsonResponse(response_data, status=200)
            else:
                return JsonResponse({"status": "error", "message": "Invalid selection"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
