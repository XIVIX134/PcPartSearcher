from flask import request, jsonify
from scrapers.amazon.amazon_spyder import AmazonSpyder
import json

def Amazon_Search():
    try:
        data = request.get_json()
        search_term = data.get('searchTerm')
        
        if not search_term:
            return jsonify({"error": "searchTerm is required"}), 400
        
        scraper = AmazonSpyder()
        search_results = scraper.search_products(search_term)
        
        # Convert the list to JSON and then back to ensure proper serialization
        return jsonify({"results": search_results, "status": "success"})
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500