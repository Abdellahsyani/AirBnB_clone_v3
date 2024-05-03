#!/usr/bin/python3
"""Users api long and I don't what to do more than that!"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route(
    "/users",
    strict_slashes=False
)
def get_users():
    """Retrieves the list of all users"""
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route(
    "/users/<user_id>",
    strict_slashes=False
)
def get_user(user_id):
    """Retrieves user by id or abort"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route(
    "/users/<user_id>",
    strict_slashes=False
)
def remove_user(user_id):
    """Delete a user by its id, or abort"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
    "/users",
    methods=["POST"],
    strict_slashes=False
)
def new_user():
    """create new user"""
    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in data.keys():
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in data.keys():
        return jsonify({"error": "Missing password"}), 400
    user = User(email=data["email"], password=data["password"])
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route(
    "/users/<user_id>",
    methods=["PUT"],
    strict_slashes=False
)
def update_user(user_id):
    """Update user by its id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key in data.keys():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, data[key])
    user.save()
    storage.save()
    return jsonify(user.to_dict()), 200
