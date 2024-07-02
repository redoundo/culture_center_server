import enum
from crawler.settingcrawler.settingcrawl.emartsettingcrawler import EmartSettingCrawler
from crawler.settingcrawler.settingcrawl.lottesettingcrawler import LotteSettingCrawler
from crawler.settingcrawler.settingcrawl.akplazasettingcrawler import AkplazaSettingCrawler
from crawler.settingcrawler.settingcrawl.hyundaisettingcrawler import HyundaiSettingCrawler
from crawler.settingcrawler.settingcrawl.galleriasettingcrawler import GalleriaSettingCrawler
from crawler.settingcrawler.settingcrawl.homeplussettingcrawler import HomePlusSettingCrawler
from crawler.settingcrawler.settingcrawl.lottemartsettingcrawler import LotteMartSettingCrawler
from crawler.settingcrawler.settingcrawl.shinsegaesettingcrawler import ShinsegaeSettingCrawler
from crawler.settingcrawler.settingcrawlerabstract import SettingCrawler


class SettingCrawlerFactory(enum.Enum):

    SHINSEGAE = ("SHINSEGAE", ShinsegaeSettingCrawler)
    LOTTE = ("LOTTE", LotteSettingCrawler)
    LOTTEMART = ("LOTTEMART", LotteMartSettingCrawler)
    HOMEPLUS = ("HOMEPLUS", HomePlusSettingCrawler)
    AKPLAZA = ("AKPLAZA", AkplazaSettingCrawler)
    GALLERIA = ("GALLERIA", GalleriaSettingCrawler)
    HYUNDAI = ("HYUNDAI", HyundaiSettingCrawler)
    EMART = ("EMART", EmartSettingCrawler)

    def __init__(self, name: str, crawler: SettingCrawler):
        self.center = name
        self.crawler = crawler
        return

    @classmethod
    def get_crawler(cls, center: str) -> SettingCrawler:
        """
        사이트 이름으로 크롤러 클래스를 찾아 반환한다.
        :param center: 사이트 이름
        :return: 해당 사이트의 크롤러
        """
        return [member.crawler for name, member in cls.__members__.items() if name == center][0]


