# Ponto de entrada WSGI padrão do Django. O aluno usa manage.py runserver no laboratório.
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
