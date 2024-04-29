#!/usr/bin/python3
"""folder app"""

from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.treadown_appcontext
def treadown_appcontext():
    """call the storage"""
    storage.close()

if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    if HBNB_API_HOST is None:
        HBNB_API_HOST = '0.0.0.0'

    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if HBNB_API_PORT is None:
        HBNB_API_PORT = 5000
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
