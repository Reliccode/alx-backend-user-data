#!/usr/bin/env python3
"""
Hash passwords
"""


import bcrypt
# import hashlib


def _hash_password(password: str) -> bytes:
    """
    hashes passwd using bcrypt.hashpw
    """
    # encode password as bytes
    password_bytes = password.encode('utf-8')

    # Generating Salt
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_password
