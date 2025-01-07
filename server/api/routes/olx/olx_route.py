from flask import Blueprint
from server.api.controllers.olx.olx_controllers import get_olx

olx_bp = Blueprint('olx', __name__)

olx_bp.route('/laptops', methods=['GET'])(get_olx)
