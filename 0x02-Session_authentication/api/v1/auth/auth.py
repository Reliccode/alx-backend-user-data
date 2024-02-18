#!/usr/bin/env python3
""" Module of Auth the API authentication
"""
import os
from typing import List, TypeVar


class Auth:
    """Class Auth"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        for p in excluded_paths:
            if p.endswith('*'):
                # If the excluded path ends with '*', remove it before matching
                p = p[:-1]
                if path.startswith(p):
                    return False
            elif path == p or path == p.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request
        """
        if request is None:
            return None
        # use cookies.get(key) instead of cookies[key] to not get a
        # KeyError if the cookie is missing.
        return request.cookies.get(os.environ.get('SESSION_NAME'))
