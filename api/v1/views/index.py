#!/usr/bin/python3
"""index file"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def attain_status():
    """/api/v1/status route"""
    return jsonify(status='OK')
