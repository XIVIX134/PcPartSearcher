from flask import jsonify

def get_sigma_items():
    return jsonify({'sigma_items': ['itemA', 'itemB', 'itemC']})
