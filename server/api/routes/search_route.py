from flask import Blueprint
from api.controllers.search_controller import search_products

search_bp = Blueprint('search', __name__)

search_bp.route('/search', methods=['POST'])(search_products)
