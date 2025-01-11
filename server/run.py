import sys
import os

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True)