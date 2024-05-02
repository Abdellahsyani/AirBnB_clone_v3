#!/usr/bin/python3
""" place parameters """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City


@app_views.route(
    "/cities/<city_id>/places",
    strict_slashes=False,
    methods=['GET']
)
def get_places_city(city_id):
    """Retrieves all places in a city, or raise 404 error"""
    city = storage.get("City", str(city_id))
    print(city)
    if city:
        places = city.places
        return jsonify([place.to_dict() for place in places])
    else:
        abort(404)


@app_views.route(
    "/places/<place_id>",
    methods=["GET"],
    strict_slashes=False
)
def get_place(place_id):
    """Get place object by its id, or abort"""
    place = storage.get("Place", str(place_id))
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route(
    "/places/<place_id>",
    methods=["DELETE"],
    strict_slashes=False
)
def delete_place(place_id):
    """Delete place object by id if exist or abort"""
    place = storage.get("Place", str(place_id))
    if place:
        place.delete()
        return jsonify({})
    else:
        abort(404)


@app_views.route(
    "/cities/<city_id>/places",
    methods=["POST"],
    strict_slashes=False
)
def new_place(city_id):
    """create new place"""
    data = request.get_json(force=True, silent=True)
    city = storage.get("City", str(city_id))
    if not city:
        abort(404)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data.keys():
        return jsonify({"error": "Missing name"}), 400
    if 'user_id' not in data.keys():
        return jsonify({"error": "Missing user_id"}), 400
    if not storage.get("User", data["user_id"]):
        # user doesn't exist
        abort(404)
    place = Place(
        user_id=data["user_id"],
        name=data["name"],
        city_id=city_id
    )
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route(
    "/places/<place_id>",
    methods=["PUT"],
    strict_slashes=False
)
def update_place(place_id):
    """Update place details"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key in data.keys():
        if key not in ["id", "city_id", "user_id","created_at", "updated_at"]:
            setattr(place, key, data[key])
    place.save()
    storage.save()
    return jsonify(place.to_dict()), 200
