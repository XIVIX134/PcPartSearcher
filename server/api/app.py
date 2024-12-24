from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import sys

# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from api.routes.olx_route import olx_bp
from api.routes.sigma_route import sigma_bp
from api.routes.search_route import search_bp
from api.routes.badr_route import badr_bp  # Add badr_route import

def get_allowed_origins():
    if app.debug:
        # In development, allow all origins
        return "*"
    # In production, return specific origins
    return ['https://your-production-domain.com']

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Increase Flask's timeout
app.config['PERMANENT_SESSION_LIFETIME'] = 600  # 10 minutes

# Configure CORS before registering blueprints
CORS(app, 
     resources={r"/*": {
         "origins": "*",  # Allow all origins in development
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"],
         "expose_headers": ["Content-Type"],
         "supports_credentials": False,  # Must be False when using '*' origin
         "max_age": 600  # Cache preflight requests for 10 minutes
     }})

@app.after_request
def after_request(response):
    # Ensure all responses have CORS headers
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.errorhandler(Exception)
def handle_error(error):
    print(f"An error occurred: {error}")
    return jsonify({
        "error": "Internal server error",
        "message": str(error)
    }), 500

# Register blueprints
app.register_blueprint(olx_bp, url_prefix='/olx')
app.register_blueprint(sigma_bp, url_prefix='/sigma')
app.register_blueprint(badr_bp, url_prefix='/badr')  # Register badr blueprint
app.register_blueprint(search_bp)  # No url_prefix for search
