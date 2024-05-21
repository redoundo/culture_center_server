from .dbconnection import DbConnection
from sqlalchemy.orm import Session
from sqlalchemy import delete, update, insert, select
from hashlib import sha256
from .tablemodels import *


def delete_applied_by_lecture_id_user_id(lecture_id: int, user_id: int):
    session: Session = DbConnection().get_session()
    stmt = delete(Applied).where(Applied.appliedLectureId == lecture_id and Applied.appliedUserId == user_id)
    session.execute(stmt)
    session.commit()
    session.close()
    return


def delete_liked_by_lecture_id_user_id(lecture_id: int, user_id: int):
    session: Session = DbConnection().get_session()
    stmt = delete(Liked).where(Liked.likedLectureId == lecture_id and Liked.likedUserId == user_id)
    session.execute(stmt)
    session.commit()
    session.close()
    return


def delete_all_applied_by_user_id(user_id: int):
    session: Session = DbConnection().get_session()
    stmt = delete(Applied).where(Applied.appliedUserId == user_id)
    session.execute(stmt)
    session.commit()
    session.close()
    return


def delete_all_liked_by_user_id(user_id: int):
    session: Session = DbConnection().get_session()
    stmt = delete(Liked).where(Liked.likedUserId == user_id)
    session.execute(stmt)
    session.commit()
    session.close()
    return


def insert_applied_by_user_id(user_id: int, lecture_id: int):
    session: Session = DbConnection().get_session()
    exist_applied = session.query(Applied).where(Applied.appliedLectureId == lecture_id).where( Applied.appliedUserId == user_id).count()
    if exist_applied == 0:
        stmt = insert(Applied).values(appliedLectureId=lecture_id, appliedUserId=user_id)
        session.execute(stmt)
    session.commit()
    session.close()
    return


def insert_liked_by_user_id(user_id: int, lecture_id: int):
    session: Session = DbConnection().get_session()
    exist_liked = session.query(Liked).where(Liked.likedLectureId == lecture_id).where(Liked.likedUserId == user_id).count()
    if exist_liked == 0:
        stmt = insert(Liked).values(likedLectureId=lecture_id, likedUserId=user_id)
        session.execute(stmt)
    session.commit()
    session.close()
    return


def withdraw_user_by_user_id(user_id: int):
    session: Session = DbConnection().get_session()
    stmt = delete(Users).where(Users.userId == user_id)
    session.execute(stmt)
    session.commit()
    session.close()
    return


def sign_in_user(email: str, password: str, nickname: str, provider: str, providers_id: str):
    session: Session = DbConnection().get_session()
    sha_password: str = sha256(password.encode()).hexdigest()
    stmt = insert(Users).values(email=email, nickname=nickname, password=sha_password,
                                snsProvider=provider, snsProviderId=providers_id)
    session.execute(stmt)
    session.commit()
    session.close()
    return


def update_user_by_user_id(user_id: int, nickname: str):
    session: Session = DbConnection().get_session()
    stmt = update(Users).values({"nickname": nickname}).where(Users.userId == user_id)
    session.execute(stmt)
    session.commit()
    session.close()
    return


def register_fcm_receiver(user_id: int, token: str):
    session: Session = DbConnection().get_session()
    stmt = update(Users).values({"wantFcmMessage": True}, {"fcmToken": token}).where(Users.userId == user_id)
    session.execute(stmt)
    session.commit()
    session.close()
    return


