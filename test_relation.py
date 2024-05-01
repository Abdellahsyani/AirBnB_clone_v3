#!/bin/python3

from models import *
from models.state import State
from models.city import City
from models import storage


# state = State(name="Boston")
# state.save()
#
# city_1 = City(name="city1")
# city_2 = City(name="city2")
# city_3 = City(name="city3")
# state.cities = [city_1, city_2, city_3]
# state.save()
state = storage.get("state", "b1a513e3-4ab6-4fff-a3ca-b11e44eb6b4d")
state.delete()


