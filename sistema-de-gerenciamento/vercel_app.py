import os
import sys
from pathlib import Path

# Adicionar o diretório atual ao Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gerenciamento_2.settings')

# Importar Django após configurar o path
import django
django.setup()

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()