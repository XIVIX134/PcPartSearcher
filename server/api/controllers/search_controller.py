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
        data = request.get_json()
        search_term = data.get('searchTerm')
        
        if not search_term:
            return jsonify({'error': 'No search term provided'}), 400

        try:
            from scrapers.olx_spyder import scrape_olx
            # Get all results at once
            all_results = scrape_olx(search_term)
            
            logger.debug(f"Total OLX results: {len(all_results)} items")
            
            return jsonify({
                'olx': all_results,
                'badr': [],
                'totalPages': len(all_results) // 24 + (1 if len(all_results) % 24 > 0 else 0),
                'itemsPerPage': 24
            })
        except Exception as e:
            logger.error(f"OLX scraper error: {str(e)}")
            return jsonify({'olx': [], 'badr': [], 'totalPages': 0, 'itemsPerPage': 24})
            
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500
