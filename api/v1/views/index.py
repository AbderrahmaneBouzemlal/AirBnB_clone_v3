#!/usr/bin/python3
"""Defining the routes"""

from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage


@app_views.route('/api/v1/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Returns a JSON response with status OK.
    """
    return make_response(jsonify(status="OK"), 200)


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    Create an endpoint that retrieves the number of each objects by type
    """
    return make_response(
        jsonify(
        states=storage.count('State'),
        cities=storage.count('City'),
        places=storage.count('Place'),
        amenities=storage.count('Amenity'),
        reviews=storage.count('Review'),
        users=storage.count('User')
        ),
        200)
