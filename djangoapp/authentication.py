from django.http.request import HttpRequest
from rest_framework.request import Request
from .jwtprovider import *
from .customerror import CustomException
from .service.selectservice import select_user_by_user_id


def validate_string(string: str) -> bool:
    """
    문자열이 유효한지 검증
    :param string: 검증이 필요한 문자열
    :return: 유효성 여부
    """
    return string is not None and string != "null" and len(string) > 0


def jwt_token_authenticate(func):

    def api_function(request: HttpRequest, **arg):
        try:
            request.headers.get("Authorization")
        except Exception as e:
            raise CustomException.NEED_LOGIN_EXCEPTION

        token = request.headers.get("Authorization")
        if not validate_string(token):
            raise CustomException.NEED_LOGIN_EXCEPTION

        user_id: dict = decode_jwt(token)  # 정상적인 토큰이 아니라면 에러가 발생해 아래의 내용은 진행 되지 않음.
        print(arg, user_id)
        if arg is not None and len(list(arg.keys())) > 0:
            key: str = list(arg.keys())[0]
            print(key)
            key_dict: dict = {key: arg.get(key)}
            return func(request, user_id, **key_dict)
        else:
            return func(request, user_id)

    return api_function


def is_authenticated(func):

    def api_function(request: HttpRequest, user_id: dict, **arg):
        if user_id is None:
            raise CustomException.NEED_LOGIN_EXCEPTION

        entity = select_user_by_user_id(int(user_id.get("userId")))
        if entity is None:  # 토큰에서
            raise CustomException.NEED_SIGN_IN_EXCEPTION

        user: dict = entity.dictionary()
        print(arg, user)
        if arg is not None and len(list(arg.keys())) > 0:
            key: str = list(arg.keys())[0]
            print(key)
            key_dict: dict = {key: arg.get(key)}
            return func(request, user, **key_dict)
        else:
            return func(request, user)

    return api_function


