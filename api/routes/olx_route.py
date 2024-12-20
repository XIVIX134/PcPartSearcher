from flask import Blueprint
from api.controllers.olx_controllers import get_laptops

badr_bp = Blueprint('olx', __name__)

badr_bp.route('/laptops', methods=['GET'])(get_laptops)
