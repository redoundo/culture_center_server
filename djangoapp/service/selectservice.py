from ..models import *
from django.db.models import Q
from django.utils.timezone import now


def validate_string(string: str) -> bool:
    """
    문자열이 유효한지 검증
    :param string: 검증이 필요한 문자열
    :return: 유효성 여부
    """
    return string is not None and string != "null" and len(string) > 0


def select_users_info_by_user_id(user_id: int) -> dict | None:
    """
    사용자 아이디 로 사용자 정보와 좋아요 누른 강좌  및 신청한 강좌 전부 반환.
    :param user_id: 사용자 아이디
    :return: 사용자 및 관련 정보 일체 반환.
    """
    a_result = Users.objects.get(userid=user_id)
    
    if a_result is None:
        return a_result
    result_id: int = a_result.userid 
    applied_result = select_all_applied_lectures_by_user_id(user_id=result_id)
    liked_result = select_all_liked_lectures_by_user_id(user_id=result_id)
    return {
        "user": a_result.dictionary(),
        "applied": applied_result,
        "liked": liked_result
    }


def select_user_by_user_id(user_id: int) -> Users:
    """
    사용자 아이디로 사용자 찾기
    :param user_id: 사용자 아이디
    :return: 사용자 정보
    """
    return Users.objects.get(userid=user_id)


def select_user_by_email(email: str) -> Users:
    """
    이메일로 사용자 찾기
    :param email: 사용자 이메일
    :return: 사용자 정보
    """
    return Users.objects.get(email=email)


def check_user_nickname_is_unique(nickname: str) -> bool:
    """
    사용자가 입력한 닉네임을 사용할 수 있는지 확인하기 위해 해당 닉네임과 동일한 닉네임의 수가 얼마나 되는지 확인.
    :param nickname: 저장하고 싶은 닉네임.
    :return: 사용 가능 여부
    """
    uniqueness = Users.objects.filter(nickname=nickname)
    return uniqueness.count() == 0


def check_user_already_exists(email: str) -> bool:
    """
    해당 이메일로 가입한 적이 있는지 확인.
    :param email: 사용자의 이메일
    :return: 존재 여부
    """
    exist = Users.objects.filter(email=email)
    return exist.count() >= 1


def select_all_applied_lectures_by_user_id(user_id: int) -> list[dict]:
    """
    사용자가 신청한 강좌의 내용들을 가져온다.
    :param user_id: 사용자 아이디
    :return: 강좌 내용
    """
    applied = Applied.objects.filter(applieduserid=user_id)
    lecture_id: list[int] = [apply.appliedlectureid for apply in applied]

    lectures: list[dict] = []
    for lecture in lecture_id:
        lecture: Lectures = Lectures.objects.get(lectureid=lecture)
        lectures.append(lecture.dictionary())

    return lectures


def select_all_liked_lectures_by_user_id(user_id: int) -> list[dict]:
    """
    사용자가 좋아요 한 강좌 내용.
    :param user_id: 사용자 아이디
    :return: 좋아요 한 강좌 내용
    """
    liked = Liked.objects.filter(likeduserid=user_id) 
    lecture_id: list[int] = [like.likedlectureid for like in liked]
    
    lectures: list[dict] = []
    for lecture in lecture_id:
        lecture_content: Lectures = Lectures.objects.get(lectureid=lecture)
        lectures.append(lecture_content.dictionary())

    return lectures


def select_all_categories() -> list[dict]:
    """
    모든 카테고리 반환.
    :return:
    """
    categories = Categories.objects.all()
    return [category.dictionary() for category in categories]


def select_all_targets() -> list[dict]:
    """
    모든 대상 반환.
    :return:
    """
    targets = Targets.objects.all()
    return [target.dictionary() for target in targets]


def get_registered_fmc_token(user_id: int) -> str | None:
    """
    fcm 메시지를 보내기 위해서 사용자의 아이디로 존재 하는 토큰을 가져 온다.
    :param user_id: 사용자 아이디
    :return: fcm token | None
    """
    registered_user: Users = Users.objects.get(userid=user_id)
    if registered_user is None:
        return registered_user
    return registered_user.fcmtoken


def select_lecture_by_lecture_id(lecture_id: int) -> dict | None:
    """
    강좌 아이디로 강좌 내용을 찾아 반환
    :param lecture_id: 강좌 아이디
    :return: 강좌 내용 | None
    """
    a_lecture: Lectures = Lectures.objects.get(lectureid=lecture_id)
    if a_lecture is None:
        return a_lecture
    return a_lecture.dictionary()


def select_all_center_type() -> list[dict]:
    """
    모든 센터들의 타입 반환.
    :return: 센터 타입들
    """
    center_types = Centers.objects.all()
    return [center_type.dictionary() for center_type in center_types]


def select_centers_by_type(types: str) -> list[dict]:
    """
    센터 타입에 맞는 센터들을 반환.
    :param types: 센터 타입
    :return: 센터들
    """
    centers = Centers.objects.filter(centertype=types)
    return [center.dictionary() for center in centers]


def select_all_lectures_by_search_options(**kwargs) -> list[dict]:
    """
    검색 조건이 없으면 기본 값을 설정한 뒤 검색 결과를 반환한다.
    :param kwargs: 검색 조건들.
    :return: 검색 결과
    """
    page_num: str = kwargs.get("page")
    keyword: str = kwargs.get("keyword")
    center_type: str = kwargs.get("centerType")
    target: str = kwargs.get("target")
    category: str = kwargs.get("category")
    center_name: str = kwargs.get("centerName")

    and_dict: dict = dict()
    or_dict: dict = dict()
    
    if validate_string(target) and validate_string(category):
        and_dict[target] = category
    elif validate_string(category):
        or_dict["kid"] = category
        or_dict["adult"] = category
        or_dict["baby"] = category
    else:
        pass
    if validate_string(center_type):
        and_dict["centertype"] = center_type
    if validate_string(keyword):
        and_dict["title"] = f"%{keyword}%"
    if validate_string(center_name):
        and_dict["center"] = center_name
    
    limit: int = 0
    if page_num is not None and len(page_num) > 1 and page_num != "null":
        limit = int(page_num)
    else:
        pass

    if len(or_dict.keys()) > 2:
        lectures = Lectures.objects.filter(Q(kid=or_dict["kid"]) | Q(adult=or_dict["adult"]) | Q(child=or_dict["child"]), **and_dict)[limit * 16: (limit +1) * 16]
    elif len(or_dict.keys()) > 0:
        and_dict.update(or_dict)
        lectures = Lectures.objects.filter(**and_dict)[limit * 16: (limit + 1) * 16]
    else:
        lectures = Lectures.objects.filter(**and_dict)[limit * 16: (limit + 1) * 16]

    return [lecture.dictionary() for lecture in lectures]


def need_message_in_fmc_receivers(new_user: Users = None) -> dict[Users, list[Lectures]]:
    """
    오늘 알림 전송이 필요한 사용자 및 알림 대상 강좌 내용 반환.
    :return:
    """

    if new_user is None:
        receivers: list[Users] = [user for user in Users.objects.filter(wantfcmmessage=0)]
    else:
        receivers: list[Users] = [new_user]
    
    today: str = f"{now().year}-{now().month}-{now().day}"
    need_message_today: dict = dict()

    for receiver in receivers:
        lecture_ids: list[int] = [applied.appliedlectureid for applied in Applied.objects.filter(applieduserid=receiver.userid)]
        lectures: list[Lectures] = [lecture for lecture in Lectures.objects.filter(lectureid__in=lecture_ids, lecturehelddates=f"%{today}%")]
        need_message_today[receiver] = lectures

    return need_message_today

