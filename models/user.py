#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from hashlib import md5
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import event


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship(
            "Place",
            backref="user",
            cascade="all, delete-orphan"
        )
        reviews = relationship(
            "Review",
            backref="user",
            cascade="all, delete-orphan"
        )
    else:
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, hash_pass=False, **kwargs):
        """initializes user"""
        if hash_pass:
            row_passwd = kwargs.get("password")
            kwargs["password"] = md5(row_passwd.encode()).hexdigest()
        super().__init__(*args, **kwargs)

    if models.storage_t != 'db':
        @property
        def password(self):
            """The password property."""
            return self._password

        @password.setter
        def password(self, value):
            self._password = md5(value.encode()).hexdigest()


def hash5(target, value, oldvalue, initiator):
    """Hach the password using md5 algorithm
    This precedure function that will be invoked where set new value to
    password event is triggered
    """
    return md5(value.encode()).hexdigest()


if models.storage_t == 'db':
    event.listen(User.password, 'set', hash5, retval=True)
