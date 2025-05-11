# app/__init__.py

from flask import Flask
from flask_cors import CORS

from config import Config
from app.extensions import db
from app.json_provider import CustomJSONProvider

# temporarily as there is not blueprint importing client yet
from app.main.models.client import Client

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # podmieniamy provider
    app.json_provider_class = CustomJSONProvider
    # po stworzeniu instancji JSONProvider:
    app.json = app.json_provider_class(app)
    # pozwól na CORS ze wszystkich domen (lub tylko z 3000)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    # inicjalizacja rozszerzeń
    db.init_app(app)

    # rejestracja blueprintów
    from app.main.hairdressers import bp as hairdressers_bp
    app.register_blueprint(hairdressers_bp, url_prefix='/hairdressers')
    from app.main.services import bp as services_bp
    app.register_blueprint(services_bp, url_prefix='/services')
    from app.main.products import bp as products_bp
    app.register_blueprint(products_bp, url_prefix='/products')

    from app.main.appointments import bp as appointments_bp
    app.register_blueprint(appointments_bp, url_prefix='/appointments')

    from app.main.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    with app.app_context():
        # tworzymy tabele jeśli nie istnieją
        db.create_all()

        # **Import i wywołanie seedowania**
        from app import seed
        seed.seed_database()

    return app
