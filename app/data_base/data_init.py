from base import declarative_base, Column, Integer, String, Boolean, DateTime, ForeignKey ,SessionLocal, User, Repository, BannedUser, CommitMark, SkillScore, SkillMarketValue, ApplicationAdmins
from datetime import datetime

def grant_admin(db, user_id):
    admin = ApplicationAdmins(user_id=user_id)
    db.add(admin)
    db.commit()

def init_db():
    db = SessionLocal()
    
    if db.query(User).first():
        db.close()
        return

    user1 = User(
        username="shadow_coder",
        email="coder@shadowskills.com",
        full_name="Shadow Coder",
        hashed_password="fake_hashed_secret",
        is_active=True
    )
    user2 = User(
        username="bad_actor",
        email="bad@shadowskills.com",
        full_name="Bad Actor",
        hashed_password="fake_hashed_secret",
        is_active=False
    )
    db.add_all([user1, user2])
    db.commit()

    repo = Repository(
        name="ShadowSkills",
        owner="megaladonntm-arch",
        url="https://github.com/megaladonntm-arch/ShadowSkills"
    )
    db.add(repo)
    db.commit()

    ban = BannedUser(user_id=user2.id, reason="Нарушение правил сообщества")
    mark = CommitMark(user_id=user1.id, commit_sha="a1b2c3d", mark=95)
    score = SkillScore(skill_name="Python", score=88, project_id=repo.id)
    market_val = SkillMarketValue(skill_name="Python", market_value=5000, project_id=repo.id)

    db.add_all([ban, mark, score, market_val])
    
    grant_admin(db, user1.id)

    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
