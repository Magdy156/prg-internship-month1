from fastapi.responses import JSONResponse
from fastapi import status
from utils.exceptions import (
    UserNotFoundException,
    InvalidCredentialsException,
    JWTDecodeException,
    UsernameExistsException,
    TodoListNotFoundException,
    TodoItemNotFoundException,
)

class ExceptionHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExceptionHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # Prevent re-initialization
            self.initialized = True

    async def handle(self, request, exc: Exception) -> JSONResponse:
        print(f"Exception: {type(exc).__name__}: {str(exc)}")
        
        if isinstance(exc, UserNotFoundException):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": exc.detail},
            )
        elif isinstance(exc, InvalidCredentialsException):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": exc.detail},
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif isinstance(exc, JWTDecodeException):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": exc.detail},
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif isinstance(exc, UsernameExistsException):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": exc.detail},
            )
        elif isinstance(exc, TodoListNotFoundException):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": exc.detail},
            )
        elif isinstance(exc, TodoItemNotFoundException):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": exc.detail},
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal server error"},
            )
