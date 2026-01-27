#make crud
from app.data_base import base as models
from app.data_base.base import SessionLocal
from sqlalchemy.orm import Session      
from schemas.user import UserCreate, UserUpdate


#here is prob with import i will try to fix it within 10 minutes


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=user.hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    for var, value in vars(user_update).items():
        setattr(db_user, var, value) if value else None
    db.commit()
    db.refresh(db_user)
    return db_user
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user
def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_active_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.is_active == True).offset(skip).limit(limit).all()

def deactivate_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    return db_user

def activate_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db_user.is_active = True
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_count(db: Session):
    return db.query(models.User).count()
def get_users_by_full_name(db: Session, full_name: str):
    return db.query(models.User).filter(models.User.full_name == full_name).all()

def get_users_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).all()

def get_users_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).all()

def ban_user(db: Session, user_id: int, reason: str):
    db_banned_user = models.BannedUser(
        user_id=user_id,
        reason=reason
    )
    db.add(db_banned_user)
    db.commit()
    db.refresh(db_banned_user)
    return db_banned_user
def unban_user(db: Session, user_id: int):
    db_banned_user = db.query(models.BannedUser).filter(models.BannedUser.user_id == user_id).first()
    if not db_banned_user:
        return None
    db.delete(db_banned_user)
    db.commit()
    return db_banned_user
def is_user_banned(db: Session, user_id: int):
    return db.query(models.BannedUser).filter(models.BannedUser.user_id == user_id).first() is not None
def get_all_banned_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BannedUser).offset(skip).limit(limit).all()
