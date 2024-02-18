#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.views import app_views
from os import getenv
from api.v1.views.users import view_all_users, view_one_user
from api.v1.views.index import status, stats, unauthorized, forbidden
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)

app.register_blueprint(app_views)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTH_TYPE = getenv("AUTH_TYPE")

if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> str:
    """ Before Request Handler
    Requests Validation
    """
    if auth is None:
        return

    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/users/me']  # new endpoint to excluded path

    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    if request.path == '/api/v1/users/me':  # handle new endpoint
        current_user = auth.current_user(request)
        if current_user is None:
            return '', 200
        return jsonify(current_user.to_dict())

    if auth.current_user(request) is None:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.debug = True
    app.run(host=host, port=port)
