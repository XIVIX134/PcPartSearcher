from flask import Blueprint
from api.controllers.badr_controller import cpus

badr_bp = Blueprint('badr', __name__)

badr_bp.route('/cpus', methods=['GET'])(cpus)

