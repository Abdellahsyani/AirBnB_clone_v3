#!/bin/python3

from models.user import User
from models import storage

u = storage.get(User, "46dac7e1-c4d0-4b98-aefd-3c3fd6730def")
u.save()
print(u.password)
u = User(hash_pass=True, password="testing")
u.save()
print(u.password)
