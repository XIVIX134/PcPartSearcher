from api.app import app

if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True,
        threaded=True,
        host='0.0.0.0',  # Allow external connections
        use_reloader=True
    )
