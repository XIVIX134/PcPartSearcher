import json
import os

# Get the absolute path of the current file (storage.py)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Correct paths to the JSON files relative to this file's directory
data_path = os.path.join(BASE_DIR, 'data.json')
badr_path = os.path.join(BASE_DIR, 'badr.json')

# Open the files using the absolute paths
with open(data_path) as file:
    data = json.load(file)

with open(badr_path) as badr_file:
    badr = json.load(badr_file)
