import sys
import os


from data_base.crud import create_user, get_user_by_email, get_user_by_username, update_user, delete_user, get_all_users, get_user, get_active_users, deactivate_user, activate_user, get_user_count, get_users_by_full_name, get_users_by_email, get_users_by_username, ban_user, unban_user
from data_base.base import SessionLocal
from schemas.user import UserCreate, UserUpdate
from sqlalchemy.orm import Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db_gen = get_db()
    db: Session = next(db_gen)
    try:
        if not get_user_by_username(db, "admin"):
            admin_user = UserCreate(
                username="admin",
                email="f7TlI@example.com",
                full_name="Admin User",
                hashed_password="adminpassword"
            )
            create_user(db, admin_user)
    finally:
        next(db_gen, None)

def say_hello():
    return "Hello from crud.py"
init_db()