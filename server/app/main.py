from fastapi import FastAPI
from app.routes.search_routes import search_bp

app = FastAPI()


app.include_router(search_bp)
