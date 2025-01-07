from flask import Blueprint
from server.api.controllers.badr.badr_controller import get_badr

badr_bp = Blueprint('badr', __name__)

badr_bp.route('/cpus', methods=['GET'])(get_badr)

