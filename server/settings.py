from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9d722(ztrc1a=d-(1zq-mdnh_392lqey_dep=mpc82!abec5_x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  

ALLOWED_HOSTS = ['*']  

CORS_ALLOW_ALL_ORIGINS = True  
CSRF_TRUSTED_ORIGINS = ["*"]  

CSRF_COOKIE_SECURE = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party 
    'corsheaders',
    'django_bootstrap5',  # Bootstrap Styles
    'widget_tweaks',  # Styling forms with Bootstrap
    # locals 
    'accounts.apps.AccountsConfig',  # Registration
    'Nur.apps.NurConfig',  # Base Application
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Required for admin
    'django.middleware.cache.UpdateCacheMiddleware',         # Caching middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',      # Caching middleware
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Required for admin
    'django.contrib.messages.middleware.MessageMiddleware',      # Required for admin
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Password Hash for security of User's
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
]

CSRF_TRUSTED_ORIGINS = [
    "https://barakat-crm.onrender.com", 
]

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Specify custom template directories
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

WSGI_APPLICATION = 'server.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
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
TIME_ZONE = 'Asia/Dushanbe' 
USE_I18N = True
USE_TZ = True

# Custom User Model
AUTH_USER_MODEL = 'Nur.CustomUser'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Local static files directory
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory to collect static files for production
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False 
EMAIL_HOST_USER = 'siddikme.o7@gmail.com'
EMAIL_HOST_PASSWORD = 'josj pbqw vdcq mnyc' 
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Authentication redirect settings
LOGIN_URL = 'login'  # URL for the login page
LOGIN_REDIRECT_URL = "home"  # URL after successful login
LOGOUT_REDIRECT_URL = "login"  # URL after logout  

# Caching configuration
# Using Memcached
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': BASE_DIR / 'django_cache',
#         #'LOCATION': '127.0.0.1:11211', 
#     }
# }

# Cache timeout settings
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600  # Cache for 10 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'barakat_crm'

# Session caching
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
