#!/usr/bin/python3
""" state module """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def list_plays(city_id):
    """returns list of places"""
    places = []
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    for ite in storage.all("Place").values():
        if ite.city_id == city_id:
            places.append(ite.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """returns palces by id"""
    places = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """deletes a state"""
    getsto = storage.get("Place", place_id)
    if not getsto:
        abort(404)
    getsto.delete()
    storage.save()
    return {}, 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """creates a city"""
    getson = request.get_json()
    if not getson:
        abort(400, "Not a JSON")
    if "name" not in getson:
        abort(400, "Missing name")
    if "user_id" not in getson:
        abort(400, "Missing name")
    concit = storage.get("City", city_id)
    if not conit:
        abort(404)
    conus = storage.get("User", getson['user_id'])
    if not conus:
        abort(404)
    getson['city_id'] = city_id
    ret = Place(**getson)
    storage.new(ret)
    storage.save()
    return make_response(ret.to_dict(), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a State"""
    getson = request.get_json()
    if not derulo:
        abort(400, "Not a JSON")
    getplace = storage.get("Place", place_id)
    if not getplace:
        abort(404)
    for k, v in getson.items():
            setattr(getplace, k, v)
    storage.save()
    return make_response(getplace.to_dict(), 200)
