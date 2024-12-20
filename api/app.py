from flask import Flask, Blueprint


app = Flask(__name__)

badr_bp = Blueprint('badr', __name__)
olx_bp = Blueprint('olx', __name__)
sigma_bp = Blueprint('sigma', __name__)

# Register blueprints
app.register_blueprint(olx_bp, url_prefix='/olx')
app.register_blueprint(badr_bp, url_prefix='/badr')
app.register_blueprint(sigma_bp, url_prefix='/sigma')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
