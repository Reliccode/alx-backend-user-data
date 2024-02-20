#!/usr/bin/env python3
"""
Flask app
"""

from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)

AUTH = Auth()


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
