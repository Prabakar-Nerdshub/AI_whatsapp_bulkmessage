from pathlib import Path

import os
from dotenv import load_dotenv

load_dotenv()

INSTANCE_ID = os.getenv("WHATSAPP_INSTANCE_ID")

from corsheaders.defaults import default_headers

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = 'django-insecure-8!=_t47*g2ot)x65sbptum8f8n-v_$a2p*xkd0!yq8)!x+cpe1'  # Replace with a secure key for production
DEBUG = True
ALLOWED_HOSTS = ['*']  # Allow all hosts for development

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'AI_Chatbot_api',  # Your chatbot API app
    'corsheaders',  # CORS support
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware should be placed first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS settings
CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Update this if your frontend runs on a different port
]

# URL configuration
ROOT_URLCONF = 'AI_Chatbot.urls'

# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'AI_Chatbot.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files settings
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory where collectstatic will place files
STATICFILES_DIRS = [BASE_DIR / 'backend/static']  # Additional directories to look for static files
STATICFILES_DIRS = [BASE_DIR / 'backend/static'] if os.path.exists(BASE_DIR / 'backend/static') else []

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',  # ✅ Required for file uploads
        'rest_framework.parsers.FormParser',  # ✅ Also helpful for form data
    ]
}

# Add these settings for handling media files (uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
CORS_ALLOW_ALL_ORIGINS = True