# app/controllers/search_controller.py
from fastapi import HTTPException
from app.models.search_model import SearchModel
from app.views.search_view import format_search_results
from pydantic import BaseModel
import asyncio

class SearchRequest(BaseModel):
    search_term: str
    source_filters: dict

async def search_products(request: SearchRequest):
    search_term = request.search_term
    source_filters = request.source_filters
    
    try:
        model = SearchModel()
        results = await model.async_search_products(search_term, source_filters)
        
        formatted_results = format_search_results(results)
        
        return formatted_results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
