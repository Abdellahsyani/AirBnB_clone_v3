#!/usr/bin/python3
""" place parameters """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City


@app_views.route(
    "/cities/<city_id>/places",
    strict_slashes=False,
    methods=['GET']
)
def get_places_city(city_id):
    """Retrieves all places in a city, or raise 404 error"""
    city = storage.get("City", str(city_id))
    if city:
        places = city.places
        return jsonify([place.to_dict() for place in places])
    else:
        abort(404)


@app_views.route(
    "/places/<place_id>",
    methods=["GET"],
    strict_slashes=False
)
def get_place(place_id):
    """Get place object by its id, or abort"""
    place = storage.get("Place", str(place_id))
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route(
    "/places/<place_id>",
    methods=["DELETE"],
    strict_slashes=False
)
def delete_place(place_id):
    """Delete place object by id if exist or abort"""
    place = storage.get("Place", str(place_id))
    if place:
        place.delete()
        return jsonify({})
    else:
        abort(404)


@app_views.route(
    "/cities/<city_id>/places",
    methods=["POST"],
    strict_slashes=False
)
def new_place(city_id):
    """create new place"""
    data = request.get_json(force=True, silent=True)
    city = storage.get("City", str(city_id))
    if not city:
        abort(404)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data.keys():
        return jsonify({"error": "Missing name"}), 400
    if 'user_id' not in data.keys():
        return jsonify({"error": "Missing user_id"}), 400
    if not storage.get("User", data["user_id"]):
        # user doesn't exist
        abort(404)
    place = Place(
        user_id=data["user_id"],
        name=data["name"],
        city_id=city_id
    )
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route(
    "/places/<place_id>",
    methods=["PUT"],
    strict_slashes=False
)
def update_place(place_id):
    """Update place details"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key in data.keys():
        if key not in ["id", "city_id", "user_id", "created_at", "updated_at"]:
            setattr(place, key, data[key])
    place.save()
    storage.save()
    return jsonify(place.to_dict()), 200


def cites_stateid(states_id):
    """Get list of all cities of State ids"""
    cities = []
    for state_id in states_id:
        state = storage.get("State", state_id)
        if state:
            cities.extend(state.cities)
    print(cities)
    return cities


def cities_cityid(cities_ids):
    """Get list of all cities of City ids"""
    cities = []
    for city_id in cities_ids:
        city = storage.get("City", city_id)
        if city:
            cities.append(city)
    return cities

def places_cities(cities):
    """Get list of all places in cities"""
    places = []
    for city in cities:
        places.extend(city.places)
    print(places)
    return places


def places_dict(places):
    dicts = []
    for place in places:
        p = place.to_dict()
        p.pop("amenities", None)
        dicts.append(p)
    return dicts


@app_views.route(
    "/places_search",
    methods=["POST"],
    strict_slashes=False
)
def place_search():
    """Search for places using list of cities and places and amenities. Place
    id is in the response means:
        - The place is in one of City ids listed
        - The place is in one of cities state ids listed
        - The place is having all Amenity ids listed (if not empty)
    If states and cities is empty, all Place ids having all Amenity ids will be
    listed.
    """
    filters = request.get_json(force=True, silent=True)
    if filters is None:
        return jsonify({"error": "Not a JSON"}), 400
    city_ids = filters.get("cities")
    state_ids = filters.get("states")
    amenity_ids = filters.get("amenities")
    places = []
    cities = []
    
    if not (city_ids or state_ids or amenity_ids):
        all_places = storage.all(Place).values()
        return [pl.to_dict() for pl in all_places]
    if city_ids:
        cities.extend(cities_cityid(city_ids))
    if state_ids:
        cities.extend(cites_stateid(state_ids))
    if amenity_ids and not (state_ids or city_ids):
        places = list(storage.all(Place).values())
    if cities:
        places = places_cities(cities)

    if amenity_ids:
        places = list(filter(
            lambda p: set(amenity_ids).issubset([a.id for a in p.amenities]),
            places
        ))

    return jsonify(places_dict(places))
