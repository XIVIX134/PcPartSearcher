from flask import Blueprint
from server.api.controllers.sigma.sigma_controller import get_sigma

sigma_bp = Blueprint('sigma', __name__)

sigma_bp.route('/items', methods=['GET'])(get_sigma)
