import re


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


def trim_lecture_price(price_str: str) -> int:
    if not validate_string(price_str):
        return 0
    price_exist = re.search(r"[0-9,]+", price_str)
    print(price_exist)
    if price_exist is None:
        return 0
    return int(price_exist.group().replace(",", ""))
