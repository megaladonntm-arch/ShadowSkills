from data_base.base import SessionLocal

def get_all_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users