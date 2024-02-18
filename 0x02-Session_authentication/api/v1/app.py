#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
import os
from flask_cors import (CORS, cross_origin)
from flask import Flask, jsonify, abort, request
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

auth_type = os.environ.get('AUTH_TYPE')

if auth_type == 'basic_auth':
    auth = BasicAuth()
elif auth_type == 'session_auth':
    auth = SessionAuth()
elif auth_type == 'session_exp_auth':
    auth = SessionExpAuth()
elif auth_type == 'session_db_auth':
    auth = SessionDBAuth()
else:
    auth = Auth()


@app.before_request
def before_request():
    """run before each request
    """
    if auth is None:
        return
    # paths that should not require authentication
    ex_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                '/api/v1/forbidden/', '/api/v1/auth_session/login/']

    # Check if request.path is not part of the excluded paths list
    if request.path not in ex_paths:
        # check if authentication is required
        if auth.require_auth(request.path, ex_paths):
            if auth.authorization_header(request) is None \
                    and auth.session_cookie(request) is None:
                abort(401)
            current_user = auth.current_user(request)
            if auth.current_user(request) is None:
                abort(403)
            request.current_user = current_user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """ unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """ forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(debug=True, host=host, port=port)
