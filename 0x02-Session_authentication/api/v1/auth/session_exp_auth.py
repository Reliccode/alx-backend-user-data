#!/usr/bin/env python3
""" Module of Auth the API authentication
"""
from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """class inherits from SessionAuth class
        for an expiration date to a Session ID.
    """
    def __init__(self):
        """initialize variables"""
        # Get the value of the environment variable SESSION_DURATION
        session_duration_str = os.environ.get('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration_str)
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create session_id with expiration data"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns a User ID based on a Session ID
            with expiration id
        """
        # doesn’t contain any key equals to session_id or none
        if session_id is None \
                or session_id not in self.user_id_by_session_id.keys():
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        current_time = datetime.now()
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < current_time:
            return None
        return session_dict.get('user_id')
