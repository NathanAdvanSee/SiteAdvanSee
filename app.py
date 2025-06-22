# app.py (updated)
import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

#ROTAS----------------------------------------------------
from server.rotas_raiz.rotas_autenticar.auth_rt import login_required, register_user, verify_user
from server.rotas_raiz.raiz_rt import raiz_bp
from server.rotas_raiz.login_rt import login_bp
from server.rotas_raiz.register_rt import register_bp
from server.rotas_raiz.logout_rt import logout_bp
from server.rotas_raiz.main_rt import main_bp # NEW: Import the main blueprint
#---------------------------------------------------------

from server.Config.Config import Config
from flask import Flask, session, redirect, url_for, render_template, flash
from flask_jwt_extended import JWTManager
from server.Database.modelo_base_dados import db # Import db object

def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__,
                static_folder='server\\templates\\static',  # Define a pasta estática
                template_folder='server\\templates') # Define a pasta de templates
    app.config.from_object(Config)

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    jwt = JWTManager(app)

    app.register_blueprint(raiz_bp, url_prefix='/')
    app.register_blueprint(login_bp, url_prefix='/')
    app.register_blueprint(register_bp, url_prefix='/')
    app.register_blueprint(logout_bp, url_prefix='/')
    app.register_blueprint(main_bp, url_prefix='/') # NEW: Register the main blueprint
    return app

if __name__ == '__main__':
    app = create_app()
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)