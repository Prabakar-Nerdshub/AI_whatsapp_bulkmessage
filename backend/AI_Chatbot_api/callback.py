from django.http import JsonResponse

def webhook_verification(request):
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == "1234567890":
            return JsonResponse(int(challenge), safe=False)
        else:
            return JsonResponse({"error": "Invalid token"}, status=403)
