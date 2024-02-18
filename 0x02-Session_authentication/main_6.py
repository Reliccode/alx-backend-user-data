#!/usr/bin/env python3
""" Main 6
"""
import base64

from flask import request
from api.v1.auth.basic_auth import BasicAuth
from models.user import User

""" Create a user test """
user_email = "bob@hbtn.io"
user_clear_pwd = "H0lbertonSchool98!"

user = User()
user.email = user_email
user.password = user_clear_pwd
print("New user: {}".format(user.id))
user.save()

res = user.search({'email': user_email})
print(res[0].id)
# Convert each matching object to JSON representation
json_results = [obj.to_json() for obj in res]

# Print the JSON representation of each object
for json_obj in json_results:
    print(json_obj)
