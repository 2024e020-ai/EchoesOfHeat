"""
Django settings for config project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv  # ←追加

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# --- 【追加】.envファイルを読み込む ---
load_dotenv(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")  # ←.envから取得

# --- 【修正】本番環境ではFalseに設定（教員提出用） ---
DEBUG = os.getenv("DEBUG") == "True"  # ←.envから取得してTrue/Falseに変換

# --- 【修正】全ての接続を許可（Render等で動かすため） ---
ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bootstrap5",
    "records",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # --- 【重要】本番でCSSを正しく表示するためのミドルウェアを追加 ---
    "whitenoise.middleware.WhiteNoiseMiddleware", 
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
# --- 【重要】本番環境で静的ファイルを収集する設定 ---
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# WhiteNoiseが効率的に静的ファイルを配信するための設定
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- ログイン・ログアウト設定 ---
LOGIN_REDIRECT_URL = 'list'
LOGOUT_REDIRECT_URL = 'login'
