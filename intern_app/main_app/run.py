import os

from app import create_app

config_name = 'dev'
app = create_app()

"""
This runs the app and exposes its port to 8080
This is used by docker scripts
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)
