import json

with open("../scrapers/data.json") as file:
    data = json.load(file)
    
with open("../scrapers/badr.json") as badr_file:
    badr = json.load(badr_file)