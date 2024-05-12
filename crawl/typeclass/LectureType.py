import json
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import *


class LectureType(object):
    classId: str
    type: str
    center: str
    region: str
    branch: str
    address: str
    target: str
    category: str
    url: str
    src: str
    title: str
    price: int
    content: str
    curriculum: str
    lectureSupplies: str
    lectureStart: str
    lectureEnd: str
    enrollStart: str
    enrollEnd: str
    crawlerIndex: str
    lectureHeldDates: str

    def __init__(self) -> None:
        self.curriculum = 'NULL'.replace("'", "''")
        self.lectureSupplies = 'NULL'.replace("'", "''")
        self.enrollStart = 'NULL'.replace("'", "''")
        self.enrollEnd = 'NULL'.replace("'", "''")
        self.crawlerIndex = 'NULL'.replace("'", "''")
        self.classId = 'NULL'.replace("'", "''")
        self.price = -1
        self.url = 'NULL'.replace("'", "''")
        self.title = 'NULL'.replace("'", "''")
        self.content = 'NULL'.replace("'", "''")
        self.target = 'NULL'.replace("'", "''")
        self.src = 'NULL'.replace("'", "''")
        self.center = 'NULL'.replace("'", "''")
        self.region = 'NULL'.replace("'", "''")
        self.lectureStart = 'NULL'.replace("'", "''")
        self.lectureEnd = 'NULL'.replace("'", "''")
        self.address = 'NULL'.replace("'", "''")
        self.branch = 'NULL'.replace("'", "''")
        self.type = 'NULL'.replace("'", "''")
        self.lectureHeldDates = 'NULL'.replace("'", "''")
        return

    def set_curriculum(self, curriculum: dict):
        self.curriculum = json.dumps(curriculum, ensure_ascii=False)
        return

    def set_lecture_held_dates(self, lecture_start_end: list[str], detail: str, count_by_week: int):
        self.lectureStart = lecture_start_end[0]
        self.lectureEnd = lecture_start_end[1]
        lecture_day = re.findall(r"[월화수목금토일]", detail)
        if lecture_day is None or len(lecture_day) < 1:
            print(f"lecture_held_dates 를 계산 하지 못했습니다!! {detail}")
            return
        start_date_datetime: datetime = datetime.strptime(self.lectureStart, "%Y-%m-%d")
        lecture_dates: list[str] = []
        lecture_in_week = count_by_week // len(lecture_day)
        for day in lecture_day:
            if day == "월":
                next_monday = start_date_datetime + relativedelta(weekday=MO)
                lecture_dates.append(next_monday.strftime("%Y-%m-%d"))
                for num in range(1, lecture_in_week):
                    next_next_monday = next_monday + relativedelta(weeks=num)
                    lecture_dates.append(next_next_monday.strftime("%Y-%m-%d"))
            elif day == "화":
                next_tuesday = start_date_datetime + relativedelta(weekday=TU)
                lecture_dates.append(next_tuesday.strftime("%Y-%m-%d"))
                for num in range(1, lecture_in_week):
                    next_next_tuesday = next_tuesday + relativedelta(weeks=num)
                    lecture_dates.append(next_next_tuesday.strftime("%Y-%m-%d"))
            elif day == "수":
                next_wednesday = start_date_datetime + relativedelta(weekday=WE)
                lecture_dates.append(next_wednesday.strftime("%Y-%m-%d"))
                for num in range(1, lecture_in_week):
                    next_next_wednesday = next_wednesday + relativedelta(weeks=num)
                    lecture_dates.append(next_next_wednesday.strftime("%Y-%m-%d"))
            elif day == "목":
                next_thursday = start_date_datetime + relativedelta(weekday=TH)
                lecture_dates.append(next_thursday.strftime("%Y-%m-%d"))
                for num in range(1, lecture_in_week):
                    next_next_thursday = next_thursday + relativedelta(weeks=num)
                    lecture_dates.append(next_next_thursday.strftime("%Y-%m-%d"))
            elif day == "금":
                next_friday = start_date_datetime + relativedelta(weekday=FR)
                lecture_dates.append(next_friday.strftime("%Y-%m-%d"))
                for num in range(1, lecture_in_week):
                    next_next_friday = next_friday + relativedelta(weeks=num)
                    lecture_dates.append(next_next_friday.strftime("%Y-%m-%d"))
            elif day == "토":
                next_saturday = start_date_datetime + relativedelta(weekday=SA)
                lecture_dates.append(next_saturday.strftime("%Y-%m-%d"))
                for num in range(1, lecture_in_week):
                    next_next_saturday = next_saturday + relativedelta(weeks=num)
                    lecture_dates.append(next_next_saturday.strftime("%Y-%m-%d"))
            else:
                next_sunday = start_date_datetime + relativedelta(weekday=SU)
                lecture_dates.append(next_sunday.strftime("%Y-%m-%d"))
                for num in range(1, lecture_in_week):
                    next_next_sunday = next_sunday + relativedelta(weeks=num)
                    lecture_dates.append(next_next_sunday.strftime("%Y-%m-%d"))

        self.lectureHeldDates = "!".join(lecture_dates)
        return
