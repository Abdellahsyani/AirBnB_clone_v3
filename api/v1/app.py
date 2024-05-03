#!/usr/bin/python3
"""folder app"""

from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    """This used to keep always the data up to date:
    The session that created by SQLAchemy is always keeping a connection that
    is isolated to other possible existing connections. Here we forced it to
    return to the connection pool within the Engine, ensuring that every
    changes made by other pools are reloaded
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handeling not found page (error 404)"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    if HBNB_API_HOST is None:
        HBNB_API_HOST = '0.0.0.0'
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if HBNB_API_PORT is None:
        HBNB_API_PORT = 5000
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
