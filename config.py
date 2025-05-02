import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Use SQLite database file at flask_app/app.db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') \
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False  # ważne: pozwala na prawidłowe polskie znaki
    JSON_SORT_KEYS = False  # opcjonalnie: zachowaj oryginalną kolejność pól
    API_TOKEN = os.environ.get('API_TOKEN', 'Niger')