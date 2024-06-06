from crawl.crawler.crawlerabstract import PublicCenterCrawler
from crawl.typeclass.PublicLibrary import PublicLibrary
from crawl.typeclass.LectureType import LectureType
from playwright.sync_api import Page, Locator
import re
from crawl.crawler.utils.utils import validate_string, trim_lecture_time, trim_lecture_price


class PublicGneCrawler(PublicCenterCrawler):

    def crawl(self):
        for info in self.centerInfo:
            if info.get_library_name().find("교육청") > 0:
                self._edu_office_library_extract_info(info)
            elif info.get_library_name() == "김해통합도서관":
                self._lib_union_gimhae(info)
            elif info.get_library_name() == "통영시립도서관":
                self._tong_yeong_lib(info)
            else:
                continue
        return

    def _tong_yeong_lib(self, info: PublicLibrary):
        page: Page = self.browser.new_page()
        page.goto(info.get_link(), timeout=0)

        all_lectures: list[Locator] = page.locator("#program > div > table > tbody > tr").all()
        ing_locators: list[Locator] = []

        for locator in all_lectures:
            ing_text: str = locator.locator("td:nth-child(5) > span > img").get_attribute("alt")
            if ing_text.find("접수중") > 0:
                ing_locators.append(locator)

        for ing in ing_locators:
            lecture: LectureType = LectureType()
            lib_name: str = page.inner_text("#program > div > table > tbody > tr:nth-child(9) >\
             td:nth-child(1) > span > strong")
            center_name: list[str] = [name for name in list(info.get_addresses().keys()) if name.find(lib_name) > 0]
            if len(center_name) > 0:
                lecture.center = center_name[0]
                lecture.address = info.get_addresses()[lecture.center]

            ing.locator("td.tal > span > a").click(timeout=3000)

            lecture.url = page.url
            lecture.type = info.get_type()
            lecture.region = info.get_region()
            lecture.branch = info.get_branch()

            lecture.title = page.inner_text("#program > div > div.lecture_view > h4")
            str_price: str = page.inner_text("#program > div > div.lecture_view >\
             div:nth-child(5) > dl > dd:nth-child(4)")
            lecture.price = trim_lecture_price(str_price)

            lecture.content = page.inner_text("#program > div > div.lecture_view > div.lecture_contents")
            lecture.content = (lecture.content + "@#$" + page.locator("#program > div > div.lecture_view >\
             div.lecture_contents > p:nth-child(5) > img").get_attribute("src"))
            # lecture.src = page.locator("#body_content > div > div.cp20view1 > div.even-grid.float-left >\
            #  div:nth-child(1) > div > p.p1 > img").get_attribute("src")
            #
            # if len(page.locator("#tabs1pane1 > h3").all()) > 2:  # 강의 계획서가 이미지로라도 존재 하면 가지고 온다.
            #     lecture.set_curriculum({1: page.locator("#tabs1pane1 > p > img").get_attribute("src")})

            enroll_start_end: dict = trim_lecture_time(page.inner_text("#program > div > div.lecture_view >\
             div.lecture_view_detail > div.row_info2 > dl > dd:nth-child(2) > strong"), "~")
            lecture.enrollStart = enroll_start_end[0]
            lecture.enrollEnd = enroll_start_end[1]

            lecture_start_end: dict = trim_lecture_time(page.inner_text("#program > div > div.lecture_view >\
             div.lecture_view_detail > div.row_info2 > dl > dd:nth-child(4)"), "~")
            lecture.lectureStart = lecture_start_end[0]
            lecture.lectureEnd = lecture_start_end[1]

            lecture.target = page.inner_text("#program > div > div.lecture_view > div:nth-child(2) > dl > dd.wpix")
            supplies = page.inner_text("#program > div > div.lecture_view > div:nth-child(5) > dl > dd.wpix")
            if validate_string(supplies):
                lecture.lectureSupplies = supplies
            page.go_back(timeout=3000)

        page.close()
        return

    def _lib_union_gimhae(self, info: PublicLibrary):
        page: Page = self.browser.new_page()
        page.goto(info.get_link(), timeout=0)
        ing_lectures_num = int(page.inner_text("#body_content > div > div.infomenu1 > div.left > div > em:nth-child(1)"))
        if ing_lectures_num < 1:
            page.close()
            return
        all_lectures: list[Locator] = (
            page.locator("#body_content > div > div.list2table1 > div > div > table > tbody > tr").all())
        ing_href: list[str] = []
        for locator in all_lectures:
            ing_text: str = locator.locator("td:nth-child(6)").inner_text()
            if ing_text.find("접수중") > 0:
                ing_href.append(locator.locator("td.tal > a").get_attribute("href"))

        for href in ing_href:
            page.goto(href, timeout=5000)
            lecture: LectureType = LectureType()

            lecture.url = page.url
            lib_name: str = page.inner_text("#body_title > h1")
            center_name: list[str] = [name for name in list(info.get_addresses().keys()) if name.find(lib_name) > 0]
            lecture.center = center_name[0]
            lecture.address = info.get_addresses()[lecture.center]
            lecture.type = info.get_type()
            lecture.region = info.get_region()
            lecture.branch = info.get_branch()

            lecture.title = page.inner_text("#body_content > div > div.cp20view1 > div.hg1 > h2")
            str_price: str = page.inner_text("#body_content > div > div.cp20view1 > div.even-grid.float-left >\
             div:nth-child(2) > div > div.cp20dlist1 > ul > li:nth-child(7) > span")
            lecture.price = trim_lecture_price(str_price)

            lecture.content = page.inner_text("#tabs1pane1 > div")
            lecture.content = (lecture.content + "@#$" +
                               page.locator("#tabs1pane1 > div > div > p:nth-child(3) > img").get_attribute("src"))
            lecture.src = page.locator("#body_content > div > div.cp20view1 > div.even-grid.float-left >\
             div:nth-child(1) > div > p.p1 > img").get_attribute("src")

            if len(page.locator("#tabs1pane1 > h3").all()) > 2:  # 강의 계획서가 이미지로라도 존재 하면 가지고 온다.
                lecture.set_curriculum({1: page.locator("#tabs1pane1 > p > img").get_attribute("src")})

            enroll_start_end: dict = trim_lecture_time(page.inner_text("#body_content > div > div.cp20view1 >\
             div.even-grid.float-left > div:nth-child(2) > div > div.cp20dlist1 > ul > li.di.bdt0 > span"), "~")
            lecture.enrollStart = enroll_start_end[0]
            lecture.enrollEnd = enroll_start_end[1]

            lecture_start_end: dict = trim_lecture_time(page.inner_text("#body_content > div > div.cp20view1 >\
             div.even-grid.float-left > div:nth-child(2) > div > div.cp20dlist1 > ul > li:nth-child(2) > span"), "~")
            lecture.lectureStart = lecture_start_end[0]
            lecture.lectureEnd = lecture_start_end[1]

            lecture.target = page.inner_text("#body_content > div > div.cp20view1 >\
             div.even-grid.float-left > div:nth-child(2) > div > div.cp20dlist1 > ul > li:nth-child(4) > span")
            lecture.lectureSupplies = page.inner_text("#body_content > div > div.cp20view1 > div.even-grid.float-left >\
             div:nth-child(2) > div > div.cp20dlist1 > ul > li:nth-child(8) > span")
        page.close()
        return

    def _edu_office_library_extract_info(self, info: PublicLibrary):
        page: Page = self.browser.new_page()
        page.goto(info.get_link(), timeout=0)
        page.click(info.get_to_enroll(), timeout=3000, delay=200)
        lecture_locators = page.locator("#content_detail > div.mb_scroll > table > tbody > tr").all()
        locator_list: list = []  # 모집 중인 강좌의 locator 만 모아 놓는다.
        for locator in lecture_locators:
            status = locator.locator("td:nth-child(6) > img").get_attribute("alt")
            locator.click(timeout=2000)
            if status is not None and status == "모집중":
                locator_list.append(locator)
            else:
                continue

        if len(locator_list) < 1:
            page.close()
            return

        for loc in locator_list:
            lecture: LectureType = LectureType()

            lecture.center = info.get_library_name()
            lecture.address = info.get_addresses()[lecture.center]
            lecture.region = info.get_region()
            lecture.branch = info.get_branch()
            lecture.type = info.get_type()

            lecture.category = loc.locator("td.subject").inner_text(timeout=4000)
            lecture_raw_info = loc.locator("td.subject2 > a").inner_text(timeout=4000)
            split_raw_info = re.split(r"\n+", lecture_raw_info)
            print(split_raw_info)
            print(len(split_raw_info))
            lecture.title = split_raw_info[0]
            lecture.enrollStart = re.sub(r"\s*ㆍ모집\s?기간\s?:\s+|[0-9]{2}\s?:\s?[0-9]{2}", "", split_raw_info[1])
            lecture.enrollEnd = re.sub(r"\s{3,30}|[0-9]{2}\s?:\s?[0-9]{2}", "", split_raw_info[2])
            start_end: list[str] = re.split(r"\s?[-~]\s?", lecture_raw_info[3])
            lecture.lectureStart = re.sub(r"\n?\s*ㆍ학습\s?기간\s?:\s?|\s{1,10}", "", start_end[0])
            lecture.lectureEnd = re.sub(r"\s{1,10}", "", start_end[1])
            lecture.target = loc.locator("td:nth-child(3)").inner_text(timeout=4000)
            loc.click(timeout=2000)

            price = page.inner_text("#content_detail > table > tbody > tr:nth-child(9) > td:nth-child(6)", timeout=3000)
            print(price)
            search_price = re.search(r"\s?[0-9,]+([가-힇]원)?", price)
            if search_price is not None:
                lecture.price = int(search_price.group().replace(",", ""))
            else:
                lecture.price = 0
            lecture_supplies = page.inner_text("#content_detail > table > tbody > tr:nth-child(9) > td:nth-child(4)")
            print(lecture_supplies)
            search_supplies = re.search(r"\s?[0-9,]+([가-힇]원)?", lecture_supplies)
            if search_supplies is not None:
                lecture.lectureSupplies = re.sub(r"\s{2,10}", "", lecture_supplies)

            lecture.url = page.url
            lecture.content = (
                page.inner_text("#content_detail > table > tbody > tr:nth-child(10) > td:nth-child(2)", timeout=2000))

            self.database.insert_into_db(lecture)
            page.go_back()

        page.close()
        return




