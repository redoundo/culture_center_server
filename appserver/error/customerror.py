from http import HTTPStatus
from werkzeug.exceptions import HTTPException, default_exceptions, _aborter

from flask import jsonify, Flask
import enum


class ErrorCode(Exception, enum.Enum):
    """
    사용자 정의 예외 믹스인 클래스.
    """
    def __init__(self, error_name: str, status: HTTPStatus, message: str):
        self.errorName = error_name
        self.status = status
        self.message = message
        return

    @classmethod
    def error_code_names(cls) -> list[str]:
        return [name for name, member in cls.__members__.items()]

    @classmethod
    def get_error_code_by_name(cls, error: str):
        return [member for name, member in cls.__members__.items() if name is error][0]


class CustomException(ErrorCode):
    """
    사용자 예외 클래스 구현
    """
    NEED_LOGIN_EXCEPTION = ("NEED_LOGIN_EXCEPTION", HTTPStatus.FORBIDDEN, "기능을 사용하기 위해서는 로그인이 필요 합니다.")
    NEED_SIGN_IN_EXCEPTION = ("NEED_SIGN_IN_EXCEPTION", HTTPStatus.FORBIDDEN, "회원 가입이 필요 합니다.")
    WITHDRAW_FAIL_EXCEPTION = ("WITHDRAW_FAIL_EXCEPTION", HTTPStatus.FORBIDDEN, "회원 탈퇴에 실패 하였습니다. 다시 시도해 주세요.")
    INVALID_JWT_TOKEN_EXCEPTION = ("INVALID_JWT_TOKEN_EXCEPTION", HTTPStatus.BAD_REQUEST, "유효 하지 않은 jwt 토큰 입니다.")
    INVALID_JWT_SIGNATURE_EXCEPTION = ("INVALID_JWT_SIGNATURE_EXCEPTION", HTTPStatus.BAD_REQUEST,
                                       "토큰이 유효 하지 않습니다. 관리자에게 문의 하세요.")
    FAILED_AUTHORIZED_EXCEPTION = ("FAILED_AUTHORIZED_EXCEPTION", HTTPStatus.BAD_REQUEST, "로그인에 실패 하였습니다.")
    EXPIRED_TOKEN_EXCEPTION = ("EXPIRED_TOKEN_EXCEPTION", HTTPStatus.BAD_REQUEST, "jwt 토큰이 만료 되었습니다.")
    NO_REQUIRED_ARGUMENTS_EXCEPTION = ("NO_REQUIRED_ARGUMENTS_EXCEPTION", HTTPStatus.BAD_REQUEST,
                                       "진행에 필요한 내용이 존재 하지 않습니다. 확인 후 다시 시도 해주세요.")


def global_error_handler(app: Flask):
    """
    flask application 에 사용자 정의된 예외를 포함한 httpException 을 다룰 수 있는 처리자를 미리 등록 해놓음.
    :param app: flask application
    :return: app
    """
    def error_handler(error):
        if isinstance(error, CustomException):
            res: dict = {
                "errorName": error.errorName,
                "status": error.status,
                "message": error.message
            }
        elif isinstance(error, HTTPException):
            res: dict = {
                "errorName": error.name,
                "status": error.code,
                "message": error.description
            }
        else:
            # TODO: 400 으로만 할건지 좀 모호하다.
            message = _aborter.mapping[400].description
            res: dict = {
                "errorName": "ELSE_ERROR",
                "status": 400,
                "message": message
            }
        response = jsonify(res)
        response.status_code = res["status"]
        return response

    for http in list(default_exceptions.values()):
        app.register_error_handler(http, error_handler)
    app.register_error_handler(CustomException, error_handler)
    return app

