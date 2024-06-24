import re

from typeclass.tableinfotypes import BranchesTableInfo
from crawler.settingcrawler.settingcrawlerabstract import SettingCrawler
import time
from playwright.sync_api import Page


class ShinsegaeSettingCrawler(SettingCrawler):

    def __init__(self, page: Page):
        super().__init__(page)
        self.centerName = "SHINSEGAE"
        self.url = "https://www.shinsegae.com/culture/academy/about.do?tapCode="
        return

    def crawl(self):
        self.goto()
        self.parse_info()
        self.scrap()
        self.page.close()
        self.mysqlActions.connection.close()
        return

    def scrap(self):
        locators = self.page.locator("#inContent > div.shop_select.wrap.mb40 > ul > li").all()
        exist_branch: list[str] = []
        for locator in locators:
            branch_text: str = locator.locator("a").inner_text()
            if branch_text not in self.branchNames:
                locator.locator("a").click()
                self.fallback(branch_text)
            exist_branch.append(branch_text)
        need_delete = [del_name for del_name in self.branchNames if del_name not in exist_branch]
        if len(need_delete) > 0:
            for need in need_delete:
                self.mysqlActions.add_or_delete_branches(method="delete", branch_id=self.branchInfos.get(need).branchId)
        return

    def fallback(self, name: str):
        address: str = self.page.inner_text(
            "#contents_01 > table.table_area.table2.mt30.mb15 > tbody > tr:nth-child(1) > td")

        data: dict = self.longitude_latitude(address)
        longitude = data["addresses"][0]["x"]
        latitude = data["addresses"][0]["y"]
        naver_address: str = data["address"][0]["jibunAddress"]
        address_element: list = data["address"][0]["addressElements"]
        split_address: list[str] = [address_element[0]["longName"], address_element[1]["longName"],
                                    address_element[2]["longName"]]

        if re.search(r"(\s?[가-힇0-9]+\s?)", address) is None:  # 동이 존재하지 않을 경우 네이버에서 받아온 주소를 사용
            if re.search(r"\s?신세계\s?|백화점", naver_address) is not None:  # 추가적인 내용이 붙어있을 경우 제외
                naver_address_split: list[str] = naver_address.split(" ")
                address = " ".join(naver_address_split[:-1])
            else:
                address = naver_address

        new_branch: BranchesTableInfo = BranchesTableInfo(state=split_address[0], city=split_address[1],
                                                          town=split_address[2],
                                                          center_id=self.branchInfos.get(self.branchNames[0])
                                                          .centerIdOfBranch, long=longitude, lat=latitude,
                                                          name=name, address=address)
        self.mysqlActions.add_or_delete_branches(method="add", branch_info=new_branch)
        return

