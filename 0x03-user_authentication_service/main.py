#!/usr/bin/env python3
"""
End-to-end integration test for the Flask application.
"""

import requests

BASE_URL = "http://localhost:5000"  # Update with your Flask server address


def register_user(email: str, password: str) -> None:
    """
    Register a new user.
    """
    endpoint = "/users"
    data = {"email": email, "password": password}
    response = requests.post(BASE_URL + endpoint, data=data)
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with incorrect password.
    """
    endpoint = "/sessions"
    data = {"email": email, "password": password}
    response = requests.post(BASE_URL + endpoint, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Log in with the provided email and password.
    """
    endpoint = "/sessions"
    data = {"email": email, "password": password}
    response = requests.post(BASE_URL + endpoint, data=data)
    assert response.status_code == 200
    return response.cookies.get("session_id")


# Implement the remaining functions with docstrings and compliance with PEP 8

def profile_unlogged() -> None:
    """
    Get profile while unlogged.
    """
    endpoint = "/profile"
    response = requests.get(BASE_URL + endpoint)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Get profile while logged in.
    """
    endpoint = "/profile"
    cookies = {"session_id": session_id}
    response = requests.get(BASE_URL + endpoint, cookies=cookies)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """
    Log out the user.
    """
    endpoint = "/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(BASE_URL + endpoint, cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Get reset password token.
    """
    endpoint = "/reset_password"
    data = {"email": email}
    response = requests.put(BASE_URL + endpoint, data=data)
    assert response.status_code == 200
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update user's password.
    """
    endpoint = "/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password}
    response = requests.put(BASE_URL + endpoint, data=data)
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
