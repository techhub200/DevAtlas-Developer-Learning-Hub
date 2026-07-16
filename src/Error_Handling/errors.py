from typing import Any, Callable

from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class DevAtlas_Exception(Exception):
    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: DevAtlas_Exception):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


# ---- Auth / token ----

class InvalidToken(DevAtlas_Exception):
    """User has provided an invalid or expired token"""
    pass


class RevokedToken(DevAtlas_Exception):
    """User has provided a token that has been revoked"""
    pass


class AccessTokenRequired(DevAtlas_Exception):
    """User has provided a refresh token when an access token is needed"""
    pass


# ---- Authorization ----

class Forbidden(DevAtlas_Exception):
    """User is not allowed to perform this operation"""
    pass


# ---- User / uniqueness ----

class UserAlreadyTaken(DevAtlas_Exception):
    """User already exists (email/username conflict)"""
    pass


class UserNameTaken(DevAtlas_Exception):
    """This username is already taken"""
    pass


class UserEmailTaken(DevAtlas_Exception):
    """This email is already taken"""
    pass


# ---- Resource errors ----

class NotFound(DevAtlas_Exception):
    """Requested resource not found"""
    pass


class Conflict(DevAtlas_Exception):
    """Conflict with current state (e.g., duplicate)"""
    pass


# ---- Upload / file errors ----

class UnsupportedMediaType(DevAtlas_Exception):
    """Unsupported upload content type"""
    pass


class RequestEntityTooLarge(DevAtlas_Exception):
    """Uploaded file is too large"""
    pass


def register_error_handlers(app: FastAPI):

    # Token/auth errors
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "error_code": "InvalidToken",
                "message": "User has provided an invalid or expired token",
            },
        ),
    )

    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "error_code": "RevokedToken",
                "message": "User has provided a token that has been revoked",
            },
        ),
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "error_code": "AccessTokenRequired",
                "message": "User has provided a refresh token when an access token is needed",
            },
        ),
    )

    # Authorization errors
    app.add_exception_handler(
        Forbidden,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "error_code": "Forbidden",
                "message": "User is not allowed to perform this operation",
            },
        ),
    )

    # User conflicts
    app.add_exception_handler(
        UserAlreadyTaken,
        create_exception_handler(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            initial_detail={
                "error_code": "UserAlreadyTaken",
                "message": "User already exists",
            },
        ),
    )

    app.add_exception_handler(
        UserNameTaken,
        create_exception_handler(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            initial_detail={
                "error_code": "UserNameTaken",
                "message": "User name already exists",
            },
        ),
    )

    app.add_exception_handler(
        UserEmailTaken,
        create_exception_handler(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            initial_detail={
                "error_code": "UserEmailTaken",
                "message": "User email already exists",
            },
        ),
    )

    app.add_exception_handler(
        Conflict,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={
                "error_code": "Conflict",
                "message": "Conflict with current state",
            },
        ),
    )

    # Not found
    app.add_exception_handler(
        NotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "error_code": "NotFound",
                "message": "Requested resource not found",
            },
        ),
    )

    # Upload picture errors
    app.add_exception_handler(
        UnsupportedMediaType,
        create_exception_handler(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            initial_detail={
                "error_code": "UnsupportedMediaType",
                "message": "Unsupported upload content type",
            },
        ),
    )

    app.add_exception_handler(
        RequestEntityTooLarge,
        create_exception_handler(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            initial_detail={
                "error_code": "RequestEntityTooLarge",
                "message": "Uploaded file is too large",
            },
        ),
    )