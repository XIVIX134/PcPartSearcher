from flask import Blueprint
from ..controllers.search_controller import search_products

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search', methods=['POST', 'OPTIONS'])
def do_search():
    return search_products()
