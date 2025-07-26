from fastapi import HTTPException, status

class UserNotFoundException(Exception):
    def __init__(self, detail: str = "User not found"):
        self.detail = detail

class InvalidCredentialsException(Exception):
    def __init__(self, detail: str = "Incorrect username or password"):
        self.detail = detail

class JWTDecodeException(Exception):
    def __init__(self, detail: str = "Could not validate credentials"):
        self.detail = detail
