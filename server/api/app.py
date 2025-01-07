from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Update the path to be relative to the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from server.api.routes.olx.olx_route import olx_bp
from server.api.routes.sigma.sigma_route import sigma_bp
from server.api.routes.general_search.search_route import search_bp
from server.api.routes.badr.badr_route import badr_bp  
from server.api.routes.amazon.amazon_route import amazon_bp  

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
app.register_blueprint(amazon_bp, url_prefix='/api/amazon')

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
