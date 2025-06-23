from pathlib import Path
import environ
import os
from datetime import timedelta

# BASE_DIR / 環境変数の読み込み
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# セキュリティ設定
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

# アプリケーション定義
INSTALLED_APPS = [
    # Django 標準
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 外部ライブラリ
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',  # dj-rest-auth 用
    'corsheaders',

    # 認証関連
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth',
    'dj_rest_auth.registration',

    # 自作アプリ
    'users',
    'notes',
]

SITE_ID = 1

# 認証バックエンド
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# allauth 完全設定（Google OAuth2対応）
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True

# HTTPプロトコル設定（OAuth2で重要）
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http' if DEBUG else 'https'

# Google OAuth2 設定（完全修正版）
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
        'VERIFIED_EMAIL': True,
        'VERSION': 'v2',
        'APP': {
            'client_id': env('GOOGLE_OAUTH2_CLIENT_ID', default='995866888869-8398ivqlc5cjef3jrhtstp5nc6o3put7.apps.googleusercontent.com'),
            'secret': env('GOOGLE_OAUTH2_CLIENT_SECRET', default=''),
            'key': ''
        }
    }
}

# ソーシャルアカウント追加設定
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_QUERY_EMAIL = True

# ミドルウェア
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORSは CommonMiddleware の前に配置
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # 最後に配置
]

# URL / WSGI
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# テンプレート設定（allauth用）
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # allauth用
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# PostgreSQLデータベース設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB', default='notelog_db'),
        'USER': env('POSTGRES_USER', default='postgres'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST', default='localhost'),
        'PORT': env('POSTGRES_PORT', default='5432'),
        'OPTIONS': {
            'connect_timeout': 10,
        },
        'CONN_MAX_AGE': 0,  # 接続プーリング無効（開発環境）
    }
}

# パスワードバリデーション
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# タイムゾーンと言語
LANGUAGE_CODE = 'ja'
TIME_ZONE = env('TIME_ZONE', default='Asia/Tokyo')
USE_I18N = True
USE_TZ = True

# 静的ファイル設定
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []

# メディアファイル設定（画像アップロード用）
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ファイルアップロード制限
FILE_UPLOAD_MAX_MEMORY_SIZE = env.int('FILE_UPLOAD_MAX_MEMORY_SIZE', default=5242880)  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = env.int('DATA_UPLOAD_MAX_MEMORY_SIZE', default=5242880)  # 5MB
FILE_UPLOAD_PERMISSIONS = 0o644

# カスタムユーザーモデル
AUTH_USER_MODEL = 'users.User'

# Django REST Framework + JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # Admin用
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Simple JWT設定（環境変数対応）
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=env.int('JWT_ACCESS_TOKEN_LIFETIME', default=60)),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=env.int('JWT_REFRESH_TOKEN_LIFETIME', default=1440)),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# dj-rest-auth設定（Google OAuth2対応）
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_HTTPONLY': False,  # SPAなのでFalse
    'JWT_AUTH_RETURN_EXPIRATION': True,
    'JWT_AUTH_COOKIE': None,
    'REGISTER_SERIALIZER': 'users.serializers.CustomRegisterSerializer',
    'OLD_PASSWORD_FIELD_ENABLED': True,
    'LOGOUT_ON_PASSWORD_CHANGE': False,
    'PASSWORD_RESET_USE_EMAIL': True,
    'SESSION_LOGIN': False,  # JWT使用時はFalse
}

# CORS設定（完全版）
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:8000',
    'http://127.0.0.1:8000'
])
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# CSRF設定（SPA対応）
CSRF_TRUSTED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:8000',
    'http://127.0.0.1:8000'
])
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False

# セキュリティ設定（本番環境用）
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# セッション設定
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = env.int('SESSION_COOKIE_AGE', default=1209600)  # 2週間
SESSION_COOKIE_NAME = 'notelog_sessionid'
SESSION_SAVE_EVERY_REQUEST = env.bool('SESSION_SAVE_EVERY_REQUEST', default=False)
SESSION_EXPIRE_AT_BROWSER_CLOSE = env.bool('SESSION_EXPIRE_AT_BROWSER_CLOSE', default=False)

# メール設定（開発・本番対応）
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
if EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
    EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = env.int('EMAIL_PORT', default=587)
    EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
    EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
    DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)

# 国際化設定
LANGUAGE_CODE = 'ja'
LANGUAGES = [
    ('ja', 'Japanese'),
    ('en', 'English'),
]
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# 自動フィールド
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 内部IPs（デバッグ用）
INTERNAL_IPS = env.list('INTERNAL_IPS', default=['127.0.0.1', 'localhost'])

# ログ設定（OAuth2デバッグ用）
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'INFO',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.utils.autoreload': {
            'handlers': [],
            'level': 'WARNING',
            'propagate': False,
        },
        'allauth': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',  # OAuth2デバッグ用
            'propagate': False,
        },
        'dj_rest_auth': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',  # REST APIデバッグ用
            'propagate': False,
        },
        'users': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'notes': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

# ログディレクトリ作成
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# キャッシュ設定（将来のパフォーマンス向上用）
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# 本番環境でのRedisキャッシュ
if env('REDIS_URL', default=None):
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': env('REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }

# データベースルーティング（将来の読み書き分離用）
DATABASE_ROUTERS = []

# API設定
API_VERSION = env('API_VERSION', default='v1')
API_TITLE = env('API_TITLE', default='Notelog API')
API_DESCRIPTION = env('API_DESCRIPTION', default='Personal Knowledge Management Platform API')

# セキュリティヘッダー（追加）
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

# パフォーマンス設定
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000