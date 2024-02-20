#!/usr/bin/env python3
"""
add_user method
"""


from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
# from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User

# Base = declarative_base()


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        # try:
        self._session.commit()
        # except IntegrityError as err:
        self._session.rollback()
        # raise ValueError("User already exists") from err
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        using keywords to find user in db
        """
        try:
            # start new SELECT query targeting User model
            # Apply filtering according to keywords provided
            user = self._session.query(User).filter_by(**kwargs).first()
            # if user is not found, raise NoResultFound
            if user is None:
                raise NoResultFound

            # return the user object found
            return user
        except InvalidRequestError as e:
            # if there are issues with query, raise InvalidResquestError
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        update user in db based on user_id
        """

        try:
            #find user by user_id
            user = self.find_user_by(id=user_id)

            #looping thru keyword arguments
            for key, value in kwargs.items():
                #check if attribute exists in User model
                if hasattr(User, key):
                    #update users attribute
                    setattr(user, key, value)

                else:
                    #If an invalud attr is passed, raise ValueError
                    raise ValueError(f"Invalid attribute: {key}")

            #commit changes to db
                self.__session.commit()
        except NoResultFound:
            #if user not found raise NoResultFound
            raise
