from flask import jsonify, request
import asyncio
from scrapers.alfrensia.alfrensia_spyder import ALFrensia_Spyder

def Alfrensia_Search():
    try:
        data = request.get_json()
        search_term = data.get('searchTerm')
        
        if not search_term:
            return jsonify({"error": "searchTerm is required"}), 400
        
        spider = ALFrensia_Spyder()
        search_results = asyncio.run(spider.scrap(search_term))
        
        return jsonify({"results": search_results, "status": "success"})
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
