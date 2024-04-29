# app/main/routes.py
from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return "Bienvenue sur l'API De Chat"