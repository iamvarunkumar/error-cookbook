import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file from the project root (where manage.py is)
# This line assumes your .env file is in the same directory as manage.py
load_dotenv(BASE_DIR / '.env') # Corrected path if settings.py is one level down from .env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-h&e)cz7(9hropws#zoww1n^g=c+71^*f#abj@)uik20(yu82xu"



# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG will be True if your .env file has DEBUG=True, otherwise False
DEBUG = 'True'


# ALLOWED_HOSTS
# Reads from .env: ALLOWED_HOSTS=127.0.0.1,localhost,yourdomain.com
# If DEBUG is True and ALLOWED_HOSTS is not set in .env, it defaults to common dev hosts.
ALLOWED_HOSTS_STRING = os.getenv('ALLOWED_HOSTS')
if ALLOWED_HOSTS_STRING:
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STRING.split(',') if host.strip()]
elif DEBUG:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
else:
    ALLOWED_HOSTS = [] # Should be explicitly set in .env for production if DEBUG=False


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main_app', # Assuming your app is named 'main_app' as per your file
    # If you named your app 'cookbook' use:
    # 'cookbook.apps.CookbookConfig',
    # or simply 'cookbook',
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

# Ensure this matches your project's configuration directory name
# If your project config dir is 'error_cookbook_project', this is correct.
# If it's 'error_cookbook_config' (as suggested in my original Sprint 1 setup), change it.
ROOT_URLCONF = 'error_cookbook_project.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # ADD THIS for project-level templates
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

# Ensure this matches your project's configuration directory name
WSGI_APPLICATION = 'error_cookbook_project.wsgi.application'


# Database
# Using SQLite as per your original settings for Sprint 1
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# If you want to use dj_database_url for .env flexibility (recommended later):
# import dj_database_url
# DATABASES = {
#     'default': dj_database_url.config(
#         default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
#         conn_max_age=600
#     )
# }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC' # Consider changing to 'Asia/Kolkata' or your local timezone
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] # ADD THIS for project-level static files


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication URLs (Important for Sprint 1 auth flow)
LOGIN_REDIRECT_URL = '/' # Or a dashboard page e.g., 'cookbook:index'
LOGOUT_REDIRECT_URL = '/' # Or a specific logout page
LOGIN_URL = 'login' # Name of your login URL pattern