from fastapi import HTTPException
from app.models.search_model import SearchModel
from server.app.utils.search_utils import format_search_results
from pydantic import BaseModel


async def search_controller(search_term, source_filters):
    
    try:
        model = SearchModel()
        results = await model.async_search_products(search_term, source_filters)
        
        formatted_results = format_search_results(results)
        
        return formatted_results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"[ CONTROLL ] Search failed: {str(e)}")
