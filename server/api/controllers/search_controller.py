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

from scrapers.olx_spyder import scrape_olx

def search_products():
    search_term = request.json.get('searchTerm')
    logger.debug(f"Received search request for term: {search_term}")
    
    if not search_term:
        return jsonify({'error': 'No search term provided'}), 400

    try:
        try:
            olx_results = scrape_olx(search_term)
            logger.debug(f"OLX results: {len(olx_results)} items")
            return jsonify({'olx': olx_results})
        except Exception as e:
            logger.error(f"OLX scraper error: {str(e)}")
            return jsonify({'olx': []})
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500
