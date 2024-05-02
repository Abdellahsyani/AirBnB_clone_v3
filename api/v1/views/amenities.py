#!/usr/bin/python3
""" amenities api """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route(
    "/amenities",
    strict_slashes=False,
    methods=['GET']
)
def get_amenities():
    """Retrieves the list of all amenities"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route(
    "/amenities/<amenity_id>",
    strict_slashes=False,
    methods=['GET']
)
def get_amenitiy(amenity_id):
    """Retrieves amenity by id, or abort"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route(
    "/amenities/<amenity_id>",
    strict_slashes=False,
    methods=['DELETE']
)
def remove_amenitiy(amenity_id):
    """Delete an amenity by its id, or abort"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        amenity.delete()
        return jsonify({})
    else:
        abort(404)


@app_views.route(
    "/amenities",
    strict_slashes=False,
    methods=['POST']
)
def new_amenitiy():
    """Create new amenity"""
    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data.keys():
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(name=data["name"])
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route(
    "/amenities/<amenity_id>",
    methods=["PUT"],
    strict_slashes=False
)
def update_amenity(amenity_id):
    """update amenity by its id, or abort"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key in data.keys():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, data[key])
    amenity.save()
    storage.save()
    return jsonify(amenity.to_dict()), 200
