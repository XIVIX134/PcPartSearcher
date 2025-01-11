from flask import Blueprint
import asyncio
from ...controllers.general_search.search_controller import search_products

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search', methods=['POST', 'OPTIONS'])
def do_search():
    return asyncio.run(search_products())
