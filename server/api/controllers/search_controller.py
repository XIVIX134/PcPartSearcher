from flask import request, jsonify, make_response
from flask_cors import cross_origin
import os
import sys
import logging
import traceback

# Configure logging with more details
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, project_root)

@cross_origin()
def search_products():
    try:
        logger.info("Received search request")
        
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            return response

        if not request.is_json:
            logger.error("Request is not JSON")
            return jsonify({'error': 'Request must be JSON'}), 400

        data = request.get_json()
        logger.info(f"Request data: {data}")
        
        search_term = data.get('searchTerm')
        if not search_term or not isinstance(search_term, str):
            raise ValueError("Invalid or missing searchTerm")

        from scrapers.olx.olx_spyder import scrape_olx
        logger.debug("Calling scrape_olx now...")
        results = scrape_olx(search_term)
        logger.debug(f"Scrape returned {len(results)} results")
        
        response_data = {
            'olx': results,
            'badr': [],
            'totalPages': len(results) // 24 + (1 if len(results) % 24 > 0 else 0),
            'itemsPerPage': 24,
            'status': 'success'
        }
        
        logger.info(f"Search completed successfully. Found {len(results)} results")
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error in search_products: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': 'Search failed',
            'message': str(e)
        }), 500
