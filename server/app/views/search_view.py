from fastapi import HTTPException
from pydantic import BaseModel
from app.controllers.search_controller import search_controller

class SearchRequest(BaseModel):
    search_term: str
    source_filters: dict
    
async def search_view(request: SearchRequest):
    try:
        search_term = request.search_term
        source_filters = request.source_filters
        
        if not search_term and not source_filters:
            return {"status": "error", "message": "Search term and filters is required."}   
        
        results = await search_controller(search_term, source_filters)
        return results  # Return the results from the controller
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"[ VIEW ] Search failed: {str(e)}")