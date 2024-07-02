import abc
from crawler.db.MysqlActions import MysqlActions
from playwright.sync_api import Page
from typeclass.branchinfoforsetting import BranchInfoForSetting
import requests
from dotenv import load_dotenv
import os
import time
load_dotenv()


class SettingCrawlerAbstract(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def goto(self):
        pass

    @abc.abstractmethod
    def crawl(self):
        pass

    @abc.abstractmethod
    def parse_info(self):
        pass

    @abc.abstractmethod
    def scrap(self):
        pass

    @abc.abstractmethod
    def fallback(self, name: str):
        pass


class SettingCrawler(SettingCrawlerAbstract):

    mysqlActions: MysqlActions
    centerName: str
    url: str
    page: Page
    branchNames: list[str]
    branchInfos: dict[str, BranchInfoForSetting]
    ncpId: str = os.getenv("X-NCP-APIGW-API-KEY-ID")
    ncpSecret: str = os.getenv("X-NCP-APIGW-API-KEY")

    def __init__(self, page: Page):
        self.page = page
        self.mysqlActions = MysqlActions()
        return

    def __call__(self, page: Page):
        self.__init__(page)
        return

    def fallback(self, name: str):
        pass

    def longitude_latitude(self, address: str) -> dict:
        response = requests.get(f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}",
                                headers={"X-NCP-APIGW-API-KEY-ID": self.ncpId, "X-NCP-APIGW-API-KEY": self.ncpSecret})
        data = response.json()
        return data

    def goto(self):
        self.page.goto(self.url, timeout=0)
        time.sleep(2)
        return

    def scrap(self):
        pass

    def crawl(self):
        pass

    def parse_info(self):
        self.branchInfos = self.mysqlActions.center_info_by_center_name(name=self.centerName)
        self.branchNames = [name for name in list(self.branchInfos.keys())]
        return
