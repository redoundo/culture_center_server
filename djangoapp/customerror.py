from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import enum


class ErrorCode(Exception, enum.Enum):
    """
    사용자 정의 예외 믹스인 클래스.
    """
    def __init__(self, error_name: str, status: status, message: str):
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
    NEED_LOGIN_EXCEPTION = ("NEED_LOGIN_EXCEPTION", status.HTTP_403_FORBIDDEN, "기능을 사용하기 위해서는 로그인이 필요 합니다.")
    NEED_SIGN_IN_EXCEPTION = ("NEED_SIGN_IN_EXCEPTION", status.HTTP_403_FORBIDDEN, "회원 가입이 필요 합니다.")
    WITHDRAW_FAIL_EXCEPTION = ("WITHDRAW_FAIL_EXCEPTION", status.HTTP_403_FORBIDDEN, "회원 탈퇴에 실패 하였습니다. 다시 시도해 주세요.")
    INVALID_JWT_TOKEN_EXCEPTION = ("INVALID_JWT_TOKEN_EXCEPTION", status.HTTP_400_BAD_REQUEST, "유효 하지 않은 jwt 토큰 입니다.")
    INVALID_JWT_SIGNATURE_EXCEPTION = ("INVALID_JWT_SIGNATURE_EXCEPTION", status.HTTP_400_BAD_REQUEST,
                                       "토큰이 유효 하지 않습니다. 관리자에게 문의 하세요.")
    FAILED_AUTHORIZED_EXCEPTION = ("FAILED_AUTHORIZED_EXCEPTION", status.HTTP_400_BAD_REQUEST, "로그인에 실패 하였습니다.")
    EXPIRED_TOKEN_EXCEPTION = ("EXPIRED_TOKEN_EXCEPTION", status.HTTP_400_BAD_REQUEST, "jwt 토큰이 만료 되었습니다.")
    NO_REQUIRED_ARGUMENTS_EXCEPTION = ("NO_REQUIRED_ARGUMENTS_EXCEPTION", status.HTTP_400_BAD_REQUEST,
                                       "진행에 필요한 내용이 존재 하지 않습니다. 확인 후 다시 시도 해주세요.")


def custom_exception_handler(exc, context):
    # DRF의 기본 예외 처리 함수 호출
    response = exception_handler(exc, context)
    if isinstance(exec, CustomException) or isinstance(exec, ErrorCode):
        return JsonResponse({"status": exec.status, "errorMessage": exec.message, "errorCode": exec.errorName})
    return response
