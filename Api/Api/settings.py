from pathlib import Path
import environ
import os




# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# No início do arquivo
print("✅ settings.py: Iniciando carregamento...")

# Após definir BASE_DIR
print(f"✅ BASE_DIR definido como: {BASE_DIR}")

# Após SECRET_KEY
print("✅ SECRET_KEY carregada")

# Após DATABASES
print("✅ DATABASES configurado")


# Inicializa o leitor de .env
env = environ.Env(
    DEBUG=(bool, False),
   
)
# Tenta ler o .env, mas não falha se não existir
try:
    environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
except Exception as e:
    print(f"[WARN] Não foi possível carregar .env: {e}")  # Certifique-se de que o .env está na raiz do projeto

# Segurança
SECRET_KEY = env("SECRET_KEY", default="django-insecure-fallback-key")
DEBUG = env.bool("DJANGO_DEBUG", default=False)

# Hosts permitidos (separados por vírgula no .env)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["*"])

# Aplicativos instalados
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'User',
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # corsheaders precisa vir antes do CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# URLS
ROOT_URLCONF = 'Api.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Api.wsgi.application'

# Banco de dados
DATABASE_URL = env("DATABASE_URL", default=None)

if DATABASE_URL:
    DATABASES = {"default": env.db()}
else:
    # fallback seguro para ambiente sem banco conectado
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "fallback.sqlite3",
        }
    }

# Modelo de usuário customizado
AUTH_USER_MODEL = 'User.CustomUser'

# Validações de senha
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

# Internacionalização
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True




STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'




# ID padrão para chaves primárias
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === FORÇA STATIC_ROOT (Correção Garantida) ===
import os
from pathlib import Path

# Garante BASE_DIR como Path
if 'BASE_DIR' not in globals():
    BASE_DIR = Path(__file__).resolve().parent.parent

# Força STATIC_ROOT como string absoluta
STATIC_ROOT = str(BASE_DIR / 'static')

# Cria a pasta se não existir
os.makedirs(STATIC_ROOT, exist_ok=True)

print("✅ 6. Definindo STATIC_ROOT...")
try:
    STATIC_URL = '/static/'
    STATIC_ROOT = str(BASE_DIR / 'static')
    print(f"✅ 7. STATIC_ROOT definido como: {STATIC_ROOT}")
except Exception as e:
    print(f"❌ ERRO ao definir STATIC_ROOT: {e}")
# ==============================================