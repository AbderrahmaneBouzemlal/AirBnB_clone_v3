#!/usr/bin/python3
"""Defining the routes"""

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/api/v1/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Returns a JSON response with status OK.
    """
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    Create an endpoint that retrieves the number of each objects by type
    """
    return jsonify({
        'states': storage.count(State),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'amenities': storage.count(Amenity),
        "reviews": storage.count(Review),
        "users": storage.count(User)
        })
