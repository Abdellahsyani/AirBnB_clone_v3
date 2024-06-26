#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import unittest
from hashlib import md5
try:
    import pycodestyle as pep8
except Exception as e:
    import pep8


classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}
DBStorage = db_storage.DBStorage


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    def test_storage_get(self):
        """Testing Get method"""
        myObject = State(name="Alabama")
        myObject.save()
        state = models.storage.get(State, myObject.id)
        self.assertEqual(state.name, "Alabama")
        self.assertEqual(state.created_at, myObject.created_at)

    def test_storage_count_1(self):
        """Testing Count method"""
        s_count_old = len(models.storage.all(State))
        s_count_new = models.storage.count(State)
        self.assertEqual(s_count_old, s_count_new)
        myObject = State(name="Alabama")
        myObject.save()
        s_count_old = len(models.storage.all(State))
        s_count_new = models.storage.count("stAte")
        self.assertEqual(s_count_old, s_count_new)

    def test_storage_count_2(self):
        """Count in case of all objects"""
        count_old = len(models.storage.all())
        count_new = models.storage.count()
        self.assertEqual(count_old, count_new)

    def test_pass_hash(self):
        """The new password is hashed before it is stored"""
        password = "happiness"
        u = User(email="testing@hbnb.io", password=password)
        hashed_pass = md5(password.encode()).hexdigest()
        self.assertEqual(hashed_pass, u.password)

    def test_no_rehash(self):
        """If the password exists, don't hash it again"""
        pw = "happiness"
        u = User(email="testing@hbnb.io", password=pw)
        id = u.id
        u.save()
        models.storage.reload()
        some_u = models.storage.get("User", id)
        some_pw = some_u.password
        self.assertEqual(some_pw, md5(pw.encode()).hexdigest())

    def test_pass_hidden(self):
        """to_dict is not showing the passowrd"""
        password = "happiness"
        u = User(email="testing@hbnb.io", password=password)
        id = u.id
        u.save()
        self.assertIsNone(u.to_dict().get("password"))
        models.storage.reload()
        u = models.storage.get("User", id)
        self.assertIsNone(u.to_dict().get("password"))
