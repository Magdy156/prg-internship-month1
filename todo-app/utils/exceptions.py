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

class UsernameExistsException(Exception):
    def __init__(self, detail: str = "Username already exists"):
        self.detail = detail

class TodoListNotFoundException(Exception):
    def __init__(self, detail: str = "TodoList not found"):
        self.detail = detail

class TodoItemNotFoundException(Exception):
    def __init__(self, detail: str = "TodoItem not found"):
        self.detail = detail
