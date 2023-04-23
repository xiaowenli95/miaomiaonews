from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.app.crud.todo_crud import get_user_todos, add_todo, update_todo, delete_todo
from src.app.crud.user_crud import get_current_user
from src.app.db import get_db
from src.app.models.usermodel import UserModel
from src.app.schemas.todo_schemas import TodoSchema, TodoBaseSchema, TodoUpdateSchema, TodoResponseSchema

todo_router = APIRouter()


@todo_router.get('', response_model=List[TodoResponseSchema])
def get_my_todos_view(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    todos = get_user_todos(db, current_user)
    return todos


@todo_router.post('', response_model=List[TodoResponseSchema])
def add_todo_view(
        todo_data: TodoBaseSchema,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user),
):
    add_todo(
        db,
        current_user,
        todo_data,
    )
    todos = get_user_todos(db, current_user)
    return todos


@todo_router.put('', response_model=List[TodoResponseSchema])
def update_todo_view(
        todo_data: TodoUpdateSchema,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user),
):
    update_todo(
        db,
        new_todo=todo_data,
    )
    todos = get_user_todos(db, current_user)
    return todos


@todo_router.delete('/{todo_id:int}', response_model=List[TodoResponseSchema])
def delete_todo_view(
        todo_id: int,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)
):
    delete_todo(db, todo_id)
    todos = get_user_todos(db, current_user)
    return todos
