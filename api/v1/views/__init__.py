#!/usr/bin/python3
"""Creates the blueprint"""

from flask import Blueprint


app_views = Blueprint('/api/v1', __name__)

if True:
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.cities import *
    from api.v1.views.amenities import *
    from api.v1.views.users import *
    from api.v1.views.places import *
