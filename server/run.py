import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from api.app import app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
