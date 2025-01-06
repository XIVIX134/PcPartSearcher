from flask import jsonify

def get_sigma():
    return jsonify({'sigma_items': ['itemA', 'itemB', 'itemC']})
