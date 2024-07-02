from crawler.settingcrawler.settingcrawlerabstract import SettingCrawler
import re
import time
from playwright.sync_api import Page

from typeclass.tableinfotypes import BranchesTableInfo


class LotteMartSettingCrawler(SettingCrawler):

    def __init__(self, page: Page):
        super().__init__(page)
        self.centerName = "AKPLAZA"
        self.url: str = "https://culture.lottemart.com/cu/customer/branchSearch/main.do"
        return

    def crawl(self):
        self.goto()
        self.parse_info()
        self.scrap()
        self.page.close()
        self.mysqlActions.connection.close()
        return

    def scrap(self):
        count: int = int(self.page.inner_text("#contents > div.btn_more-area.listAdd > a > em")
                         .replace("(1/", "").replace(")", ""))
        for click in range(0, count):
            self.page.click("#contents > div.btn_more-area.listAdd > a")
            time.sleep(1)

        locators = self.page.locator("#listTbody > tr").all()
        exist_branch: list[str] = []
        for locator in locators:
            branch_text: str = locator.locator("td:nth-child(1)").inner_text()
            if branch_text not in self.branchNames:
                self.fallback(branch_text)
            exist_branch.append(branch_text)

        need_delete = [del_name for del_name in self.branchNames if del_name not in exist_branch]
        if len(need_delete) > 0:
            for need in need_delete:
                self.mysqlActions.add_or_delete_branches(method="delete", branch_id=self.branchInfos.get(need).branchId)
        return

    def fallback(self, name: str):
        locators = self.page.locator("#listTbody > tr").all()
        for locator in locators:
            branch_text: str = locator.locator("td:nth-child(1)").inner_text()
            if name != branch_text:
                continue
            address: str = locator.locator("td:nth-child(2) > ul > li:nth-child(2)").inner_text().replace("(신) ", "")
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
        return
