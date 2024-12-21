import json
import os

# Get the absolute path of the current file (storage.py)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Correct paths to the JSON files relative to this file's directory
data_path = os.path.join(BASE_DIR, 'data.json')
badr_path = os.path.join(BASE_DIR, 'badr.json')

def initialize_json_file(file_path):
    """Initialize a JSON file with an empty array if it doesn't exist or is invalid"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    # If file exists but is invalid JSON, overwrite with empty array
                    pass
        
        # Create new file with empty array
        with open(file_path, 'w') as file:
            json.dump([], file)
        return []
    
    except Exception as e:
        print(f"Error handling file {file_path}: {str(e)}")
        return []

# Initialize both JSON files
data = initialize_json_file(data_path)
badr = initialize_json_file(badr_path)

if __name__ == '__main__':
    print(f"Initialized data.json with {len(data)} items")
    print(f"Initialized badr.json with {len(badr)} items")
