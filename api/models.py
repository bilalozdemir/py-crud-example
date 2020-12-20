from typing import Optional, Union, List, Dict

from pydantic import BaseModel, ValidationError, validator, EmailStr

from api import util

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    password: str
    password_check: str

    class Config:
        anystr_strip_whitespace = True

    _check_username_validity = validator('username', allow_reuse=True)(util.check_username_validity)
    _check_password_safety = validator('password', allow_reuse=True)(util.check_password_safety)

    @validator('password_check')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords doesn\'t match!')


class LoginRequest(BaseModel):
    username: str
    password: str

    class Config:
        anystr_strip_whitespace = True

    _check_username_validity = validator('username', allow_reuse=True)(util.check_username_validity)

    @validator('password')
    def password_length(cls, v):
        assert length(v), 'Password length must be greater than or equal to 8!'
        return v

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    new_password_check: str

    class Config:
        anystr_strip_whitespace = True

    @validator('current_password')
    def password_length(cls, v):
        assert length(v), 'Password length must be greater than or equal to 8!'
        return v

    _check_password_safety = validator('new_password', allow_reuse=True)(util.check_password_safety)

    @validator('new_password_check')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords doesn\'t match!')


class OkResponseModel(BaseModel):
    ok: str
    msg: str
    data: Optional[Union[Dict, List[Dict]]]

class ErrResponseModel(BaseModel):
    err: str
    msg: str
