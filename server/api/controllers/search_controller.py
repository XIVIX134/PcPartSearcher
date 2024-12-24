from flask import request, jsonify
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.insert(0, project_root)

def search_products():
    try:
        if request.method == 'OPTIONS':
            # Handle preflight request
            response = jsonify({'status': 'ok'})
            return response

        data = request.get_json()
        search_term = data.get('searchTerm') if data else None
        
        logger.debug(f"Received search request for term: {search_term}")
        
        if not search_term:
            return jsonify({'error': 'No search term provided'}), 400

        try:
            from scrapers.olx_spyder import scrape_olx
            olx_results = scrape_olx(search_term)
            logger.debug(f"OLX results: {len(olx_results)} items")
            return jsonify({
                'olx': olx_results,
                'badr': []  # Add empty badr results for now
            })
        except Exception as e:
            logger.error(f"OLX scraper error: {str(e)}")
            return jsonify({'olx': [], 'badr': []})
            
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500
