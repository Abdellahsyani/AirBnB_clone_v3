#!/usr/bin/python3
""" handle state actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route(
    "/states",
    methods=['GET'],
    strict_slashes=False
)
def get_states():
    """GET all states in the storage"""
    states = storage.all("State").values()
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)


@app_views.route(
    "/states",
    methods=['POST'],
    strict_slashes=False
)
def new_state():
    """Add new state to storage if it has a name"""
    kwargs = request.get_json(force=True, silent=True)
    if kwargs is None:
        abort(400, "Not a JSON")
    if kwargs.get('name') is None:
        abort(400, "Missing name")
    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route(
    "/states/<uuid:state_id>",
    methods=['DELETE'],
    strict_slashes=False
)
def remove_state(state_id):
    """Remove state from storage if exist"""
    state = storage.get(State, str(state_id))
    if state:
        state.delete()
        return jsonify({})
    else:
        abort(404)


@app_views.route(
    "/states/<uuid:state_id>",
    methods=['GET'],
    strict_slashes=False
)
def get_state(state_id):
    """Retrieves a State object if exist"""
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
    "/states/<uuid:state_id>",
    methods=['PUT'],
    strict_slashes=False
)
def update_state(state_id):
    """Update state with the corresponding id"""
    request_data = request.get_json(force=True, silent=True)
    if request_data is None:
        abort(400, "Not a JSON")
    for key in request_data:
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(state, key, request_data.get(key))
    storage.save()
    return jsonify(state.to_dict())
