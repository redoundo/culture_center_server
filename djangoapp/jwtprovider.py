from dotenv import load_dotenv
import datetime
from datetime import timedelta
import jwt
from .customerror import CustomException
import os
load_dotenv()


def encode_jwt(user_id: int) -> str:
    """
    userId로 jwt 토큰 발행.
    :param user_id: auto_increase 된 사용자 아이디
    :return:
    """
    encoded: str = jwt.encode({"userId": user_id, 'exp': datetime.datetime.now(datetime.UTC) + timedelta(days=3)},
                              key=os.getenv("JWT_SECRET"),
                              algorithm=os.getenv("JWT_ALGORITHM")
                              )
    return encoded


def decode_jwt(token: str) -> dict:
    """
    jwt 토큰을 받아 디코딩 하는데 토큰 만료, 유효하지 않은 토큰 등등의 문제가 없다면 userId 를 반환할 것이다.
    :param token: jwt 토큰
    :return: {'userId': userId(int)} | exception
    """
    try:
        decoded = jwt.decode(token,
                             key=os.getenv("JWT_SECRET"),
                             algorithms=[os.getenv("JWT_ALGORITHM")]
                             )
    except jwt.ExpiredSignatureError:
        raise CustomException.EXPIRED_TOKEN_EXCEPTION
    except jwt.InvalidSignatureError:
        raise CustomException.INVALID_JWT_SIGNATURE_EXCEPTION
    except jwt.InvalidTokenError:
        raise CustomException.INVALID_JWT_TOKEN_EXCEPTION
    return decoded
