from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.search_routes import search_bp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(search_bp, prefix="/api")