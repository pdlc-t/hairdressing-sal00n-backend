import os
from pathlib import Path

# Ścieżka do katalogu głównego projektu (jeden poziom wyżej niż ten plik)
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')

    # Jeżeli DATABASE_URI jest ustawione w środowisku, użyj jego wartości,
    # w przeciwnym razie zapisz plik app.db w katalogu głównym projektu
    SQLALCHEMY_DATABASE_URI = (
            os.environ.get('DATABASE_URI')
            or f"sqlite:///{PROJECT_ROOT / 'app.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False  # pozwala na prawidłowe polskie znaki
    JSON_SORT_KEYS = False  # zachowaj oryginalną kolejność pól

    # Stosowane np. do generowania testowego tokena lub fallback
    API_TOKEN = os.environ.get('API_TOKEN', 'Niger')
