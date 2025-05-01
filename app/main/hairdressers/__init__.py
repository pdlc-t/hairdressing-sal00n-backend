from flask import Blueprint
bp = Blueprint('hairdressers', __name__)
from app.main.hairdressers import routes
