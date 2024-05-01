#!/usr/bin/python3
""" City parameters """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def cities(state_id):
    """Retrieves the list of all City objects of a State"""
    cities = []
    states = list(storage.all(State).values())
    state = None
    for st in states:
        if st.id == state_id:
            state = st
            break
    if state:
        for city in storage.all(City).values():
            if city.state_id == state.id:
                cities.append(city.to_dict())
    else:
        abort(404)
    return jsonify(cities)


@app_views.route("/cities/<city_id>", strict_slashes=False)
def city(city_id):
    """find city_id"""
    cities = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            return jsonify(city.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """delete city object"""
    city = storage.get(City, city_id)
    response = jsonify({})
    response.status_code = 200
    if city:
        storage.delete(city)
        storage.save()
        return (response)
    else:
        abort(404)


@app_views.route(
    "/states/<state_id>/cities",
    methods=["POST"], strict_slashes=False)
def post_city(state_id):
    """create a new city"""
    data = request.get_json(force=True, silent=True)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data.keys():
        return jsonify({"error": "Missing name"}), 400
    city = City(state_id=state_id, name=data["name"])
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """update object"""
    data = request.get_json(force=True, silent=True)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key in data.keys():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, data[key])
    city.save()
    storage.save()
    return jsonify(city.to_dict()), 200
