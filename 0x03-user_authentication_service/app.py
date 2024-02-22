#!/usr/bin/env python3
"""
Flask app
"""

from flask import Flask, jsonify, request, make_response, abort
from flask import redirect
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


@app.route("/sessions", methods=['DELETE'])
def logout():
    # Get session id from cookie
    session_id = request.cookies.get('session_id')

    # find user corresponding to session id
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        # destroy the session
        AUTH.destroy_session(user.id)
        # redirect user to GET /
        return redirect("/", code=302)
    else:
        # Respond with 403 status if user not exists
        return "Forbidden", 403


@app.route("/profile", methods=['GET'])
def profile():
    # get session_id from cookie
    session_id = request.cookies.get('session_id')

    # find user matching the session id
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        # respond with 200 status & return users email
        return jsonify({"email": user.email}), 200
    else:
        # respond with 403 status if session id invalid
        # respond with 403 status if user does not exist
        return "Forbidden", 403


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    # get email from form data
    email = request.form.get('email')

    try:
        # generate reset passwd token for user
        reset_token = AUTH.get_reset_password_token(email)

        # respond with json payload
        response = jsonify({"email": email, "reset_token": reset_token})
        return response, 200

    except ValueError:
        # if email is not registered respond with 403 status code
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    try:
        # Get form data
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')

        # Call Auth.update_password method
        Auth.update_password(reset_token, new_password)

        # Respond with success message
        response = {"email": email, "message": "Password updated"}
        return jsonify(response), 200

    except ValueError as e:
        # Respond with 403 if token is invalid
        return str(e), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
