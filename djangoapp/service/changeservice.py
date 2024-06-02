from ..models import *
from django.db import transaction


@transaction.atomic()
def delete_applied_by_lecture_id_user_id(lecture_id: int, user_id: int):
    """
    사용자 아이디를 가진 지원한 강좌 내역 삭제
    :param lecture_id: 강좌 아이디
    :param user_id: 사용자 아이디
    :return:
    """
    Applied.objects.filter(appliedlectureid=lecture_id, applieduserid=user_id).delete()
    return


@transaction.atomic()
def delete_liked_by_lecture_id_user_id(lecture_id: int, user_id: int):
    """
    사용자 아이디를 가진 찜한 강좌 내역 삭제
    :param lecture_id: 강좌 아이디
    :param user_id: 사용자 아이디
    :return: 
    """
    Liked.objects.filter(likedlectureid=lecture_id, likeduserid=user_id).delete()
    return


@transaction.atomic()
def delete_all_applied_by_user_id(user_id: int):
    """
    사용자 아이디를 가지고 있는 모든 지원한 강좌 내용을 삭제
    :param user_id: 사용자 아이디
    :return: 
    """
    Applied.objects.filter(applieduserid=user_id).delete()
    return


@transaction.atomic()
def delete_all_liked_by_user_id(user_id: int):
    """
    사용자 아이디를 가지고 있는 모든 찜한 강좌 내용을 삭제
    :param user_id: 사용자 아이디
    :return:
    """
    Liked.objects.filter(likeduserid=user_id).delete()
    return


@transaction.atomic()
def insert_applied_by_user_id(user_id: int, lecture_id: int):
    """
    지원한 강좌 내역 추가
    :param user_id: 
    :param lecture_id: 
    :return: 
    """
    exist = Applied.objects.filter(appliedlectureid=lecture_id).count() 
    
    if exist > 0:
        return
    Applied.objects.create(appliedlectureid=lecture_id, applieduserid=user_id)
    return


@transaction.atomic()
def insert_liked_by_user_id(user_id: int, lecture_id: int):
    """
    찜한 강좌 내역 추가
    :param user_id:
    :param lecture_id:
    :return:
    """
    exist = Liked.objects.filter(likedlectureid=lecture_id).count() 
    
    if exist > 0:
        return
    Liked.objects.create(likedlectureid=lecture_id, likeduserid=user_id)
    return


@transaction.atomic()
def withdraw_user_by_user_id(user_id: int):
    """
    회원 탈퇴
    :param user_id: 사용자 아이디
    :return: 
    """
    Users.objects.filter(userid=user_id).delete()
    return


@transaction.atomic()
def sign_in_user(email: str, password: str, nickname: str, provider: str, providers_id: str):
    """
    회원가입
    :param email: 이메일 
    :param password: 비밀번호
    :param nickname: 닉네임
    :param provider: sns 
    :param providers_id: sns에서 지급하는 고유 아이디
    :return: 
    """
    Users.objects.create(email=email, password=password, nickname=nickname, snsprovider=provider, snsproviderid=providers_id)
    return


@transaction.atomic()
def update_user_by_user_id(user_id: int, nickname: str):
    """
    사용자 정보 변경
    :param user_id: 사용자 아이디 
    :param nickname: 닉네임
    :return: 
    """
    Users.objects.filter(userid=user_id).update(nickname=nickname)
    return


@transaction.atomic()
def register_fcm_receiver(user_id: int, token: str):
    """
    fcm token 등록
    :param user_id: 사용자 아이디
    :param token: fcm token
    :return: 
    """
    Users.objects.filter(userid=user_id).update(fcmtoken=token)
    return
