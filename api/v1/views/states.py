#!/usr/bin/python3
""" handle state actions"""

from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route("/states", methods=['GET', 'POST'], strict_slashes=False)
def states():
    """handle get and post requests"""
    if request.method == 'GET':
        states = storage.all('states').values()
        state_list = [state.to_dict() for state in states]
        return jsonify(state_list)
    else:
        post_req = request.get_json(force=True, silent=True)
        if post_req is None:
            abort(400, "Not a JSON")
        if post_req.get('name') is None:
            abort(400, "Missing name")
        state = State(**kwargs)
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route("/states/<uuid:state_id>",
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def state(state_id):
    """handle the get delete put requests with state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(400)
    if request.method ==  'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({})
    else:
        put_req = request.get_json(force=True, silent=True)
        if put_req is None:
            abort(400, "Not a JSON")
        for key in put_req:
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(state, key, put_req.get(key))
        storage.save()
        return jsonify(state.to_dict())
