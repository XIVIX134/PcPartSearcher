from flask import Flask
from flask_cors import CORS
import os
import sys

# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from api.routes.olx_route import olx_bp
from api.routes.sigma_route import sigma_bp
from api.routes.search_route import search_bp

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "supports_credentials": True
    }
})

# Register blueprints
app.register_blueprint(olx_bp, url_prefix='/olx')
app.register_blueprint(sigma_bp, url_prefix='/sigma')
app.register_blueprint(search_bp, url_prefix='')  # Changed to empty prefix
