#!/usr/bin/python3
"""Defining the routes"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/api/v1/status', methods=['GET'])
def status():
    """
    Returns a JSON response with status OK.
    """
    return jsonify({"status": "OK"})
