from typing import Sequence

from .dbconnection import DbConnection
from sqlalchemy.orm import Session
from sqlalchemy import select, text
from .tablemodels import *


def validate_string(string: str) -> bool:
    """
    문자열이 유효한지 검증
    :param string: 검증이 필요한 문자열
    :return: 유효성 여부
    """
    return string is not None and string != "null" and len(string) > 0


def select_users_info_by_user_id(user_id: int) -> dict | None:
    """
    사용자 아이디 로 사용자 정보와 좋아요 누른 강좌  및 신청한 강좌 전부 반환.
    :param user_id: 사용자 아이디
    :return: 사용자 및 관련 정보 일체 반환.
    """
    session: Session = DbConnection().get_session()
    stmt = select(Users).where(Users.userId == user_id)
    result = session.scalar(stmt)
    if result is None:
        return result
    applied_results = select_all_applied_lectures_by_user_id(result.userId)
    liked_results = select_all_liked_lectures_by_user_id(result.userId)
    session.close()
    return {
        "user": result,
        "applied": applied_results,
        "liked": liked_results
    }


def select_user_by_user_id(user_id: int) -> Users:
    """
    사용자 아이디로 사용자 찾기
    :param user_id: 사용자 아이디
    :return: 사용자 정보
    """
    session: Session = DbConnection().get_session()
    stmt = select(Users).where(Users.userId == user_id)
    user: Users = session.scalar(stmt)
    session.close()
    return user


def select_user_by_email(email: str) -> Users:
    """
    이메일로 사용자 찾기
    :param email: 사용자 이메일
    :return: 사용자 정보
    """
    session: Session = DbConnection().get_session()
    stmt = select(Users).where(Users.email == email)
    result = session.scalar(stmt)
    session.close()
    return result


def check_user_nickname_is_unique(nickname: str) -> bool:
    """
    사용자가 입력한 닉네임을 사용할 수 있는지 확인하기 위해 해당 닉네임과 동일한 닉네임의 수가 얼마나 되는지 확인.
    :param nickname: 저장하고 싶은 닉네임.
    :return: 사용 가능 여부
    """
    session: Session = DbConnection().get_session()
    uniqueness = session.query(Users).where(Users.nickname == nickname).count()
    session.close()
    return uniqueness == 0


def check_user_already_exists(email: str) -> bool:
    """
    해당 이메일로 가입한 적이 있는지 확인.
    :param email: 사용자의 이메일
    :return: 존재 여부
    """
    session: Session = DbConnection().get_session()
    exist: int = session.query(Users).where(Users.email == email).count()
    session.close()
    return exist == 0


def select_all_applied_lectures_by_user_id(user_id: int) -> list[Lectures]:
    """
    사용자가 신청한 강좌의 내용들을 가져온다.
    :param user_id: 사용자 아이디
    :return: 강좌 내용
    """
    session: Session = DbConnection().get_session()
    stmt = select(Applied.appliedLectureId).where(Applied.appliedUserId == user_id)
    result: Sequence[int] = session.scalars(stmt).all()
    lectures: list[Lectures] = []
    for item in result:
        query = select(Lectures).where(Lectures.lectureId == item)
        lecture = session.scalar(query)
        lectures.append(lecture)
    session.close()
    return lectures


def select_all_liked_lectures_by_user_id(user_id: int) -> list[Lectures]:
    """
    사용자가 좋아요 한 강좌 내용.
    :param user_id: 사용자 아이디
    :return: 좋아요 한 강좌 내용
    """
    session: Session = DbConnection().get_session()
    stmt = select(Liked.likedLectureId).where(Liked.likedUserId == user_id)
    lectures: list[Lectures] = []
    result: Sequence[int] = session.scalars(stmt).all()
    for item in result:
        query = select(Lectures).where(Lectures.lectureId == item)
        lecture = session.scalar(query)
        lectures.append(lecture)
    session.close()
    return lectures


def select_all_categories() -> Sequence[Categories]:
    """
    모든 카테고리 반환.
    :return:
    """
    session: Session = DbConnection().get_session()
    stmt = select(Categories)
    result = session.scalars(stmt).all()
    session.close()
    return result


def select_all_targets() -> Sequence[Targets]:
    """
    모든 대상 반환.
    :return:
    """
    session: Session = DbConnection().get_session()
    stmt = select(Targets)
    result = session.scalars(stmt).all()
    session.close()
    return result


def select_centers_by_type(types: str) -> Sequence[Centers]:
    session: Session = DbConnection().get_session()
    stmt = select(Centers).where(Centers.centerType == types)
    result = session.scalars(stmt).all()
    session.close()
    return result


def select_all_center_type() -> Sequence[str]:
    session: Session = DbConnection().get_session()
    stmt = select(Centers.centerType)
    result = session.scalars(stmt).all()
    session.close()
    return result


def select_lecture_by_lecture_id(lecture_id: int) -> Lectures:
    session: Session = DbConnection().get_session()
    stmt = select(Lectures).where(Lectures.lectureId == lecture_id)
    result = session.scalar(stmt)
    session.close()
    return result


def select_all_lectures_by_search_options(**kwargs) -> Sequence[Lectures]:
    page_num: int = kwargs.get("page")
    keyword: str = kwargs.get("keyword")
    center_type: str = kwargs.get("centerType")
    target: str = kwargs.get("targetId")
    category: str = kwargs.get("categoryId")

    text_query: str = "SELECT * FROM lectures"
    query_list: list[str] = []

    session: Session = DbConnection().get_session()

    if validate_string(category):
        category_name: str = session.query(Categories.categoryName).where(Categories.categoryId == int(category)).one()
        query_list.append(f"category='{category_name}'")

    if validate_string(target):
        target_name: str = session.query(Targets.targetName).where(Targets.targetId == int(target)).one()
        query_list.append(f"target='{target_name}'")

    if validate_string(keyword):
        query_list.append(f"title LIKE '%{keyword}%'")

    if validate_string(center_type):
        query_list.append(f"type='{center_type}'")

    if query_list.__len__() > 0:
        text_query = text_query + "WHERE " + " AND ".join(query_list)

    if page_num is not None:
        text_query = text_query + f" LIMIT {page_num * 16}, 16;"
    else:
        text_query = text_query + " LIMIT 1, 16;"

    stmt = select(Lectures).from_statement(text(text_query))
    results = session.scalars(stmt).all()
    session.close()
    return results


def today_sign_in_user_mount() -> int:
    query: str = f"SELECT Count(*) AS count FORM users WHERE DATE_FORMAT(registerDate, '%Y-%m-%d')={datetime.now()};"
    stmt = select(Users).from_statement(text(query))
    session: Session = DbConnection().get_session()
    mount: int = session.scalars(stmt).one()
    session.close()
    return mount


def get_registered_fmc_token(user_id: int) -> str | None:
    """
    fcm 메시지를 보내기 위해서 사용자의 아이디로 존재 하는 토큰을 가져 온다.
    :param user_id: 사용자 아이디
    :return: fcm token | None
    """
    session: Session = DbConnection().get_session()
    token: str = session.query(Users.fcmToken).where(Users.userId == user_id).one_or_none()
    session.close()
    return token


def need_message_in_fmc_receivers(new_user: Users = None) -> dict[Users, Sequence[Lectures]]:
    """

    :return:
    """
    session: Session = DbConnection().get_session()
    if new_user is None:
        stmt = select(Users).where(Users.wantFcmMessage is True)
        receivers: Sequence[Users] = session.scalars(stmt).all()
    else:
        receivers: Sequence[Users] = [new_user]

    need_message_today: dict = dict()

    now: datetime = datetime.now()
    today: str = f"{now.year}-{now.month}-{now.day}"
    for receiver in receivers:
        applied_id_stmt = select(Applied.appliedLectureId).where(Applied.appliedUserId == receiver.userId)
        applied_ids = session.scalars(applied_id_stmt).all()
        lecture_stmt: str = f"SELECT * FROM (SELECT * FROM lectures\
         WHERE lectureHeldDates LIKE '%{today}%') AS Lectures WHERE\
         Lectures.lectureId IN ({','.join(applied_ids)});"
        need_message_today[receiver] = session.scalars(text(lecture_stmt)).all()
    session.close()
    return need_message_today


