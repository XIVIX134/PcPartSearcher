from flask import request, jsonify, make_response
from flask_cors import cross_origin
import logging
import traceback
import asyncio
from scrapers import OLX_Spyder, SigmaSpyder, AmazonSpyder, ALFrensia_Spyder, BadrSpyder

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def async_search_products(search_term, source_filters):
    results = {
        'olx': [],
        'sigma': [],
        'amazon': [],
        'badr': [],
        'alfrensia': []
    }

    tasks = []

    if source_filters.get('olx'):
        olx_spyder = OLX_Spyder(search_term)
        tasks.append(olx_spyder.scrape())

    if source_filters.get('sigma'):
        sigma_spyder = SigmaSpyder(search_term)
        tasks.append(sigma_spyder.scrape())

    if source_filters.get('amazon'):
        amazon_spyder = AmazonSpyder()
        tasks.append(amazon_spyder.search_products_async(search_term))

    if source_filters.get('badr'):
        badr_spyder = BadrSpyder()
        tasks.append(badr_spyder.scrape(search_term))

    if source_filters.get('alfrensia'):
        alfrensia_spyder = ALFrensia_Spyder()
        tasks.append(alfrensia_spyder.scrap(search_term))

    results_list = await asyncio.gather(*tasks, return_exceptions=True)

    sources = ['olx', 'sigma', 'amazon', 'badr', 'alfrensia']
    for i, source in enumerate(sources):
        if source_filters.get(source):
            if isinstance(results_list[i], Exception):
                logger.error(f"Error occurred with {source.capitalize()} scraper: {results_list[i]}")
                results[source] = [f"Error scraping {source.capitalize()}: {str(results_list[i])}"]
            else:
                results[source] = results_list[i] or []

    return results


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
        search_term = data.get('search_term')
        source_filters = data.get('source_filters', {})

        if not search_term or not isinstance(search_term, str) or len(search_term.strip()) < 2:
            logger.error("Invalid search term")
            return jsonify({'error': 'Invalid search term'}), 400

        # Use asyncio.run to handle the asynchronous function
        results = asyncio.run(async_search_products(search_term, source_filters))

        total_items = sum(len(items) for items in results.values())
        response_data = {
            **results,
            'totalPages': (total_items // 24) + (1 if total_items % 24 > 0 else 0),
            'itemsPerPage': 24,
            'status': 'success'
        }
        return jsonify(response_data)
    except Exception as e:
        logger.error(f"Error in search_products: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'Search failed', 'message': str(e)}), 500
