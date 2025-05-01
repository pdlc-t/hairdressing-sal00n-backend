from flask import Blueprint

bp = Blueprint('products', __name__)

from app.main.products import routes