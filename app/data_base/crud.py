from sqlalchemy.orm import Session

from app.data_base import base as models
from app.data_base.base import SessionLocal
from schemas.user import UserCreate, UserUpdate
from schemas.repository import RepositoryCreate, RepositoryUpdate


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#user crud
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_active_users(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.User)
        .filter(models.User.is_active.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_user_count(db: Session) -> int:
    return db.query(models.User).count()


def create_user(db: Session, user: UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        password=user.password,
        is_active=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user


def deactivate_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    return db_user


def activate_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    db_user.is_active = True
    db.commit()
    db.refresh(db_user)
    return db_user

#repos crud


def get_repository(db: Session, repository_id: int):
    return (
        db.query(models.Repository)
        .filter(models.Repository.id == repository_id)
        .first()
    )


def get_repository_by_url(db: Session, url: str):
    return db.query(models.Repository).filter(models.Repository.url == url).first()


def get_user_repositories(db: Session, user_id: int):
    return (
        db.query(models.Repository)
        .filter(models.Repository.owner_id == user_id)
        .all()
    )


def create_repository(
    db: Session,
    user_id: int,
    repository: RepositoryCreate,
):
    db_repo = models.Repository(
        name=repository.name,
        owner=repository.owner,
        url=str(repository.url),
        owner_id=user_id,
    )
    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)
    return db_repo


def update_repository(
    db: Session,
    repository_id: int,
    repository_update: RepositoryUpdate,
):
    db_repo = get_repository(db, repository_id)
    if not db_repo:
        return None

    update_data = repository_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_repo, field, value)

    db.commit()
    db.refresh(db_repo)
    return db_repo


def delete_repository(db: Session, repository_id: int):
    db_repo = get_repository(db, repository_id)
    if not db_repo:
        return None

    db.delete(db_repo)
    db.commit()
    return db_repo


#bans crud

def ban_user(db: Session, user_id: int, reason: str):
    db_ban = models.BannedUser(
        user_id=user_id,
        reason=reason,
    )
    db.add(db_ban)
    db.commit()
    db.refresh(db_ban)
    return db_ban


def unban_user(db: Session, user_id: int):
    db_ban = (
        db.query(models.BannedUser)
        .filter(models.BannedUser.user_id == user_id)
        .first()
    )
    if not db_ban:
        return None

    db.delete(db_ban)
    db.commit()
    return db_ban


def is_user_banned(db: Session, user_id: int) -> bool:
    return (
        db.query(models.BannedUser)
        .filter(models.BannedUser.user_id == user_id)
        .first()
        is not None
    )


def get_banned_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BannedUser).offset(skip).limit(limit).all()
