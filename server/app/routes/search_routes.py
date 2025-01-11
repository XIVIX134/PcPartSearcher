from fastapi import APIRouter
from app.views.search_view import search_view

search_bp = APIRouter()

search_bp.post("/search")(search_view)
