"""
Django settings for projetosite project.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ Use sua SECRET_KEY atual (mantive a que você já tinha):
SECRET_KEY = 'django-insecure-c%*%-uo78cu-%n6#!=sr4(b&scmc24fvs4np6)sn)=r1!!98*%'

DEBUG = True
ALLOWED_HOSTS: list[str] = []

# ===== Jazzmin (tema do admin) =====
JAZZMIN_SETTINGS = {
    "site_title": "Admin Academia",
    "site_header": "Academia & Aulas",
    "site_brand": "Academia",
    "welcome_sign": "Bem-vindo ao painel",

    # (opcionais) coloque os arquivos em static/website/img/
    "site_logo": "website/img/logo.png",
    "login_logo": "website/img/logo.png",
    "login_logo_dark": "website/img/logo.png",
    "site_icon": "website/img/favicon.png",

    # Ícones
    "icons": {
        "website.Plano": "fas fa-tags",
        "website.Modalidade": "fas fa-dumbbell",
        "website.Professor": "fas fa-chalkboard-teacher",
        "website.Aluno": "fas fa-user-graduate",
        "website.Turma": "fas fa-users",
        "website.Matricula": "fas fa-id-badge",
        "website.Exercicio": "fas fa-bolt",
        "website.Treino": "fas fa-clipboard-list",
        "website.TreinoExercicio": "fas fa-list-ol",
        "website.Presenca": "fas fa-check-circle",
        "website.AvaliacaoFisica": "fas fa-weight",
        "website.Pagamento": "fas fa-receipt",
    },

    # Ordem (opcional)
    "order_with_respect_to": [
        "website", "website.Plano", "website.Modalidade", "website.Professor",
        "website.Aluno", "website.Turma", "website.Matricula",
        "website.Treino", "website.Exercicio", "website.TreinoExercicio",
        "website.Presenca", "website.AvaliacaoFisica", "website.Pagamento",
    ],

    # Seu CSS custom (caminho relativo a /static/)
    "custom_css": ["website/css/admin.css"],
    # "custom_js": ["website/js/admin.js"],
}

# Ajustes visuais do Jazzmin
JAZZMIN_UI_TWEAKS = {
    "theme": "default",                 # experimente: "flatly" (claro) ou "darkly" (escuro)
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-primary",
    "brand_colour": "navbar-dark",
    "accent": "accent-info",
    "navbar_fixed": True,
    "sidebar_fixed": True,
    "actions_sticky_top": True,
}

# ===== Apps =====
INSTALLED_APPS = [
    "jazzmin",  # sempre antes do admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "website",
]

# ===== Middleware =====
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "projetosite.urls"

# ===== Templates =====
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # sua pasta templates/
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

WSGI_APPLICATION = "projetosite.wsgi.application"

# ===== Database =====
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ===== Password validators (padrão) =====
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ===== i18n =====
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ===== Static files =====
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # pasta global de estáticos

# ===== Default PK =====
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
