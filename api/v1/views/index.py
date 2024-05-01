#!/usr/bin/python3
"""index file"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def attain_status():
    """GIve a user a way to make sure the api is working perfectly"""
    return jsonify(status='OK')


@app_views.route("/stats", strict_slashes=False)
def stats():
    """Retraive number of record by object type"""
    typeobj_count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(typeobj_count)
