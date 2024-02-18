#!/usr/bin/env python3
""" Module of Users views session
    authentication
"""
from flask import abort, request, jsonify
from api.v1.views import app_views
import os
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth__session_login():
    """ POST /auth_session/login
    Return:
      Retrieve the User instance based on the email
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or email is None:
        return {"error": "email missing"}, 400
    if not password or password is None:
        return {"error": "password missing"}, 400
    users = User().search({'email': email})
    if not users:
        return {"error": "no user found for this email"}, 404
    for user in users:
        if not user.is_valid_password(password):
            return {"error": "wrong password"}, 401
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        res = jsonify(user.to_json())
        res.set_cookie(os.environ.get('SESSION_NAME'), session_id)
        return res


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def auth__session_logout():
    """ DELETE /api/v1/auth_session/logout
    Return:
      deletes the user session / logout
    """
    from api.v1.app import auth
    # deleting the Session ID contains in the request as cookie
    destroyed_session_id = auth.destroy_session(request)
    if destroyed_session_id is False:
        abort(404)
    return {}, 200
