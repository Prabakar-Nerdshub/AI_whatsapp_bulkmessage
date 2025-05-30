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
# backend/urls.py

from django.contrib import admin
from django.urls import path, include
from AI_Chatbot_api.whatsapp_flow_handler import webhook  # Import webhook directly
from AI_Chatbot_api.custom_flowTemp import webhook1

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include('AI_Chatbot_api.urls')),  # Ensure API routes are included
    path("webhook", webhook, name="webhook_direct"),  # Add direct webhook path
    path("webhook/", webhook, name="webhook_direct_slash"),  # Add with trailing slash too
    path("webhook1", webhook1, name="webhook1_direct"),  # Add direct webhook path
    path("webhook1/", webhook1, name="webhook1_direct_slash"),  # Add with trailing slash too
]
