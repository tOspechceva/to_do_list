import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent / "data"
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data.settings")
django.setup()