from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# Flask eklentileri
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Eklentileri başlat
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Login manager ayarları
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Bu sayfaya erişmek için giriş yapmalısınız.'
    login_manager.login_message_category = 'info'
    
    # Blueprint'leri kaydet
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from app.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app

from app import models 