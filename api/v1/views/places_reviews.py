#!/usr/bin/python3
""" place parameters """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route(
    "/places/<place_id>/reviews",
    strict_slashes=False,
    methods=['GET']
)
def get_place_reviews(place_id):
    """Retrieves all reviews of a place by place id, or raise 404 error"""
    place = storage.get("Place", str(place_id))
    if place:
        reviews = place.reviews
        return jsonify([review.to_dict() for review in reviews])
    else:
        abort(404)


@app_views.route(
    "reviews/<review_id>",
    strict_slashes=False,
    methods=['GET']
)
def get_reviews(review_id):
    """Retrieves review by its id, or raise 404 error"""
    review = storage.get("Review", str(review_id))
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route(
    "reviews/<review_id>",
    strict_slashes=False,
    methods=['DELETE']
)
def remove_review(review_id):
    """Delete a reviews by its id, or raise 404 error"""
    review = storage.get("Review", str(review_id))
    if review:
        review.delete()
        return jsonify({})
    else:
        abort(404)


@app_views.route(
    "/places/<place_id>/reviews",
    methods=["POST"],
    strict_slashes=False
)
def new_place_review(place_id):
    """Create new review for the place of place_id, if exists"""
    place = storage.get("Place", str(place_id))
    data = request.get_json(force=True, silent=True)
    if place is None:
        abort(404)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in data.keys():
        return jsonify({"error": "Missing user_id"}), 400
    if not storage.get("User", data["user_id"]):
        # user doesn't exist
        abort(404)
    if 'text' not in data.keys():
        return jsonify({"error": "Missing text"}), 400
    place = Review(
        user_id=data["user_id"],
        text=data["text"],
        place_id=place_id
    )
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route(
    "/reviews/<review_id>",
    methods=["PUT"],
    strict_slashes=False
)
def update_review(review_id):
    """Update place details"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key in data.keys():
        readonly_keys = [
            "id",
            "place_id",
            "user_id",
            "created_at",
            "updated_at"
        ]
        if key not in readonly_keys:
            setattr(review, key, data[key])
    review.save()
    storage.save()
    return jsonify(review.to_dict()), 200
