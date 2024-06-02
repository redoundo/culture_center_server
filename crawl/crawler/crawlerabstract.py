from playwright.sync_api import Page
from crawl.typeclass.CenterInfoWithLink import CenterInfoWithLink
from crawl.typeclass.CenterInfoNoLink import CenterInfoNoLink
from crawl.typeclass.ClassIdInfoType import ClassIdInfos


class NoLinkCrawler:
    """
        검색 조건이 쿼리스트링에 설정 되지 않아 크롤러가 검색 조건을 직접 설정 해야 하는 사이트들이 대상.
    """
    centerInfo: CenterInfoNoLink
    page: Page
    url: str
    total: int
    pageCount: int
    lectureHrefs: list[str]
    lectureInfos: list[ClassIdInfos]

    def __init__(self, url: str, center_info: CenterInfoNoLink, page: Page) -> None:
        self.centerInfo = center_info
        self.page = page
        self.url = url

        self.lectureInfos = []
        self.lectureHrefs = []
        self.pageCount = -1
        self.total = -1
        return

    def crawl(self):
        """
           extract_lecture_info 를 제외한 메서드로 강의 들의 링크를 가져오는 역할을 한다.
           extract_lecture_info 는 새로운 객체를 만들어 따로 진행.
           :return:
        """
        pass

    def search_option_setting(self) -> None:
        """
        크롤링을 하기 위해 target, category 설정 제외한 지역과 지점 설정만 한다.
        :return:
        """
        pass

    def load_more(self):
        """
        페이지네이션 처리
        :return:
        """
        pass

    def check_lecture_total(self):
        """
        설정한 조건으로 존재하는 강의가 있는지 확인. 있다면 self 멤버 변수의 수를 바꾸고 없으면 -1 상태로 냅둔다.
        :return:
        """
        pass

    def get_loaded_lecture_url(self):
        """
        편리한 크롤링을 위해 로드된 강의들의 href 를 가져 온다.
        :return:
        """
        pass

    def extract_lecture_info(self, url: str, page: Page, info: dict):
        """
        강의 href 를 통해 강의 정보를 가져 온다.
        :param url: 내용을 추출할 url
        :param page: playwright Page 객체
        :param info: url 을 가져 왔을 때의 context
        :return:
        """
        pass

    def __call__(self, url: str, center_info: CenterInfoNoLink, page: Page):
        self.__init__(url, center_info, page)
        return


class WithLinkCrawler:
    """
    쿼리스트링으로 검색 조건을 설정할 수 있는 사이트들을 대상으로 크롤링을 실행한다.
    """
    centerInfo: CenterInfoWithLink
    page: Page

    total: int
    pageCount: int
    lectureHrefs: list[str]
    lectureInfos: list[ClassIdInfos]

    def __init__(self, center_info: CenterInfoWithLink, page: Page) -> None:
        self.page = page
        self.centerInfo = center_info

        self.total = -1
        self.pageCount = -1
        self.lectureInfos = []
        self.lectureHrefs = []
        return

    def crawl(self):
        """
        extract_lecture_info 를 제외한 메서드로 강의 들의 링크를 가져오는 역할을 한다.
        extract_lecture_info 는 새로운 객체를 만들어 따로 진행.
        :return:
        """
        pass

    def load_more(self):
        """
        페이지네이션 처리
        :return:
        """
        pass

    def get_loaded_lecture_url(self):
        """
        로드된 강의들의 href를 가져온다.
        :return:
        """
        pass

    def extract_lecture_info(self, url: str, page: Page, info: dict):
        """
        강의 정보를 가져온다.
        :param url:
        :param page:
        :param info:
        :return:
        """
        pass

    def goto_page(self, url: str) -> None:
        """
        url 페이지로 이동한다.
        :param url: 지점, 대상, 카테고리가 세팅된 url
        :return:
        """
        pass

    def rest_page(self):
        pass

    def __call__(self, center_info: CenterInfoWithLink, page: Page):
        self.__init__(center_info, page)
        return
