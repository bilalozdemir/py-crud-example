import os
import re
import base64
import bcrypt
import datetime
from typing import Union

import jwt

if os.getenv('PRODUCTION'):
    JWT_SECRET_KEY = base64.b64encode(os.getenv('JWT_SECRET_KEY')).decode('utf-8')
else:
    JWT_SECRET_KEY = 'atidoBWDDEz6VDmfylGLxmfEUjvr9Dca'

def check_email_validity(mail: str) -> bool:
    regex = r"^[a-z0-9]?[\._]?[a-z0-9]+[@]\w+[.]\w+$"
    return re.search(regex, mail)

def check_username_validity(_username: str) -> Union[str, AssertionError]:
    assert len(_username) >= 5, 'Length of username must be greater than or equal to 5'
    assert _username.isalnum(), 'Username must be alphanumeric.'
    assert _username.lower() == _username, 'Username must be lowercase'
    return _username

def check_password_safety(_password: str) -> Union[str, AssertionError]:
    assert _password, 'Password field can\'t be empty!'
    assert len(_password) >= 8, 'Password length must be greater than or equal to 8!'
    assert _password.lower() != _password and _password.upper() != _password, 'Must contain at least one uppercase and one lowercase character'
    assert [char for char in '@$!_?' if char in _password], 'Must contain at least one of @$!_?'
    assert [num for num in '0123456789' if num in _password], 'Must contain at least one number'
    assert not any(c in _password for c in '<>/\\{}[]`~;:()\'\".,'), 'Can\'t contain any of <>/\\{}[]`~;:()\'\".,'
    assert not any(not c.isascii() for c in _password), 'Can\'t contain non-ascii characters'
    return _password

def hash_password(_pw: str) -> bytes:
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(_pw.encode('utf-8'), salt)
    return hash.decode('utf-8')

def check_password(_pw: str, hashed_pw: bytes) -> bool:
    return bcrypt.checkpw(_pw.encode('utf-8'), hashed_pw.encode('utf-8'))

def jwt_encode(username: str) -> str:
    _payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
    }
    return jwt.encode(_payload, JWT_SECRET_KEY, algorithm='HS256')

def jwt_decode(jwt_token: str) -> dict:
    try:
        return jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms='HS256')
    except jwt.exceptions.ExpiredSignatureError as _e:
        return {'err': 'Expired', 'msg': _e}
    except (jwt.exceptions.Decode, jwt.exceptions.InvalidSignatureError) as _e:
        return {'err': 'Failed Decoding', 'msg': _e}
