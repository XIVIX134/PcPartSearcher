from flask import Blueprint
from server.api.controllers.amazon.amazon_search_controller import Amazon_Search

amazon_bp = Blueprint('amazon', __name__)

amazon_bp.route('/search', methods=['POST', 'OPTIONS'])(Amazon_Search)