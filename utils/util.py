from hashlib import sha256
import json
import re
import datetime


def validate_string(string: str) -> bool:
    """
    문자열이 유효한지 검증
    :param string: 검증이 필요한 문자열
    :return: 유효성 여부
    """
    return string is not None and string != "null" and len(string) > 0


def validate_password(password: str, db_password: str) -> bool:
    """

    :param password: 사용자가 입력한 password
    :param db_password:
    :return:
    """
    sha_password: str = sha256(password.encode()).hexdigest()
    return sha_password == db_password


def json_data(path: str, how: str):
    with open(path, how, encoding='utf-8-sig') as j:
        data = json.load(j)
    return data


def add_json_data(path: str, how: str, value: any):
    with open(path, how, encoding='utf-8-sig') as J:
        json.dump(value, J, ensure_ascii=False, indent=4)


def adjust_white_space(string: str) -> str:
    adjust_string: str = re.sub(r"\s+", "", string)
    return adjust_string


def current_time(when, change):
    """
    현재 혹은 조정된 시간을 반환.
    :param when: y | m | d
    :param change: +- 숫자
    :return: 날짜
    """
    now: datetime = datetime.datetime.now()
    year: int = now.year
    month: int = now.month
    day: int = now.day
    if when == "d":
        day = day + change
    elif when == "y":
        year = year + change
    elif when == "m":
        month = month + change
    else:
        pass
    return f"{year}-{month}-{day}"


def trim_lecture_time(time_str: str, split: str | None) -> str | dict:
    if split is None:
        lecture_time = re.search(r"[0-9]{2,4}[-~.\s][0-9]{2}[-~.\s][0-9]{2}[-~.\s]", time_str)
        if lecture_time is None:
            return time_str
        return lecture_time.group()

    start_end: list[str] = time_str.split(split)
    return {
        "start": re.sub(r"\s*[0-9]{2}\s?:\s?[0-9]{2}", "", start_end[0]).strip(),
        "end": re.sub(r"\s*[0-9]{2}\s?:\s?[0-9]{2}", "", start_end[1]).strip()
    }


def trim_lecture_price(price_str: str) -> int:
    if not validate_string(price_str):
        return 0
    price_exist = re.search(r"[0-9,]+", price_str)
    print(price_exist)
    if price_exist is None:
        return 0
    return int(price_exist.group().replace(",", ""))
