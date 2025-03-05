"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# AI_Chatbot_api/urls.py

from django.urls import path
from .views import get_csrf_token, upload_file, get_phone_numbers
from .views import send_whatsapp_message


urlpatterns = [
    path("csrf/", get_csrf_token, name="csrf_token"),
    path('upload', upload_file, name='upload_file'),
    path("get_phone_numbers/<str:file_id>/", get_phone_numbers, name='get_phone_numbers'),
    path("send_whatsapp_message", send_whatsapp_message, name="send_whatsapp_message"),
]


