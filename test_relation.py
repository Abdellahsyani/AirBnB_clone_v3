#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ get the state with cities
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/states")
    r_j = r.json()
    
    state_id = None
    for state_j in r_j:
        rs = requests.get("http://0.0.0.0:5000/api/v1/states/{}/cities".format(state_j.get('id')))

        rs_j = rs.json()
        if len(rs_j) != 0:
            state_id = state_j.get('id')
            break
    
    if state_id is None:
        print("State with cities not found")
    
    """ get city
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/states/{}/cities".format(state_id))
    r_j = r.json()
    city_id = None
    for city_j in r_j:
        rc = requests.get("http://0.0.0.0:5000/api/v1/cities/{}/places".format(city_j.get('id')))
        rc_j = rc.json()
        if len(rc_j) != 0:
            city_id = city_j.get('id')
            break
    
    if city_id is None:
        print("City with places not found")

    """ get place
    """
    print("city", city_id)
    r = requests.get("http://0.0.0.0:5000/api/v1/cities/{}/places".format(city_id))
    r_j = r.json()
    place_id = None
    for place_j in r_j:
        rp = requests.get("http://0.0.0.0:5000/api/v1/places/{}/amenities".format(place_j.get('id')))
        rp_j = rp.json()
        if len(rp_j) == 0:
            place_id = place_j.get('id')
            break
    
    if place_id is None:
        print("Place without amenities not found")
    
    
    """ Fetch amenities
    """
    r = requests.get("http://0.0.0.0:5000/api/v1/places/{}/amenities".format(place_id))
    r_j = r.json()
    print(r_j)
    print(type(r_j))
    print(len(r_j))
