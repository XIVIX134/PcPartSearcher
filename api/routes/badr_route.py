from flask import Blueprint
from api.controllers.badr_controller import get_badr_items

badr_bp = Blueprint('badr', __name__)

badr_bp.route('/items', methods=['GET'])(get_badr_items)
