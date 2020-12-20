from typing import Optional

from fastapi import FastAPI, Request, Cookie, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

import util, db, models

app = FastAPI()

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    #allow_origin_regex='https://.*\.example\.org'
    #allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await db.init()

@app.on_event("shutdown")
def shutdown_event():
    pass

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return await JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=models.ErrResponseModel(
            err="Bad Request",
            msg=f"Couldn't validate request data. {exc}"
        )
    )

@app.post('/register')
async def create_user(_request: models.RegisterRequest):
    await db.create_user(_request)
    return await JSONResponse(
        status=status.HTTP_201_CREATED,
        content=models.OkResponseModel(
            ok="Successful",
            msg=f"User {_request['username']} created successfully!"
        )
    )

@app.get('/user/{user_id}')
async def get_user(user_id: int):
    result = await db.get_user_s(user_id)
    if "err" in result:
        return await JSONResponse(
            status=status.HTTP_404_NOT_FOUND,
            content=models.ErrResponseModel(result)
        )
    return await JSONResponse(
        status=status.HTTP_200_OK,
        content=models.OkResponseModel(result)
    )

@app.delete('/user/{user_id}')
async def delete_user(user_id: int):
    deleted = await db.delete_user(user_id)
    if deleted:
        return await JSONResponse(
            status=status.HTTP_200_OK,
            content=models.OkResponseModel(
                ok="Deleted",
                msg=f"User <{user_id}> deleted successfully!"
            )
        )
    return await JSONResponse(
        status=status.HTTP_404_NOT_FOUND,
        content=models.ErrResponseModel(
            err="Not Found",
            msg=f"There is no user with ID <{user_id}>!"
        )
    )

@app.get('/users')
async def get_users():
    result = await db.get_user_s()
    if "err" in result:
        return await JSONResponse(
            status=status.HTTP_404_NOT_FOUND,
            content=models.ErrResponseModel(result)
        )
    return await JSONResponse(
        status=status.HTTP_200_OK,
        content=models.OkResponseModel(result)
    )

@app.post('/login')
async def login(_request: models.LoginRequest, jwt_token: Optional[str] = Cookie(None)):
    if jwt_token:
        decoded = util.jwt_decode(jwt_token)
        if 'err' in decoded:
            response = JSONResponse(
                status=status.HTTP_400_BAD_REQUEST,
                content=models.ErrResponseModel(
                    err="JWT Invalid",
                    msg="Invalid JWT Token. Please log in again."
                )
            )
            response.set_cookie(key="jwt_token", value='')
            return response
        else:
            return JSONResponse(
                status=status.HTTP_400_BAD_REQUEST,
                content=models.ErrResponseModel(
                    err="Logged in",
                    msg=f"Already logged in as <{decoded['username']}>."
                )
            )

    if await db.check_password(_request['username'], _request['password']):
        response = JSONResponse(
            status=status.HTTP_200_OK,
            content=models.OkResponseModel(
                ok="Logged in",
                msg=f"Logged in as <{_request['username']}>."
            )
        )
        response.set_cookie(key="jwt_token", value=util.jwt_encode(_request['username']))
        return response

@app.put('/change_password')
async def change_password(_request: models.ChangePasswordRequest, jwt_token: Optional[str] = Cookie(None)):
    if not jwt_token:
        return await JSONResponse(
            status=status.HTTP_401_UNAUTHORIZED,
            content=models.ErrResponseModel(
                err="Unauthorized",
                msg="You must login first to change your password!"
            )
        )

    decoded = util.jwt_decode(jwt_token)
    if "err" in decoded:
        return await JSONResponse(
            status=status.HTTP_401_UNAUTHORIZED,
            content=models.ErrResponseModel(
                err="Unauthorized",
                msg="You must re-login to change your password!"
            )
        )

    await db.change_password(decoded["username"], util.hash_password(_request["password"]))
    return await JSONResponse(
        status=status.HTTP_200_OK,
        content=models.OkResponseModel(
            ok="Successful",
            msg=f"Password changed for user {decoded['username']}"
        )
    )

@app.get('/logout')
async def logout(jwt_token: Optional[str] = Cookie(None)):
    if jwt_token:
        decoded = util.jwt_decode(jwt_token)
        if 'err' in decoded:
            response = JSONResponse(
                status=status.HTTP_401_UNAUTHORIZED,
                content=models.ErrResponseModel(
                    err="JWT Invalid",
                    msg="Invalid JWT Token. Please log in again."
                )
            )
            response.set_cookie(key="jwt_token", value='')
            return response
        else:
            response = JSONResponse(
                status=status.HTTP_200_OK,
                content=models.OkResponseModel(
                    err="Logged out",
                    msg=f"Logged out. User: <{decoded['username']}>."
                )
            )
            response.set_cookie(key="jwt_token", value='')
            return response

    return JSONResponse(
        status=status.HTTP_401_BAD_REQUEST,
        content=models.ErrResponseModel(
            err="JWT Token not found.",
            msg="Not logged in."
        )
    )
