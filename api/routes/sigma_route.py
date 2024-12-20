from flask import Blueprint
from api.controllers.sigma_controller import get_sigma_items
from api.app import sigma_bp


sigma_bp.route('/items', methods=['GET'])(get_sigma_items)
