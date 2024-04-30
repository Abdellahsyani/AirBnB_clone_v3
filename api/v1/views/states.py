#!/usr/bin/python3
""" handle state actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states",
                 methods=['GET', 'POST'], strict_slashes=False)
def states():
    """handle get and post requests"""
    if request.method == 'GET':
        states = storage.all("State").values()
        return jsonify(list(map(lambda x: x.to_dict(), states)))
    else:
        Requests = request.get_json(force=True, silent=True)
        if Requests is None:
            abort(400, "Not a JSON")
        if Requests.get('name') is None:
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
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({})
    else:
        Requests = request.get_json(force=True, silent=True)
        if Requests is None:
            abort(400, "Not a JSON")
        for key in Requests:
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(state, key, Requests.get(key))
        storage.save()
        return jsonify(state.to_dict())
