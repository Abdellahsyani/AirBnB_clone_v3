#!/usr/bin/python3
"""User"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def users():
    """get all user objects"""
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route("/users/<user_id>", strict_slashes=False)
def user(user_id):
    """get user"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def delete_user(user_id):
    """delete"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def post_user():
    """create user"""
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


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def put_user(user_id):
    """update user object"""
    data = request.get_json(force=True, silent=True)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key in data.keys():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, data[key])
    user.save()
    storage.save()
    return jsonify(user.to_dict()), 200
