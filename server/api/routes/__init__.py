from .badr.badr_route import badr_bp
from .olx.olx_route import olx_bp
from .sigma.sigma_route import sigma_bp
from .amazon.amazon_route import amazon_bp
from .alfrensia.alfrensia_route import alfrensia_bp  # Add this line

__all__ = ['badr_bp', 'olx_bp', 'sigma_bp', 'amazon_bp', 'alfrensia_bp']  # Update this line