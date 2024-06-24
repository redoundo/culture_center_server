from crawler.settingcrawler.settingcrawlerabstract import SettingCrawler
import time
import re
from playwright.sync_api import Page

from typeclass.tableinfotypes import BranchesTableInfo


class HyundaiSettingCrawler(SettingCrawler):

    def __init__(self, page: Page):
        super().__init__(page)
        self.centerName = "HYUNDAI"
        self.url: str = "https://www.ehyundai.com/newCulture/CT/CT050100_M.do"
        return

    def crawl(self):
        self.goto()
        self.parse_info()
        self.scrap()
        self.page.close()
        self.mysqlActions.connection.close()
        return

    def scrap(self):
        locators = self.page.locator("#contents > div > div > div > div.tab_wrap.type_box.branch > div.tabs > ul > li").all()
        exist_branch: list[str] = []
        for locator in locators:
            branch_text: str = locator.locator("a").inner_text()
            if branch_text not in self.branchNames:
                self.fallback(branch_text)
            exist_branch.append(branch_text)
        self.page.goto("https://www.ehyundai.com/newCulture/CT/CH050100_M.do", timeout=0)

        ch_locators = self.page.locator("#contents > div > div > div > div.tab_wrap.type_box.ui_tab > div.tabs > ul > li").all()
        for ch_locator in ch_locators:
            ch_branch_text: str = ch_locator.locator("a").inner_text()
            exist_branch.append(ch_locator.locator("a").inner_text())
            if ch_branch_text not in self.branchNames:
                self.fallback(ch_branch_text)

        need_delete = [del_name for del_name in self.branchNames if del_name not in exist_branch]
        if len(need_delete) > 0:
            for need in need_delete:
                self.mysqlActions.add_or_delete_branches(method="delete", branch_id=self.branchInfos.get(need).branchId)
        return

    def fallback(self, name: str):
        address: str = self.page.inner_text(
            "#contents > div > div > div > div.tab_wrap.type_box.ui_tab > div.tab_conts > div > div.branch_desc_box > dl > div:nth-child(1) > dd")
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






