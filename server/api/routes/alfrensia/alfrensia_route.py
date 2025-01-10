from flask import Blueprint
from server.api.controllers.alfrensia.alfrensia_controller import Alfrensia_Search

alfrensia_bp = Blueprint('alfrensia', __name__)

alfrensia_bp.route('/search', methods=['POST', 'OPTIONS'])(Alfrensia_Search)
