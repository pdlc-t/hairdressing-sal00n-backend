from flask import Blueprint

bp = Blueprint('services', __name__)

from app.main.services import routes