#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from api.v1.views.index import status, stats, unauthorized, forbidden
from api.v1.views.users import view_all_users, view_one_user
from flask import Blueprint
from models.user import User

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# register routes

User.load_from_file()
