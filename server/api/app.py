from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

# Update CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "max_age": 3600
    }
})

@app.errorhandler(Exception)
def handle_error(error):
    print(f"An error occurred: {error}")
    return jsonify({
        "error": "Internal server error",
        "message": str(error)
    }), 500

# Register blueprints with debug logging
logger.debug("Registering blueprints...")
app.register_blueprint(search_bp, url_prefix='/api')
app.register_blueprint(olx_bp, url_prefix='/api/olx')
app.register_blueprint(sigma_bp, url_prefix='/api/sigma')
app.register_blueprint(badr_bp, url_prefix='/api/badr')

@app.route('/debug-routes', methods=['GET'])
def list_routes():
    """Debug endpoint to list all registered routes"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'path': str(rule)
        })
    return jsonify(routes)

logger.debug(f"Registered routes: {[rule.rule for rule in app.url_map.iter_rules()]}")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
