from flask import Blueprint
from api.controllers.olx_controllers import get_laptops
from api.app import olx_bp


olx_bp.route('/laptops', methods=['GET'])(get_laptops)
