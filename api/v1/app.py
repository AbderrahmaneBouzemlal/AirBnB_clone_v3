#!/usr/bin/python3HBNB_API_PORT
"""
first endpoint (route) will be to return the status of the API
"""
import json
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
'''The Flask web application instance.'''

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(Exception):
    """closes the storage on teardown"""
    storage.close()


# @app.errorhandler(404)
# def not_found(e):
#     response = e.get_response()
#     response.data = json.dumps({"error": "Not found"})
#     response.content_type = "application/json"
#     return response


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", '0.0.0.0')
    port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
