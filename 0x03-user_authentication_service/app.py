#!/usr/bin/env python3
"""
Flask app
"""

from flask import Flask, jsonify, request, make_response, abort
from auth import Auth


app = Flask(__name__)

AUTH = Auth()
auth = Auth()


@app.route("/", methods=['GET'])
def api():
    message = {"message": "Bienvenue"}

    return jsonify(message)


@app.route("/users", methods=["POST"])
def users():
    # extract email and password from form data
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        # attempt to register user
        user = AUTH.register_user(email, password)
        # if reg successful, return json with user info and status code
        return jsonify({"email": user.email, "message": "user created"}), 200

    except ValueError:
        # if user already exists, return json indicating email is registered
        # already
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login():
    # get email and passwd from form data
    email = request.form.get('email')
    password = request.form.get('password')

    # authenticate the user
    if auth.valid_login(email, password):
        # create new sesion for user
        session_id = auth.create_session(email)

        # set the session ID as a cookie on response
        response = make_response(
            jsonify({"email": email, "message": "logged in"}))
        response.set_cookie('session_id', session_id)

        return response, 200
    else:
        # if login info is incorrect, return 401 unauthorized
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
