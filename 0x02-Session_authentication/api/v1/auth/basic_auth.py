#!/usr/bin/env python3
""" Module of Auth the API authentication
"""
from typing import TypeVar
import base64
import binascii
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """class inherits from Auth class
        for basic authenthication
    """
    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        """extract base 64"""
        if authorization_header is None or not isinstance(authorization_header,
                                                          str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.lstrip('Basic ')

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """extract base 64"""
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header,
                str):
            return None
        try:
            decode_64 = base64.b64decode(base64_authorization_header,
                                         validate=True)
            return decode_64.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str
                                 ) -> str:
        """extract user email and password"""
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header,
                str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        # allow password with :
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """eturns the User instance based on his email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            # search user matching  with email
            users_with_email = User.search({'email': user_email})
        except Exception:
            return None

        # check if password match
        for user in users_with_email:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """return user current"""
        autho_header_value = self.authorization_header(request)
        extract_base64 = self.extract_base64_authorization_header(
            autho_header_value)
        decode_base64 = self.decode_base64_authorization_header(extract_base64)
        user_pass = self.extract_user_credentials(decode_base64)
        email, password = user_pass
        user = self.user_object_from_credentials(email, password)
        return user
