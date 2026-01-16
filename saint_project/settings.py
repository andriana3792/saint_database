from pathlib import Path
import os
import pymysql
from dotenv import load_dotenv

# ======================
# Environment
# ======================

load_dotenv()

# Use PyMySQL as MySQLdb
pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent


def split_csv_env(name: str) -> list[str]:
    """Split comma-separated env vars safely."""
    return [x.strip() for x in os.getenv(name, "").split(",") if x.strip()]


# ======================
# Core settings
# ======================

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in the environment")

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")


# ======================
# Hosts & CSRF
# ======================

if DEBUG:
    # Local development
    ALLOWED_HOSTS = [
        "localhost",
        "127.0.0.1",
        "[::1]",
    ]
    CSRF_TRUSTED_ORIGINS = []
else:
    # Production
    ALLOWED_HOSTS = split_csv_env("ALLOWED_HOSTS")
    CSRF_TRUSTED_ORIGINS = split_csv_env("CSRF_TRUSTED_ORIGINS")


# ======================
# Media
# ======================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ======================
# Security
# ======================

if DEBUG:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
else:
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_AGE = 1800  # 30 minutes
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_SAVE_EVERY_REQUEST = True

    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True

    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"


# ======================
# Applications
# ======================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "saints.apps.SaintsConfig",
    "multiselectfield",
]


# ======================
# Middleware
# ======================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ======================
# URLs / WSGI
# ======================

ROOT_URLCONF = "saint_project.urls"
WSGI_APPLICATION = "saint_project.wsgi.application"


# ======================
# Templates
# ======================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # project-level templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ======================
# Database (MySQL)
# ======================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "3306"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        },
    }
}


# ======================
# Password validation
# ======================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ======================
# Internationalization
# ======================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Nicosia"
USE_I18N = True
USE_TZ = True


# ======================
# Static files
# ======================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / "static"]


# ======================
# Defaults
# ======================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
