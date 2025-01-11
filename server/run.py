import os
import sys

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from api.app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
