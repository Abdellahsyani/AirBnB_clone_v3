#!/usr/bin/python3
""" City parameters """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route(
    "/states/<state_id>/cities",
    strict_slashes=False,
    methods=['GET']
)
def get_state_cities(state_id):
    """Retrieves the list of all cities in a state"""
    state = storage.get("State", str(state_id))
    if state:
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    else:
        abort(404)


@app_views.route(
    "/cities/<city_id>",
    strict_slashes=False,
    methods=['GET']
)
def get_city(city_id):
    """Retrieves city object by id, or raise 404 error"""
    city = storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route(
    "/cities/<city_id>",
    methods=["DELETE"],
    strict_slashes=False
)
def delete_city(city_id):
    """Delete city object by id if or abort"""
    city = storage.get(City, city_id)
    if city:
        city.delete()
        return jsonify({})
    else:
        abort(404)


@app_views.route(
    "/states/<state_id>/cities",
    methods=["POST"],
    strict_slashes=False
)
def new_city(state_id):
    """create new city"""
    data = request.get_json(force=True, silent=True)
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data.keys():
        return jsonify({"error": "Missing name"}), 400
    city = City(state_id=state_id, name=data["name"])
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route(
    "/cities/<city_id>",
    methods=["PUT"],
    strict_slashes=False
)
def put_city(city_id):
    """Update object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key in data.keys():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, data[key])
    city.save()
    storage.save()
    return jsonify(city.to_dict()), 200
