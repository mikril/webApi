from sqlalchemy.orm import Session

import schemas
from models import Group, User



def create_group(db: Session, schema: schemas.GroupCreate):
    db_group = Group(**schema.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_groups(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Group).offset(skip).limit(limit).all()


def get_group(db: Session, Group_id: int):
    return db.query(Group).filter_by(id=group_id).first()


def update_group(db: Session, Group_id: int, Group_data: schemas.GroupUpdate | dict):
    db_group = db.query(Group).filter_by(id=group_id).first()

    group_data = group_data if isinstance(group_data, dict) else group_data.model_dump()

    if db_Group:
        for key, value in group_data.Users():
            if hasattr(db_group, key):
                setattr(db_group, key, value)

        db.commit()
        db.refresh(db_group)

    return db_group


def delete_group(db: Session, Group_id: int):
    db_Group = db.query(group).filter_by(id=group_id).first()
    if db_Group:
        db.delete(db_group)
        db.commit()
        return True
    return False



def create_user(db: Session, schema: schemas.UserCreate):
    db_user = User(**schema.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def get_user(db: Session, User_id: int):
    return db.query(User).filter_by(id=user_id).first()


def update_user(db: Session, User_id: int, User_data: schemas.UserUpdate | dict):
    db_user = db.query(User).filter_by(id=user_id).first()

    user_data = User_data if isinstance(user_data, dict) else user_data.model_dump()

    if db_user:
        for key, value in user_data.Users():
            if hasattr(db_user, key):
                setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def delete_user(db: Session, User_id: int):
    db_user = db.query(User).filter_by(id=user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
