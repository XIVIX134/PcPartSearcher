from flask import Flask
from api.routes.badr_route import badr_bp
from api.routes.olx_route import olx_bp
from api.routes.sigma_route import sigma_bp



app = Flask(__name__)

# Register blueprints
app.register_blueprint(badr_bp, url_prefix='/badr')
app.register_blueprint(olx_bp, url_prefix='/olx')
app.register_blueprint(sigma_bp, url_prefix='/sigma')
