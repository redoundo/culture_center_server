import re
from datetime import datetime


def validate_string(string: str) -> bool:
    """
    문자열이 유효한지 검증
    :param string: 검증이 필요한 문자열
    :return: 유효성 여부
    """
    return string is not None and string != "null" and len(string) > 0


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


def trim_lecture_span_str(spans: str) -> tuple:
    lecture_spans: list[str] = re.findall(r"[0-9]{4}\s?[/.-]\s?[0-9]{2}\s?[/.-]\s?[0-9]{2}", spans)
    return lecture_spans[0], lecture_spans[1]


def trim_lecture_price(price_str: str) -> int:
    if not validate_string(price_str):
        return 0
    price_exist = re.search(r"[0-9,]+", price_str)
    print(price_exist)
    if price_exist is None:
        return 0
    return int(price_exist.group().replace(",", ""))


def weekday_from_date_str(date_str: str, trim: bool = False) -> str:
    if trim:
        weekday: int = datetime.strptime(date_str, "%Y-%m-%d").weekday()
    else:
        date: str = re.findall(r"[0-9]{4}\s?[/.-]\s?[0-9]{2}\s?[/.-]\s?[0-9]{2}", date_str)[0].replace(".", "-")
        date_trim: str = re.sub(r"[/.]", "-", date)
        weekday: int = datetime.strptime(date_trim, "%Y-%m-%d").weekday()

    if weekday == 0:
        return "월"
    elif weekday == 1:
        return "화"
    elif weekday == 2:
        return "수"
    elif weekday == 3:
        return "목"
    elif weekday == 4:
        return "금"
    elif weekday == 5:
        return "토"
    else:
        return "일"


