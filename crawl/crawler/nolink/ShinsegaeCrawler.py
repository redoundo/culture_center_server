import re
import copy
import time
from pytz import timezone
import datetime
from crawl.typeclass.CenterInfoNoLink import CenterInfoNoLink
from crawl.typeclass.LectureType import LectureType
from crawl.crawler.crawlerabstract import NoLinkCrawler
from crawl.typeclass.ClassIdInfoType import ClassIdInfos
from playwright.sync_api import Page


class ShinsegaeCrawler(NoLinkCrawler):
    currentPage: int

    def __init__(self, url: str, center_info: CenterInfoNoLink, page: Page):
        super().__init__(url, center_info, page)
        self.currentPage = 1
        return

    def crawl(self):
        self.search_option_setting()
        self.check_lecture_total()
        for _ in range(0, self.pageCount):
            self.get_loaded_lecture_url()
            self.load_more()
        return

    def search_option_setting(self) -> None:
        self.page.goto(self.url, timeout=0)
        time.sleep(2)

        self.page.select_option(selector="#storeCode", label=self.centerInfo.get_branch(), timeout=4000)
        self.page.click(selector="#btnInquiry", timeout=4000)  # 변경 되었는지 확인 가능한 방법이 별도로 없음....미친..
        time.sleep(3)
        return

    def load_more(self):
        if self.pageCount < 2:
            return
        pagination = self.page.locator(selector="#pageNavi > a").all()
        for page in pagination:
            page_str: str = page.inner_text()
            # 현재 10 페이지에 위치해 있고 총 페이지가 12 이상일 경우에 11 버튼이 아닌 > 버튼을 누른다. 11, 21,31... 숫자도 동일 하다.
            if (self.currentPage % 10) == 0 and self.pageCount > self.currentPage + 1:
                span_selector = self.page.locator("#pageNavi > span").all()
                a_selector = span_selector[-1].locator("a").all()[0]  # > 버튼
                self.currentPage += 1
                a_selector.click()
                break
            elif int(page_str) == self.currentPage + 1:
                self.currentPage += 1
                page.click()
                break
            else:
                continue
        time.sleep(2)
        return

    def check_lecture_total(self):
        lectures = self.page.locator(selector="#lectList > tr").all()
        if len(lectures) < 10:
            self.total = len(lectures)
            self.pageCount = 1
            return

        locators = self.page.locator(selector="#pageNavi > a").all()
        if len(locators) < 9:  # 페이지 버튼이 9 개 보다 적으면 추가적으로 이동해야 하는 페이지가 존재하지 않는 다는 의미.
            self.total = 10 * len(locators)
            self.pageCount = len(locators)
            return

        span_locators = self.page.locator(selector="#pageNavi > span").all()
        a_locators = span_locators[-1].locator("a").all()
        if len(a_locators) < 1:  # 9 개 여도 페이지가 더 없을 수 있으므로 따로 처리
            self.total = 10 * len(locators)
            self.pageCount = len(locators)
            return

        total_str: str = a_locators[-1].get_attribute("onclick")
        a_locators[-1].click(timeout=4000)
        time.sleep(2)
        last_lectures = self.page.locator(selector="#lectList > tr").all()  # 맨 마지막 길이는 10 보다 더 작을 수 있으므로 확인 후 더한다.
        total_page: int = int(total_str.replace("javascript:fnGoPage(", "").replace(")", ""))

        self.pageCount = total_page
        self.total = (total_page - 1) * 10 + len(last_lectures)

        self.page.reload()  # 첫 페이지로 이동
        time.sleep(2)
        return

    def get_loaded_lecture_url(self):
        lectures = self.page.locator(selector="#lectList > tr").all()
        for lecture in lectures:
            lecture_href: str = lecture.locator("td.al.ptb15 > div.title > a").get_attribute("href")
            self.lectureHrefs.append(f"https://sacademy.shinsegae.com{lecture_href}")
        return

    def extract_lecture_info(self, url: str, page: Page, info: dict):
        page.goto(url, timeout=0)
        time.sleep(2)

        lecture: LectureType = LectureType()
        lecture.url = page.url
        lecture.address = info.get("address")
        lecture.branch = info.get("branch")
        lecture.region = info.get("region")
        lecture.crawlerIndex = info.get("crawler_index")
        lecture.type = "백화점"
        lecture.center = "SHINSEGAE"

        lecture.title = page.inner_text(selector="#h2lectName")
        price_str: str = page.inner_text(selector="#inContent > div.wrap.mb70 > div.detail_form2 > table > tbody > tr:nth-child(12) > td > span")
        lecture.price = int(price_str.replace(",", ""))
        lecture.target = page.inner_text(selector="#inContent > div.wrap.mb70 > div.detail_form2 > table > tbody > tr:nth-child(5) > td")
        lecture.src = page.get_attribute(selector="#inContent > div.wrap.mb70 > div.detail_form1 > div.slider-for.mb10.slick-initialized.slick-slider > div > div > div > img", name="src")
        lecture.url = url

        lecture.content = page.inner_text(selector="#tab1 > ul:nth-child(3) > p")
        supplies: str = page.inner_text(selector="#tab1 > ul:nth-child(7)")
        if re.search(r"등록된\s?준비물이\s?없습니다", supplies) is None:
            lecture.lectureSupplies = supplies

        start_text: str = page.inner_text(selector="#inContent > div.wrap.mb70 > div.detail_form2 > table > tbody > tr:nth-child(3) > td > p")
        start_split: list[str] = start_text.split("(총 ")
        start_span: list[str] = re.split(r"\s?[~-]\s?", start_split[0])
        lecture_num: int = int(start_split[1].replace("회)", ""))

        enroll_span: list[str] = re.split(r"\s?[~-]\s?", page.inner_text(selector="#inContent > div.wrap.mb70 > div.detail_form2 > table > tbody > tr:nth-child(9) > td"))
        lecture.enrollStart = enroll_span[0].replace(".", "-")
        lecture.enrollEnd = enroll_span[1].replace(".", "-")

        detail_time: str = page.inner_text(selector="#inContent > div.wrap.mb70 > div.detail_form2 > table > tbody > tr:nth-child(4) > td > p")
        lecture.set_lecture_held_dates(start_span, detail_time, lecture_num)

        curriculums = page.locator(selector="#tab1 > table > tbody > tr").all()
        if len(curriculums) > 0:
            curriculum_dict: dict = {}
            for curriculum in curriculums:
                if curriculums.index(curriculum) >= lecture_num:
                    break
                curriculum_text: str = curriculum.locator("td.al").inner_text()
                if len(curriculum_text) > 3:
                    curriculum_dict[f"{curriculums.index(curriculum) + 1} 회차"] = curriculum_text
            lecture.set_curriculum(curriculum_dict)

        lecture.classId = ClassIdInfos.make_class_id(lecture)

        yield lecture

        return









