from fastapi import APIRouter
from app.controllers.search_controller import search_products

search_bp = APIRouter()

search_bp.post("/api/search")(search_products)
