from flask import Blueprint
from api.controllers.olx_controllers import get_olx

olx_bp = Blueprint('olx', __name__)

olx_bp.route('/laptops', methods=['GET'])(get_olx)
