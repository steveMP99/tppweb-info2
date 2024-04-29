from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import current_app

mysql = SQLAlchemy()


def start_app():
    app = Flask(__name__)
    
    # Configuration JWT
    app.config['JWT_SECRET_KEY'] = 'info2-tp'
    jwt = JWTManager(app)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/user_auth_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    mysql.init_app(app)
    
    
    # Import des routes principales
    from .main.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Import des routes pour la auth
    from .auth.routes import auth_bp
    from .chat.routes import chat_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    
    return app