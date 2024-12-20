from flask import Blueprint
from api.controllers.badr_controller import get_badr_items
from api.app import badr_bp

badr_bp.route('/items', methods=['GET'])(get_badr_items)
