from flask import jsonify
from api.storage import badr

def cpus():
    cpus_data = [
        {
            "Product ID": item.get('Product ID'),
            "Title": item.get('Title'),
            "Price": item.get('Price'),
            "Location": item.get('Location'),
            "Image URL": item.get('Image URL'),
            "Details Link": item.get('Details Link'),
        }
        for item in badr
    ]
    return jsonify(cpus_data)
