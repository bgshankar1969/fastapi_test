from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from config.db import conn
from models.users import users
from schemas.user import User
from schemas.auth import Token, TokenData
from auth.auth import get_current_active_user, authenticate_user, user_login

user = APIRouter()

@user.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return user_login(form_data.username, form_data.password)

@user.get('/users')
def fetch_users(current_user: User = Depends(get_current_active_user)):
    return conn.execute(users.select()).fetchall()

@user.get('/user/{id}')
def get_user(id: int, current_user: User = Depends(get_current_active_user)):
    return conn.execute(users.select().where(users.c.id == id)).fetchone()

@user.post('/user')
def add_user(user_info: User, current_user: User = Depends(get_current_active_user)):
    return conn.execute(users.insert().values(
        name = user_info.name, 
        email = user_info.email,
        password = user_info.password
        ))

@user.put('/user/{id}')
def update_user(id: int, user_info: User, current_user: User = Depends(get_current_active_user)):
    return conn.execute(users.update().values(
        name = user_info.name, 
        email = user_info.email,
        password = user_info.password
        ).where(users.c.id==id) )

@user.delete('/user/{id}')
def delete_user(id: int, current_user: User = Depends(get_current_active_user)):
    return conn.execute(users.delete().where(users.c.id==id))
