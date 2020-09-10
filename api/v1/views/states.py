#!/usr/bin/python3
""" states  """

from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    """returns list of state objs"""
    storage_list = []
    for obj in storage.all(State).values():
        storage_list.append(obj.to_dict())
    return jsonify(storage_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def ret_states(state_id):
    """ retrieves states """
    getit = storage.get("State", state_id)
    if getit is None:
        abort(404)
    return jsonify(getit.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_states(state_id):
    getit = storage.get("State", state_id)
    if getit is None:
        abort(404)
    storage.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a new state """
    getson = request.get_json()
    if not getson:
        abort(400, "Not a JSON")
    if "name" not in getson:
        abort(400, "Missing name")
    st = State(**getson)
    storage.new(st)
    storage.save()
    return make_response(jsonify(st.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_states(state_id):
    """ Updates a specific state """
    getson = request.get_json()
    if not getson:
        abort(400, "Not a JSON")
    new_me = storage.get("State", state_id)
    if not new_me:
        abort(404)
    for k, v in getson.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(new_me, k, v)
    storage.save()
    return make_response(new_me.to_dict(), 200)
