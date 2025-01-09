from flask import request, jsonify, make_response
from flask_cors import cross_origin
import os
import sys
import logging
import traceback
from scrapers.olx.olx_spyder import OLX_Spyder
from scrapers.sigma.sigma_spyder import SigmaSpyder
from scrapers.amazon.amazon_spyder import AmazonSpyder  # Add this import

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
        
        ####### Validate request data #######
        
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
        source_filters = data.get('sourceFilters', {})

        if not search_term or not isinstance(search_term, str):
            raise ValueError("Invalid or missing searchTerm")

        results = {
            'olx': [],
            'badr': [],
            'sigma': [],
            'amazon': [],
        }

        # Only scrape enabled sources
        if source_filters.get('olx'):
            olx_spyder = OLX_Spyder(search_term)
            results['olx'] = olx_spyder.scrape()

        if source_filters.get('sigma'):
            sigma_spyder = SigmaSpyder(search_term)
            sigma_results = sigma_spyder.scrape()
            transformed_sigma = []
            for item in sigma_results or []:
                transformed_sigma.append({
                    'Product ID': item.get('link', '').split('/')[-1],
                    'Title': item.get('title', ''),
                    'Price': item.get('price_new', ''),
                    'Location': 'Sigma Computer',
                    'Image URL': item.get('image', ''),
                    'Details Link': item.get('link', ''),
                    'Description': item.get('description', ''),
                    'stock': item.get('stock', 'Unknown')  # Add stock info
                })
            results['sigma'] = transformed_sigma

        if source_filters.get('amazon'):
            amazon_spyder = AmazonSpyder()
            amazon_raw_results = amazon_spyder.scrap(search_term)
            transformed_amazon = []
            for item in amazon_raw_results:
                transformed_amazon.append({
                    'Product ID': 'AMZ-' + str(hash(item['title']))[:8],
                    'Title': item['title'],
                    'Price': item['price'],
                    'Location': 'Amazon.eg',
                    'Image URL': item['image'],
                    'Details Link': item['link'] or '#',
                    'Description': '',
                    'rating': item['rating'],
                    'stock': 'In Stock'  # Amazon typically only shows in-stock items
                })
            results['amazon'] = transformed_amazon

        ######## Return response ########
        
        total_items = sum(len(items) for items in results.values())
        
        response_data = {
            **results,
            'totalPages': (total_items // 24) + (1 if total_items % 24 > 0 else 0),
            'itemsPerPage': 24,
            'status': 'success'
        }
        
        logger.info(f"Search completed successfully. Found {total_items} results")
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error in search_products: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': 'Search failed',
            'message': str(e)
        }), 500
