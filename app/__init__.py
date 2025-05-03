from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={
        r"/*": {
            "origins": ["http://localhost:3000"],  # Add your frontend URL
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Range", "X-Content-Range"],
            "supports_credentials": True
        }
    })
    
    app.config.from_object(Config)
    app.config["JWT_SECRET_KEY"] = "5102ad71b95321363456e143ee0460778832a3d25144e5e4921f99a5b04c61bc"
    
    db.init_app(app)
    jwt.init_app(app)
    
    with app.app_context():
        from app.routes import bp  # Import the Blueprint
        app.register_blueprint(bp, url_prefix="/auth")  # Register the Blueprint with a prefix
        db.create_all()
    
    return app
