from crawl.crawler.crawlerabstract import NoLinkCrawler, WithLinkCrawler
from crawl.crawler.nolink.EmartCrawler import EmartCrawler
from crawl.crawler.nolink.LotteMartCrawler import LotteMartCrawler
from crawl.crawler.nolink.HomePlusCrawler import HomePlusCrawler
from crawl.crawler.nolink.AkplazaCrawler import AkplazaCrawler
from crawl.crawler.withlink.GalleriaCrawler import GalleriaCrawler
from crawl.crawler.withlink.HyundaiCrawler import HyundaiCrawler
from crawl.crawler.withlink.LotteCrawler import LotteCrawler
import enum


class NoLinkCrawlerFactory(enum.Enum):
    """
    쿼리 스트링 조합으로 검색이 불가능한 사이트들을 크롤링 하는 크롤러를 생산
    """
    HOMEPLUS = ("HOMEPLUS", HomePlusCrawler, "https://mschool.homeplus.co.kr/Lecture/Search",
                "crawler/resource/homeplus.json")
    EMART = ("EMART", EmartCrawler, "https://www.cultureclub.emart.com/enrolment",
             "crawler/resource/emart.json")
    LOTTEMART = ("LOTTEMART", LotteMartCrawler, "https://culture.lottemart.com/cu/gus/course/courseinfo/courselist.do?",
                 "crawler/resource/lottemart.json")
    AKPLAZA = ("AKPLAZA", AkplazaCrawler, "https://culture.akplaza.com/course/list02",
               "crawler/resource/akplaza.json")

    def __init__(self, center: str, crawler: NoLinkCrawler, url: str, path: str):
        """
        크롤러에 필요한 내용과 크롤러를 가리키는 객체를 담는다.
        :param center: 센터 이름
        :param crawler: 센터의 크롤러
        :param url: 센터 기본 url 주소
        :param path: 센터 설정이 들어있는 파일의 주소
        """
        self.center = center
        self.crawler = crawler
        self.url = url
        self.path = path
        return

    @classmethod
    def get_all_center_names(cls) -> list[str]:
        return [name[0] for name in cls.__members__.items()]

    @classmethod
    def get_crawler(cls, center: str) -> NoLinkCrawler:
        return [member.crawler for name, member in cls.__members__.items() if name == center][0]

    @classmethod
    def get_url(cls, center: str) -> str:
        return [member.url for name, member in cls.__members__.items() if name == center][0]

    @classmethod
    def get_all_center_paths(cls) -> dict:
        """
        센터 이름과 센터 내용 파일의 위치 반환.
        :return: {HOMEPLUS : "C:/Users/admin/flaskserver/server/app/crawl/resource/homeplus.json", ...} 형식의  dict
        """
        center_and_path: dict = {}
        for name, member in cls.__members__.items():
            center_and_path[name] = member.path
        return center_and_path


class WithLinkCrawlerFactory(enum.Enum):
    """
    쿼리 스트링 조합으로 검색이 가능한 사이트들을 크롤링 하는 크롤러 생산
    """
    HYUNDAI = ("HYUNDAI", HyundaiCrawler, "crawl/resource/hyundai.json")
    GALLERIA = ("GALLERIA", GalleriaCrawler, "crawl/resource/galleria.json")
    LOTTE = ("LOTTE", LotteCrawler, "crawl/resource/lotte.json")

    def __init__(self, center: str, crawler: WithLinkCrawler, path: str):
        """
        크롤러 생성에 필요한 내용과 각 센터들의 크롤러 객체 자체를 포함.
        :param center: 센터 이름
        :param crawler: 센터 크롤러
        :param path: 센터 설정이 들어있는 파일의 위치
        """
        self.center = center
        self.crawler = crawler
        self.path = path
        return

    @classmethod
    def get_all_center_names(cls) -> list[str]:
        return [name[0] for name in cls.__members__.items()]

    @classmethod
    def get_crawler(cls, center: str) -> WithLinkCrawler:
        return [member.crawler for name, member in cls.__members__.items() if name == center][0]

    @classmethod
    def get_all_center_paths(cls) -> dict:
        """
        센터 내용 위치와 센터 이름 반환.
        :return: {HYUNDAI: "C:/Users/admin/flaskserver/server/app/crawl/resource/hyundai.json", ...} 형식의 dict
        """
        center_and_path: dict = {}
        for name, member in cls.__members__.items():
            center_and_path[name] = member.path
        return center_and_path

