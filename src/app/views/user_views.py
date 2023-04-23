import os
from datetime import timedelta
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED
from src.app.crud.user_crud import get_current_user, get_all_users, get_user_by_email, add_user
from src.app.db import get_db
from src.app.models.usermodel import UserModel
from src.app.schemas.token_schemas import TokenSchema
from src.app.schemas.user_schemas import UserSchema, UserCreateSchema
from src.app.utils.security import authenticate_user, create_access_token

ACCESS_TOKEN_EXPIRE_MINUTES = 60

user_router = APIRouter()


@user_router.get("", response_model=List[UserSchema])
def users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return list(users)


@user_router.get("/{email:str}", response_model=UserSchema)
def get_user(email: str, db: Session = Depends(get_db)) -> UserSchema:
    user = get_user_by_email(db, email)
    if user:
        return user
    else:
        return {'message': 'user not found'}, 404


@user_router.post("", response_model=UserSchema)
def sign_up(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="email exist",
        )
    new_user = add_user(db, user_data)
    return new_user


@user_router.post("/login", response_model=TokenSchema)
def login_for_access_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    user_data = authenticate_user(db, form_data.username, form_data.password)
    if not user_data:
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            detail="invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_expires_date = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user_data.email},
        expires_delta=token_expires_date,
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@user_router.get("me", response_model=UserSchema)
def get_current_user(user_data: UserModel = Depends(get_current_user)):
    return user_data

