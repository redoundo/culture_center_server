from django.shortcuts import render
from django.http.request import HttpRequest
import json
import requests
from rest_framework import status
from django.utils.timezone import now
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import *
from .serializers import *
import os
from .customerror import CustomException
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from .service.changeservice import *
from .service.selectservice import *
import hashlib
from .authentication import is_authenticated, jwt_token_authenticate
from .jwtprovider import *


def validate_string(string: str) -> bool:
    """
    문자열이 유효한지 검증
    :param string: 검증이 필요한 문자열
    :return: 유효성 여부
    """
    return string is not None and string != "null" and len(string) > 0


@api_view(["GET"])
def find_lectures_by_search_options(request: HttpRequest):
    """
    검색 조건 설정에 필요한 내용과 전달된 조건으로 찾은 강좌를 반환 한다.
    :return:
    """
    token: str = request.headers.get("Authorization")
    print(token)
    lectures: list[dict] = select_all_lectures_by_search_options(page=request.GET.get("page", None),
                                                                 target=request.GET.get("targetId", None),
                                                                 category=request.GET.get("categoryId", None),
                                                                 keyword=request.GET.get("keyword", None),
                                                                 centerType=request.GET.get("type", None),
                                                                 centerName=request.GET.get("center", None))
    if token is not None:
        # todo: 전역 처리 설정 안함. 그래서 user_id 확인에 들어가지 않았음.
        user_id = decode_jwt(token).get("userId")
        print(user_id)
        liked_applied: dict = {"liked": select_all_liked_lectures_by_user_id(int(user_id)),
                               "applied": select_all_applied_lectures_by_user_id(int(user_id))}
    else:
        liked_applied = None

    targets: list[dict] = select_all_targets()
    categories: list[dict] = select_all_categories()
    center_types: list[dict] = select_all_center_type()
    print(targets)
    return JsonResponse({
        'lectures': lectures, 'targets': targets, 'categories': categories, 'type': center_types,
        "liked_applied": liked_applied
    })


@api_view(["GET"])
def find_lecture_by_lecture_id(request: HttpRequest):
    """
    강좌 아이디로 강좌 내용을 찾아 반환.
    :return:
    """
    lecture_id = request.GET.get("lectureId", None)
    if validate_string(lecture_id):
        lecture: dict | None = select_lecture_by_lecture_id(int(lecture_id))
        if lecture is not None:
            return JsonResponse({
                'lecture': lecture
            })
    return JsonResponse({'lecture': None})


@api_view(["GET"])
@jwt_token_authenticate
@is_authenticated
def set_liked_this_lecture_by_lecture_id(request: HttpRequest, user: dict):
    """
    강좌 저장.
    :return:
    """
    lecture_id = request.GET.get("lectureId", None)

    if validate_string(lecture_id):
        insert_liked_by_user_id(lecture_id=int(lecture_id), user_id=int(user.get("userId")))
    else:
        raise CustomException.NO_REQUIRED_ARGUMENTS_EXCEPTION
    return JsonResponse({'status': 200})


@api_view(["GET"])
def set_applied_this_lecture_by_lecture_id(request: HttpRequest):
    """
    토큰이 없어도 아무런 alert 발생 하지 않고 있으면 해당 사용자 아이디로 지원한 강좌 저장
    :return:
    """
    lecture_id = request.GET.get("lectureId", None)
    token = request.headers.get("Authorization")

    if not validate_string(token):
        raise CustomException.NEED_LOGIN_EXCEPTION

    if validate_string(lecture_id):
        user_id = decode_jwt(token).get("userId")
        insert_applied_by_user_id(lecture_id=int(lecture_id), user_id=int(user_id))
    else:
        raise CustomException.NO_REQUIRED_ARGUMENTS_EXCEPTION
    return JsonResponse({'status': 200})


@api_view(["GET"])
@jwt_token_authenticate
@is_authenticated
def find_user_by_user_id(request: HttpRequest, user: dict):
    """
    jwt 토큰을 통해 사용자 아이디를 가져온 뒤, 해당 아이디로 저장된 내용들을 전부 가져온다.
    :return:
    """
    result = select_users_info_by_user_id(int(user.get("userId")))
    print(user)
    if user is None:
        print("user is None")
        return JsonResponse(data={"user": None}, status=status.HTTP_400_BAD_REQUEST)
    print("user is not None")
    return JsonResponse(data={"user": result}, status=status.HTTP_200_OK)


@api_view(["GET"])
@jwt_token_authenticate
@is_authenticated
def my_page_delete_liked_or_applied_by_lecture_id(request: HttpRequest, user: dict, applied_liked: str):
    """
    저장 했거나 지원 했던 강좌 삭제
    :param user: is_authenticated 에서 가져온 현재 사용자 정보
    :param applied_liked: applied | liked
    :return:
    """
    lecture_id = request.GET.get("lectureId", None)
    if not validate_string(lecture_id):
        raise CustomException.NO_REQUIRED_ARGUMENTS_EXCEPTION

    if applied_liked == "liked":
        delete_liked_by_lecture_id_user_id(lecture_id=int(lecture_id), user_id=int(user.get("userId")))
    else:
        delete_applied_by_lecture_id_user_id(lecture_id=int(lecture_id), user_id=int(user.get("userId")))

    return JsonResponse(data={"status": 200})


@api_view(["GET"])
def find_user_info_for_edit_info(request: HttpRequest):
    """
    정보 변경을 위해 토큰에서 사용자 아이디를 받아온 뒤 사용자 정보를 가져온다.
    :param: user: 현재 사용자 정보
    :return: 사용자 정보
    """
    token = request.headers.get("Authorization")
    if not validate_string(token):
        raise CustomException.NEED_LOGIN_EXCEPTION
    user_id = decode_jwt(token).get("userId")
    if user_id is None:
        raise CustomException.INVALID_JWT_TOKEN_EXCEPTION
    user: Users = select_user_by_user_id(int(user_id))

    return JsonResponse({"user": user})


@api_view(["POST"])
@jwt_token_authenticate
@is_authenticated
def update_user_info(request: HttpRequest, user: dict):
    """
    사용자 정보 업데이트
    :return:
    """
    post: dict = json.loads(request.body)
    nickname: str = post.get("nickname")
    if not validate_string(nickname):
        raise CustomException.NO_REQUIRED_ARGUMENTS_EXCEPTION
    update_user_by_user_id(int(user.get("userId")), nickname)
    return JsonResponse({"status": 200})


@api_view(["GET"])
@jwt_token_authenticate
@is_authenticated
def let_withdraw_user_by_user_id(request: HttpRequest, user: dict):
    """
    회원 탈퇴
    :return:
    """
    try:
        withdraw_user_by_user_id(int(user.get("userId")))
    except Exception as e:
        print(e.args)
        raise CustomException.WITHDRAW_FAIL_EXCEPTION
    return JsonResponse({"status": 200})


@api_view(["POST"])
def sns_access_token(request: HttpRequest, sns: str):
    """
    code 를 받은 뒤에 access token 반환.
    :param sns: google | naver | culturecenter
    :return:
    """
    post: dict = json.loads(request.body)
    query = post.get("query")
    if sns == "naver":
        publish_url: str = "https://nid.naver.com/oauth2.0/token"
        response = requests.get(publish_url + "?" + query)
    else:
        publish_url: str = "https://oauth2.googleapis.com/token"
        response = requests.post(publish_url, query)
    res = response.json()
    print(res)
    return JsonResponse(res)


@api_view(["POST"])
def naver_get_user_info(request: HttpRequest):
    """
    네이버 sns 로그인 시, access token 을 사용해  사용자 정보 반환.
    :return:
    """
    url: str = "https://openapi.naver.com/v1/nid/me"
    post: dict = json.loads(request.body)
    print(post)
    response = requests.get(url=url, headers={"Authorization": "Bearer " + post.get("Authorization")})
    res = response.json()
    print(res)
    return JsonResponse(res)


@api_view(["POST"])
def sign_in_publish_jwt(request: HttpRequest, sns: str):
    """
    자체 jwt 토큰 발급
    :param sns: culturecenter | naver | google
    :return: jwt 토큰들
    """
    post: dict = json.loads(request.body)
    if post.get("email") is None and post.get("id") is None:
        raise CustomException.FAILED_AUTHORIZED_EXCEPTION
    exist: int = check_user_already_exists(post.get("email"))
    if exist > 0:
        user: Users = select_user_by_email(post.get("email"))
        print(user.userid)
        print(encode_jwt(user.userid))
        return JsonResponse({"status": 200, "Authentication": encode_jwt(user.userid)})

    if sns == "CultureCenter":
        provider_id: str = (sns.upper() + "_" + str(now().year) + str(now().month) + str(now().day) + "_"
                            + post.get("id"))
        if post.get("nickname") is None:
            nickname: str = post.get("id")[:5]
        else:
            nickname: str = post.get("nickname")

        encrypt = hashlib.sha256()
        encrypt.update(post.get("password").encode('utf-8'))
        # todo: 기본 로그인에는 email 을 사용하지 않을 텐데? 이거 다시 확인 필요.
        sign_in_user(post.get("email"), encrypt.hexdigest(), nickname, sns, provider_id)
    else:
        provider_id: str = sns.upper() + "_" + post.get("id")
        nickname: str = post.get("email")

        print(nickname)
        sign_in_user(post.get("email"), provider_id, nickname, sns, provider_id)

    new_user: Users = select_user_by_email(post.get("email"))
    print(new_user.userid)
    return JsonResponse({"status": 200, "Authentication": encode_jwt(new_user.userid)})


@api_view(["POST"])
def login_publish_jwt(request: HttpRequest, sns: str):
    """
    자체 로그인 jwt 토큰 발급
    :param sns: culturecenter | naver | google
    :return: jwt 토큰들
    """
    post: dict = json.loads(request.body)
    if post.get("email") is None and post.get("id") is None:
        raise CustomException.FAILED_AUTHORIZED_EXCEPTION

    user: Users = select_user_by_email(post.get("email"))
    if user is None:
        return JsonResponse({'status': 404})

    if sns == "CultureCenters":
        encrypt = hashlib.sha256()
        encrypt.update(post.get("password").encode('utf-8'))
        if user.password != encrypt.hexdigest():
            return JsonResponse({'status': 401})

    jwt_token: str = encode_jwt(user.userid)
    return JsonResponse({"status": 200, "Authentication": jwt_token})


@api_view(["GET"])
def is_logged_in(request: HttpRequest):
    """
    jwt 토큰 유효성 확인을 통해 사용자가 로그인 되어져 있는 상태인지 여부 반환.
    :return: userId | -1
    """
    token = request.headers.get("Authorization")
    print(list(request.headers.keys()))
    if not validate_string(token):
        raise CustomException.NEED_LOGIN_EXCEPTION
    user_id = decode_jwt(token).get("userId")
    if user_id is None:
        raise CustomException.INVALID_JWT_TOKEN_EXCEPTION
    print(user_id)
    user: Users = select_user_by_user_id(user_id)
    if user is not None and user.userid is not None:
        return JsonResponse({"status": 200, "userId": user.userid})
    else:
        return JsonResponse({"status": 400, "userId": -1})


@api_view(["POST"])
def nickname_uniqueness(request: HttpRequest):
    """
    닉네입 사용 가능 여부 확인
    :return:
    """
    post: dict = json.loads(request.body)
    if post.get("nickname") is None:
        raise CustomException.FAILED_AUTHORIZED_EXCEPTION
    exist: int = check_user_nickname_is_unique(post.get("nickname"))
    if exist > 0:
        return JsonResponse({"status": 226, "canUse": False})
    return JsonResponse({"status": 200, "canUse": True})


@api_view(["POST"])
@jwt_token_authenticate
@is_authenticated
def registering_fcm_receiver(request: HttpRequest, user: dict):
    """
    fcm 전송 요청자 등록
    :return:
    """
    post: dict = json.loads(request.body)
    if post.get("vapidToken") is None:
        return JsonResponse({"status": 400, "registered": False})
    register_fcm_receiver(user.get("userId"), post.get("vapidToken"))
    return JsonResponse({"status": 200, "registered": True})


@api_view(["GET"])
def download_new_data(request: HttpRequest):
    """
    크롤링 완료 후, 새로운 라벨링 파일이 생성 되면 endpoint 로 사용.
    :return:
    """
    file_name: str = "train_sample.json"
    file_path: str = "/flask-server/sample/train_sample.json"
    if os.path.exists(file_path) and os.path.isfile(file_path):
        fs = FileSystemStorage(file_path)
        response = FileResponse(fs.open(file_path, "rb"))
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
    return JsonResponse({"status": 404, "message": "no such file."})


