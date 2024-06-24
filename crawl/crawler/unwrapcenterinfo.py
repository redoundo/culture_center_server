from typeclass.CenterInfoWithLink import CenterInfoWithLink
from typeclass.CenterInfoNoLink import CenterInfoNoLink
# from typeclass.CenterInfo import CenterInfo, CenterInfoWithLink


def validate_string(string: str) -> bool:
    """
    문자열이 유효한지 검증
    :param string: 검증이 필요한 문자열
    :return: 유효성 여부
    """
    return string is not None and string != "null" and len(string) > 0


def unwrap_with_link(data: dict, center: str) -> list[CenterInfoWithLink]:
    """
    json 파일 내용을 객체에 담아 반환한다. 모집중 조건도 전부 세팅되어 있는 링크이므로 바로 들어가서 크롤링을 하면 된다.
    :param center:
    :param data: 링크가 있는 센터의 정보를 담은 dict
    :return: 링크가 있는 센터의 정보를 담은 객체 리스트
    """
    unwrap_list: list[CenterInfoWithLink] = []
    region_list: list[str] = [region for region in list(data.keys())]
    with_link_index: int = 0

    for region in region_list:
        branch_list: list[str] = [branch for branch in list(data[region].keys())]
        for branch in branch_list:
            target_list: list[str] = [target for target in list(data[region][branch]["Hrefs"].keys())]
            for target in target_list:
                category_list: list[str] = [category for category in list(data[region][branch]["Hrefs"][target].keys())]
                for category in category_list:
                    with_link_index += 1
                    with_link: CenterInfoWithLink = CenterInfoWithLink(
                        region=region, address=data[region][branch]["Address"], branch=branch,
                        category=category, target=target, link=data[region][branch]["Hrefs"][target][category],
                        index=f"WITH_{str(with_link_index)}", name=center)
                    unwrap_list.append(with_link)
    return unwrap_list


def unwrap_no_link(data: dict, center: str) -> list[CenterInfoNoLink]:
    """
    json 파일 내용을 담은 객체들을 반환 한다. 해당 웹사이트에 나열 되어 있는 순서 그대로 가져온 내용 이므로
    순서를 지켜 접근 한다면 for 을 통해 어떤 요소가 지점 이름과 동일한지 찾지 않아도 된다.
    :param center:
    :param data: 링크가 없는 센터의 정보를 담은 dict
    :return: dictionary 를 펼쳐서 각각의 정보를 객체에 담은 뒤 리스트에 넣어 반환.
    """
    unwrap_list: list[CenterInfoNoLink] = []
    region_list: list[str] = [region for region in list(data.keys())]
    no_link_index: int = 0
    for region in region_list:
        branch_list: list[str] = [branch for branch in list(data[region].keys())]
        for branch in branch_list:
            no_link_index += 1
            no_link: CenterInfoNoLink = CenterInfoNoLink(
                region=region, branch=branch, address=data[region][branch],
                region_index=region_list.index(region), branch_index=branch_list.index(branch),
                index=f"NO_{str(no_link_index)}", name=center)
            unwrap_list.append(no_link)
    return unwrap_list
#
#
# def unwrap_no_link_by_crawler_index(data: dict, crawler_index: str, center: str) -> list[CenterInfoNoLink]:
#     """
#     크롤링한 가장 마지막 내용에서 가져온 crawler_index 는 center_infos[index].crawlerIndex 와 동일 하다는 전제 하에 진행.
#     crawler_index 부터 크롤링에 들어가게끔 사이트 설정 정보를 수정해 반환.
#     :param center:
#     :param data: 확인하고자 하는 사이트의 설정이 담긴 파일을 loads 한 값.
#     :param crawler_index: db 에서 가져온 crawlerIndex 값.
#     :return: 인덱싱 한 사이트의 설정 정보들.
#     """
#     center_infos: list[CenterInfoNoLink] = unwrap_no_link(data, center)
#     if validate_string(crawler_index):
#         index: int = int(crawler_index.replace("NO_", ""))
#         return center_infos[index - 1:]
#     return center_infos
#
#
# def unwrap_with_link_by_crawler_index(data: dict, crawler_index: str, center: str) -> list[CenterInfoWithLink]:
#     """
#     크롤링한 가장 마지막 내용에서 가져온 crawler_index 는 center_infos[index].crawlerIndex 와 동일 하다는 전제 하에 진행.
#     crawler_index 부터 크롤링에 들어가게끔 사이트 설정 정보를 수정해 반환.
#     :param center:
#     :param data: 확인하고자 하는 사이트의 설정이 담긴 파일을 loads 한 값.
#     :param crawler_index: db 에서 가져온 crawlerIndex 값.
#     :return: 인덱싱 한 사이트의 설정 정보들.
#     """
#     center_infos: list[CenterInfoWithLink] = unwrap_with_link(data, center)
#     if validate_string(crawler_index):
#         index: int = int(crawler_index.replace("WITH_", ""))
#         return center_infos[index:]
#     return center_infos
