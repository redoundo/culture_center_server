from typeclass.LectureType import LectureType
from crawler.crawlerabstract import NoLinkCrawler
from typeclass.ClassIdInfoType import ClassIdInfos
import math
import time
import re
from playwright.sync_api import Page


class HomePlusCrawler(NoLinkCrawler):

    def crawl(self):
        self.search_option_setting()

        self.check_lecture_total()
        self.load_more()

        self.get_loaded_lecture_url()
        return

    def search_option_setting(self):
        self.page.goto(self.url, timeout=0)
        region_index: int = 0
        branch_index: int = 0

        region_locators = self.page.locator("#wrapper > section > div > div.menu_depth_2_wrap > div > div > ul.tree_menu.tree_menu_1.on > li").all()
        for region_locator in region_locators:
            if region_locators.index(region_locator) == 0:
                continue
            region_name: str = self.page.inner_text(f"#wrapper > section > div > div.menu_depth_2_wrap > div > div > ul.tree_menu.tree_menu_1.on > li:nth-child({region_locators.index(region_locator) + 1}) > button > span")
            if region_name == self.centerInfo.get_region():
                region_index = region_locators.index(region_locator)
            else:
                continue

        # 지역 클릭.
        self.page.click(f"#wrapper > section > div > div.menu_depth_2_wrap > div > div >\
                 ul.tree_menu.tree_menu_1.on > li:nth-child({region_index + 2}) > button", timeout=5000,
                        delay=100)
        region_active: str = self.page.get_attribute(f"#wrapper > section > div > div.menu_depth_2_wrap > div > div >\
         ul.tree_menu.tree_menu_1.on > li:nth-child({region_index + 2}) > button", "class", timeout=500)

        if region_active is None or region_active.find("on") == -1:
            self.page.click(f"#wrapper > section > div > div.menu_depth_2_wrap > div > div >\
                     ul.tree_menu.tree_menu_1.on > li:nth-child({region_index + 2}) > button", timeout=5000, delay=100)

        exist_branch_names: list[str] = []
        branch_locators = self.page.locator(f"#wrapper > section > div > div.menu_depth_2_wrap > div > div > ul.tree_menu.tree_menu_1.on > li:nth-child({region_index + 2}) > ul > li").all()
        for branch_locator in branch_locators:
            if branch_locators.index(branch_locator) == 0:
                continue
            branch_name: str = self.page.inner_text(f"#wrapper > section > div > div.menu_depth_2_wrap > div > div > ul.tree_menu.tree_menu_1.on > li:nth-child({region_index + 2}) > ul > li:nth-child({branch_locators.index(branch_locator) + 1}) > button > span")
            exist_branch_names.append(branch_name)
            if branch_name != self.centerInfo.get_branch():
                continue
            else:
                branch_index = branch_locators.index(branch_locator)
        exist_branch_names.sort()
        if not (exist_branch_names == self.branches):
            raise Exception("BRANCH_UNMATCH")

        self.page.click(f"#wrapper > section > div > div.menu_depth_2_wrap > div > div >\
         ul.tree_menu.tree_menu_1.on > li:nth-child({region_index + 2}) > ul >\
          li:nth-child({branch_index + 2})", timeout=5000, delay=100)  # 지점 클릭
        time.sleep(2)

        button_locator = self.page.locator("#wrapper > footer > div.footer_top_scroll > button").all()  # 설정된 조건 확인
        if len(button_locator) == 0 or len(button_locator) > 1:  # 조건이 없으면 다시 지점 클릭.조건이 여러 개면 초기화 후 지점 클릭.
            if len(button_locator) > 1:
                self.page.click("#wrapper > footer > div.footer_inner_bottom > button.btn_reload", timeout=3000,
                                delay=20)
            self.page.click(f"#wrapper > section > div > div.menu_depth_2_wrap > div > div >\
                                 ul.tree_menu.tree_menu_1.on > li:nth-child({region_index + 2}) > ul >\
                                  li:nth-child({branch_index + 2})", timeout=5000, delay=100)
        # 검색 시작.
        self.page.click("#wrapper > footer > div.footer_inner_bottom > button.btn_reuslt_search", timeout=5000, delay=20)

        time.sleep(5)
        return

    def load_more(self):
        if self.total < 0 and self.pageCount < 0:
            return
        else:
            for _ in range(0, self.pageCount):
                self.page.evaluate("() => window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
        return

    def check_lecture_total(self):
        total_text: str = self.page.inner_text("#contents_body > div.search_filter > div >\
         div.tooltip_wrap > button > span")
        total: int = int(total_text.replace("개 강좌", ""))
        if total > 0:
            self.total = total
            self.pageCount = math.ceil(total/20)
        return

    def get_loaded_lecture_url(self):
        all_hrefs = self.page.locator("#contents_body > div.search_result_list > ul > li").all()
        for href in all_hrefs:
            lecture_href: str = href.get_attribute("id")
            status: str = href.locator("div > button").get_attribute("onclick")
            if status is None:
                status_text: str = href.locator("div > button > span:nth-child(3)").inner_text()
                if status_text == "마감":
                    break
                else:
                    continue
            if lecture_href is not None:
                href_id: int = int(lecture_href.split("_")[1])
                self.lectureHrefs.append(f"https://mschool.homeplus.co.kr/Lecture/Detail?LectureMasterID={href_id}")
        return

    def extract_lecture_info(self, url: str, page: Page, info: dict):
        page.goto(url, timeout=0)
        time.sleep(5)

        lecture: LectureType = LectureType()
        lecture.url = page.url
        lecture.address = info.get("address")
        lecture.branch = info.get("branch")
        lecture.region = info.get("region")
        lecture.crawlerIndex = info.get("crawler_index")
        lecture.type = "대형마트"
        lecture.center = "HOMEPLUS"

        try:
            src = page.get_attribute("#contents > div.lecture_details >\
             div.swiper-container.lecture_detail_big.swiper-container-initialized.swiper-container-horizontal >\
              div > div > img", "src", timeout=60000)
            lecture.src = src
        except Exception as e:
            lecture.src = "NULL"
        title: str = page.inner_text("#contents > div.lecture_detail_header > dl > dt", timeout=60000)
        title_sub: str = page.inner_text("#contents > div.lecture_detail_header > dl > dd.summary", timeout=60000)
        lecture.title = (title + " " + title_sub).replace("'", "''")

        target_category: list[str] = (
            page.inner_text("#contents > div.lecture_detail_header > div > p.icon").split("] "))
        lecture.target = target_category[0].replace("[", "")
        lecture.category = target_category[1]

        lecture_price: str = page.inner_text("#lecture_detail_cont_0 > div > table > tbody >\
         tr:nth-child(7) > td > div", timeout=60000)
        price = re.findall(r"[0-9,]+\s?원", lecture_price)
        if price is not None:
            all_prices: list = price
            real_price: str = all_prices[-1]
            lecture.price = int(real_price.replace("원", "").replace(",", ""))

        lecture.lectureSupplies = page.inner_text("#lecture_detail_cont_0 > div > table > tbody >\
         tr:nth-child(8) > td > div", timeout=60000).replace("'", "''")

        lecture_count_str: str = page.inner_text("#lecture_detail_cont_0 > div > table > tbody >\
         tr:nth-child(5) > td > div", timeout=60000).split("회(")[0]
        lecture_count: int = int(lecture_count_str.replace("총", ""))

        page.click("#contents > div.tabmenu.tab2ea > ul > li:nth-child(2) > a", timeout=6000, delay=20)
        time.sleep(5)

        lecture.content = page.inner_text("#lecture_detail_cont_1 > div:nth-child(1) > div", timeout=60000).replace("'", "''")

        curriculums = (page.locator("#lecture_detail_cont_1 > div:nth-child(2) > div > div > table > tbody > tr")
                       .all())
        all_curriculums: dict = {}
        for curriculum in curriculums:
            if curriculums.index(curriculum) <= lecture_count:

                curriculum_text: str = curriculum.locator("td.sbj > div").inner_text(timeout=60000)
                text_curriculum = re.sub(r"'", "''", curriculum_text)
                curriculum_sub = re.sub(r"\n", "", text_curriculum)
                text_sub = re.sub(r'"', '\\"', curriculum_sub)

                if len(text_sub) > 3:
                    all_curriculums[curriculums.index(curriculum) + 1] = text_sub
            else:
                break

        lecture_span: list[str] = page.inner_text("#lecture_detail_cont_0 > div > table > tbody >\
         tr:nth-child(4) > td > div", timeout=60000).split(" ~ ")
        lecture_date_detail = page.inner_text("#lecture_detail_cont_0 > div > table > tbody >\
         tr:nth-child(3) > td > div")
        lecture.set_lecture_held_dates(lecture_span, lecture_date_detail, lecture_count)

        if len(list(all_curriculums.keys())) > 0:
            lecture.set_curriculum(all_curriculums)

        lecture.classId = ClassIdInfos.make_class_id(lecture)

        yield lecture

        self.lectureInfos.append(lecture)
        return