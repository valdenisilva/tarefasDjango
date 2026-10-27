"""Configuração didática para execução local dos encontros 7, 8 e 9."""
from pathlib import Path

# Pasta que contém manage.py. Evita caminhos específicos de um computador.
BASE_DIR = Path(__file__).resolve().parent.parent
# Chave exclusiva do laboratório local. Não usar em produção.
SECRET_KEY = 'django-laboratorio-local-sem-dados-reais'
# Exibe detalhes de erro durante o laboratório. Não é configuração de produção.
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
# Inclui recursos nativos e nosso app. Sem tarefas, os models não são descobertos.
INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth',
    'django.contrib.contenttypes', 'django.contrib.sessions',
    'django.contrib.messages', 'django.contrib.staticfiles', 'tarefas',
]
# Processam cada requisição: sessão, CSRF, usuário e mensagens, entre outros.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'config.urls'
# DIRS localiza templates do projeto. APP_DIRS também busca dentro dos apps.
# Context processors disponibilizam request, user e messages no HTML.
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]
WSGI_APPLICATION = 'config.wsgi.application'
# SQLite funciona em um arquivo local, sem instalar um servidor de banco.
DATABASES = {'default': {
    'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3',
}}
# Regras nativas usadas na criação e alteração de senhas.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
# Idioma das mensagens nativas e fuso usado pelo projeto.
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
# runserver serve o CSS em modo de desenvolvimento.
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Nomes das rotas de autenticação e dos destinos após entrar e sair.
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'tarefas:lista'
LOGOUT_REDIRECT_URL = 'login'
