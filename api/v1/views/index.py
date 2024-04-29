#!/usr/bin/python3
"""index file"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def attain_status():
    """/api/v1/status route"""
    return jsonify(status='OK')


@app_views.route("/stats", strict_slashes=False)
def stats():
    """/api/v1/stats route"""
    return jsonify({
        "amenities": storage.count("Amenity\n"),
        "cities": storage.count("City\n"),
        "places": storage.count("Place\n"),
        "reviews": storage.count("Review\n"),
        "states": storage.count("State\n"),
        "users": storage.count("User\n")
    })
