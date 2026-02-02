from data_base.base import SessionLocal
from data_base.crud import (
    create_user,
    get_user_by_username,
)

from schemas.user import UserCreate

from services.commit_analyzer import CommitAnalyzer


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = SessionLocal()
    try:
        users = (
            UserCreate(
                username="admin",
                email="f7TlI@example.com",
                full_name="Admin User",
                password="aasdasad",
            ),
            UserCreate(
                username="Ubaydullin",
                email="Ubaydullin@bk.ru",
                full_name="Ubaydullin",
                password="aasdasad",
            ),
            UserCreate(
                username="testuser",
                email="test@mail.com",
                full_name="Test User",
                password="testpassword",
            ),
            UserCreate(
                username="anotheruser",
                email="another@example.com",
                full_name="Another User",
                password="anotherpassword",
            ),
        )

        for user in users:
            if not get_user_by_username(db, user.username):
                create_user(db, user)
    finally:
        db.close()


def analyze_commit():
    analyzer = CommitAnalyzer(
        repo_owner="megaladonntm-arch",
        repo_name="ShadowSkills",
        commit_hash="d0e7d528d11e5270da48ad837031a69381049b34",
    )
    return analyzer.analyze_commit()


def main():
    init_db()
    report = analyze_commit()
    print("Done")
    print(report)


if __name__ == "__main__":
    main()
