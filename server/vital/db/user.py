import sqlite3

from pydantic import BaseModel



class User(BaseModel):
    user_id: str
    password: str = "1234"
