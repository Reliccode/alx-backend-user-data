#!/usr/bin/env python3
"""
Hash passwords
"""


import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
# import hashlib


def _hash_password(password: str) -> bytes:
    """
    hashes passwd using bcrypt.hashpw
    """
    # encode password as bytes
    password_bytes = password.encode('utf-8')

    # Generating Salt
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_password


class Auth:
    """
    Auth class to interact with authentication db
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers new user
        """
        # check if a user with a given email exists
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        # hash the password
        hashed_password = _hash_password(password)

        # add user to db
        user = self._db.add_user(email, hashed_password)

        return user
