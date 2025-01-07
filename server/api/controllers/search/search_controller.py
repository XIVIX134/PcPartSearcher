from flask import request, jsonify, make_response
from flask_cors import cross_origin
import os
import sys
import logging
import traceback
from scrapers.olx.olx_spyder import scrape_olx
from scrapers.sigma.sigma_spyder import scrape_sigma_computer
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

        # Get results from all sources
        olx_results = scrape_olx(search_term)
        sigma_results = scrape_sigma_computer(search_term)
        
        # Get Amazon results
        amazon_raw_results = AmazonSpyder().search_products(search_term)

        # Transform sigma results to match product format
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

        # Transform amazon results to match product format
        transformed_amazon = []
        for item in amazon_raw_results:
            transformed_amazon.append({
                'Product ID': 'N/A',
                'Title': item['title'],
                'Price': item['price'],
                'Location': 'Amazon.eg',
                'Image URL': item['image'],
                'Details Link': item['link'],
                'Description': '',
                'rating': item['rating'],
                'stock': 'In Stock'  # Amazon typically only shows in-stock items
            })
        
        response_data = {
            'olx': olx_results,
            'badr': [],
            'sigma': transformed_sigma,
            'amazon': transformed_amazon,
            'totalPages': (len(olx_results) + len(transformed_sigma) + len(transformed_amazon)) // 24 + 
                        (1 if (len(olx_results) + len(transformed_sigma) + len(transformed_amazon)) % 24 > 0 else 0),
            # 'totalPages': (len(olx_results) + len(transformed_sigma)) // 24 + 
            #             (1 if (len(olx_results) + len(transformed_sigma)) % 24 > 0 else 0),
            'itemsPerPage': 24,
            'status': 'success'
        }
        
        logger.info(f"Search completed successfully. Found {len(olx_results) + len(transformed_sigma)+ len(transformed_amazon)} results")
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error in search_products: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': 'Search failed',
            'message': str(e)
        }), 500
