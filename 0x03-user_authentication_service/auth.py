#!/usr/bin/env python3
"""
Hash passwords
"""


import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
import uuid
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


def _generate_uuid() -> str:
    """Generates new UUID and returns its string representation"""
    # make random UUID
    random_uuid = uuid.uuid4()
    return str(random_uuid)


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

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login"""
        try:
            # locate user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            # if user doesn't exists, return False
            return False

        # retrieve hashed passwd from user object
        hashed_password = user.hashed_password

        # encode provided password
        password_bytes = password.encode('utf-8')

        # we use bcry to check if given passwd matches hashed passwd
        if bcrypt.checkpw(password_bytes, hashed_password):
            return True
        else:
            return False

    def create_session(self, email: str) -> str:
        """create new session for usesr and return session ID"""
        try:
            # find user by email
            user = self._db.find_user_by(email=email)

            session_id = str(uuid.uuid4())

            self._db.update_user(user.id, session_id=session_id)

            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieves user corresponding to given session ID"""

        if session_id is None:
            return None

        try:
            user = self._db.find_user_by_session_id(session_id)
            return user
        except NoResultFound:
            return None
