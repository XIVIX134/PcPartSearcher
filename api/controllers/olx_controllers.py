from flask import jsonify
from api.storage import data

def get_laptops():
    laptops = []
    for item in data:
        product_id = item.get('Product ID')
        title = item.get('Title')
        price = item.get('Price')
        location = item.get('Location')
        image_url = item.get('Image URL')
        details_link = item.get('Details Link')
        
        laptops.append({
            "Product ID": product_id,
            "Title": title,
            "Price": price,
            "Location": location,
            "Image URL": image_url,
            "Details Link": details_link,
        })
    
    return jsonify(laptops)