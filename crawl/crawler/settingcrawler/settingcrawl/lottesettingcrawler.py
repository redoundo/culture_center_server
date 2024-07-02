from crawler.settingcrawler.settingcrawlerabstract import SettingCrawler
import time
import re
from playwright.sync_api import Page

from typeclass.tableinfotypes import BranchesTableInfo


class LotteSettingCrawler(SettingCrawler):

    def __init__(self, page: Page):
        super().__init__(page)
        self.centerName = "LOTTE"
        self.url: str = "https://culture.lotteshopping.com/information/branch/list.do"
        return

    def crawl(self):
        self.goto()
        self.parse_info()
        self.scrap()
        self.page.close()
        self.mysqlActions.connection.close()
        return

    def scrap(self):
        locators = self.page.locator("#wrap > header > div.srch_gate_pop_area > div > div.scroll_area > div > div.tab_con_area > div.con.on > div.content.only_pc > div.list_w > div").all()
        exist_branch: list[str] = []
        for locator in locators:
            branch_locators = locator.locator("div > p").all()
            for branch_locator in branch_locators:
                branch_text: str = branch_locator.locator("a").inner_text()
                if branch_text not in self.branchNames:
                    branch_locator.locator("a").click()
                    self.fallback(branch_text)
                exist_branch.append(branch_text)

        need_delete = [del_name for del_name in self.branchNames if del_name not in exist_branch]
        if len(need_delete) > 0:
            for need in need_delete:
                self.mysqlActions.add_or_delete_branches(method="delete", branch_id=self.branchInfos.get(need).branchId)
        return

    def fallback(self, name: str):
        address: str = self.page.inner_text(
            "#dtlArea > div > div:nth-child(1) > div > div.store_txt_wrap > p:nth-child(1)").split("\n")[0]
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







