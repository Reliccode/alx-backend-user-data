#!/usr/bin/env python3
"""
add_user method
"""


from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from user import Base, User

#Base = declarative_base()


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        """
        # create a new user object
        user = User(email=email, hashed_password=hashed_password)

        # Add user to the session
        self._session.add(user)
        # commit session to save changes to db but lets catch err
        try:
            self._session.commit()
        except IntegrityError as err:
            self._session.rollback()
            raise ValueError("User already exists") from err
        return user
