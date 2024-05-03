#!/usr/bin/python3
""" place - Amenity """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route(
    "/places/<place_id>/amenities",
    strict_slashes=False,
    methods=['GET']
)
def get_place_amenities(place_id):
    """Retrieves all amenities in a place, or raise 404 error"""
    place = storage.get("Place", str(place_id))
    if place:
        amenities = place.amenities
        return jsonify([amenity.to_dict() for amenity in amenities])
    else:
        abort(404)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    strict_slashes=False,
    methods=['DELETE']
)
def remove_review(place_id, amenity_id):
    """Delete an amenity from place, or raise 404 error"""
    place = storage.get("Placa", str(place_id))
    amenity = storage.get("Amenity", str(amenity_id))
    if not (place and amenity and amenity in place.amenities):
        abort(404)
    place.amenities.remove(amenity)
    return jsonify({}), 200


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["POST"],
    strict_slashes=False
)
def new_place_amenity(place_id, amenity_id):
    """Add new amenity to a place"""
    place = storage.get("Place", str(place_id))
    amenity = storage.get("Amenity", str(amenity_id))
    if not (place and amenity):
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    else:
        place.amenities.append(amenity)
        return jsonify(amenity.to_dict()), 200
