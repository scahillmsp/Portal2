import os
from pathlib import Path

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-very-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Change to False in production

ALLOWED_HOSTS = []  # Add your production domain or IP here

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',  # Your custom app for the webshop
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'excavator_parts_shop.urls'

# Templates: Add the path to your template directories here
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Custom template folder
        'APP_DIRS': True,  # Looks for templates within each app
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

WSGI_APPLICATION = 'excavator_parts_shop.wsgi.application'

# Database: Using SQLite for development, adjust for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'  # This defines the URL prefix for static files

# Directory where Django will look for static files
STATICFILES_DIRS = [BASE_DIR / 'static']  # Ensure you have this folder in your project root

# Media files (uploads like product images)
MEDIA_URL = '/media/'  # Defines the base URL for media files (images)
MEDIA_ROOT = BASE_DIR / 'media'  # Directory on the filesystem where media is stored

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django's collectstatic command will collect static files into this directory (for production)
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Only needed when running collectstatic for production

# For development debugging purposes
if DEBUG:
    INTERNAL_IPS = ['127.0.0.1']
