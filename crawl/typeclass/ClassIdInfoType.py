from .CenterInfoNoLink import CenterInfoNoLink
from .CenterInfoWithLink import CenterInfoWithLink
from .LectureType import LectureType
import re
import enum


class ClassIdInfos(enum.Enum):
    # homeplus lecture id = 9166318 = https://mschool.homeplus.co.kr/Lecture/Detail?LectureMasterID=9166318
    HOMEPLUS = ("HOMEPLUS", "대형마트", "=")
    # emart lecture id = 301BU8XTz2024S1974 = https://www.cultureclub.emart.com/class/301BU8XTz2024S1974
    EMART = ("EMART", "대형마트", "/")
    # lottemart lecture id = cls_cd=20240132211400
    LOTTEMART = ("LOTTEMART", "대형마트", "cls_cd=[0-9]+")

    # lecture id = crsSqNo=25262 = ?stCd=450&sqCd=055&crsSqNo=25262&crsCd=102010&proCustNo=P00176746&ctGubn=
    HYUNDAI = ("HYUNDAI", "백화점", "crsSqNo=[0-9]+")
    # akplaza lecture id = sSubject_cd=813006 = https://culture.akplaza.com/course/detail?store=03&sSubject_cd=813006&expired=F
    AKPLAZA = ("AKPLAZA", "백화점", "sSubject_cd=[0-9]+")
    # lecture id = lectCd=0179 = /application/search/view.do?brchCd=0335&yy=2024&lectSmsterCd=1&lectCd=0179
    LOTTE = ("LOTTE", "백화점", "lectCd=[0-9]+")
    # lecture id = 1251345530 = https://dept.galleria.co.kr/g-culture/culture-center/branch/timeworld/1251345530
    GALLERIA = ("GALLERIA", "백화점", "/")

    def __init__(self, center: str, types: str, regex: str):
        self.center: str = center
        self.types: str = types
        self.regex: str = regex
        return

    @classmethod
    def get_type_by_center_name(cls, center: str):
        return [member.types for name, member in cls.__members__.items() if name == center][0]

    @classmethod
    def get_center_by_type(cls, types: str) -> list[str]:
        """
        타입에 해당하는 센터들의 이름 전체 반환.
        :param types: 대형마트 || 백화점 || 공공기관 || 기타
        :return:
        """
        return [name for name, member in cls.__members__.items() if member.types == types]

    @classmethod
    def make_class_id(cls, lecture: LectureType) -> str:
        """
        classId 형식 = 대형마트(types)_AKPLAZA(center)_광명(region)_땡땡점(branch)_00000~(lecture id)
        :param lecture: 크롤링한 강의 내용
        :return: lecture 에 저장할 classId
        """
        center_name: str = lecture.center
        regex: str = [member.regex for name, member in cls.__members__.items() if name == center_name][0]
        center_id_list: list[str] = [lecture.type, center_name, lecture.region, lecture.branch]
        if regex in ["/", "="]:
            lecture_id: str = lecture.url.split(regex)[-1]
            center_id_list.append(lecture_id)
        else:
            lecture_id: str = re.search(regex, lecture.url).group().replace(regex, "")
            center_id_list.append(lecture_id)

        return "_".join(center_id_list)

    @classmethod
    def make_class_id_before_crawl(cls, info: CenterInfoNoLink | CenterInfoWithLink, url: str) -> str:
        center_name: str = info.get_center_name()
        regex: str = [member.regex for name, member in cls.__members__.items() if name == center_name][0]
        center_type: str = [member.types for name, member in cls.__members__.items() if name == center_name][0]
        center_id_list: list[str] = [center_type, center_name, info.get_region(), info.get_branch()]
        if regex in ["/", "="]:
            center_id_list.append(url.split(regex)[-1])
        else:
            center_id_list.append(re.search(regex, url).group().replace(regex, ""))
        return "_".join(center_id_list)

