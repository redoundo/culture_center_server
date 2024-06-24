from crawler.settingcrawler.settingcrawlerabstract import SettingCrawler
import time
import re
from playwright.sync_api import Page

from typeclass.tableinfotypes import BranchesTableInfo


class HomePlusSettingCrawler(SettingCrawler):

    def __init__(self, page: Page):
        super().__init__(page)
        self.centerName = "HOMEPLUS"
        self.url: str = "https://corporate.homeplus.co.kr/STORE/HyperMarket.aspx"
        return

    def crawl(self):
        self.parse_info()
        self.goto()
        self.scrap()
        self.page.close()
        self.mysqlActions.connection.close()
        return

    def parse_info(self):
        self.branchInfos = self.mysqlActions.center_info_by_center_name(name=self.centerName)
        self.branchNames = [name for name in list(self.branchInfos.keys())]
        self.url = self.branchInfos[self.branchNames[0]].centerUrl
        return

    def scrap(self):
        self.page.click("#ctl00_ContentPlaceHolder1_Button1")
        time.sleep(2)

        locators = self.page.locator("#content > div > div > div > ul > li").all()
        exist_branch: list[str] = []
        for locator in locators:
            name_text: str = locator.locator("div:nth-child(1) > h3 > span.name > a").inner_text()
            if name_text not in self.branchNames:
                locator.locator("div:nth-child(1) > h3 > span.name > a").click()
                self.fallback(name_text)
            exist_branch.append(name_text)

        need_delete = [del_name for del_name in self.branchNames if del_name not in exist_branch]
        if len(need_delete) > 0:
            for need in need_delete:
                self.mysqlActions.add_or_delete_branches(method="delete", branch_id=self.branchInfos.get(need).branchId)
        return

    def fallback(self, name: str):
        time.sleep(2)
        address: str = self.page.inner_text("#store_detail01 > table > tbody > tr:nth-child(1) > td")
        data: dict = self.longitude_latitude(address)
        longitude = data["addresses"][0]["x"]
        latitude = data["addresses"][0]["y"]
        naver_address: str = data["address"][0]["jibunAddress"]
        address_element: list = data["address"][0]["addressElements"]
        split_address: list[str] = [address_element[0]["longName"], address_element[1]["longName"],
                                    address_element[2]["longName"]]

        if re.search(r"(\s?[가-힇0-9]+\s?)", address) is None:
            address = " ".join(naver_address.split(" ")[:-1])

        new_branch: BranchesTableInfo = BranchesTableInfo(state=split_address[0], city=split_address[1],
                                                          town=split_address[2],
                                                          center_id=self.branchInfos.get(self.branchNames[0])
                                                          .centerIdOfBranch, long=longitude, lat=latitude,
                                                          name=name, address=address)
        self.mysqlActions.add_or_delete_branches(method="add", branch_info=new_branch)
        self.page.go_back()
        time.sleep(2)
        return
