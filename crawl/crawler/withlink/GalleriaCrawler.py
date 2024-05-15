import math
import time
import re

from crawl.typeclass.CenterInfoWithLink import CenterInfoWithLink
from crawl.crawler.crawlerabstract import WithLinkCrawler
from crawl.typeclass.LectureType import LectureType
from crawl.typeclass.ClassIdInfoType import ClassIdInfos
from playwright.sync_api import Page


class GalleriaCrawler(WithLinkCrawler):

    currentPage: int

    def __init__(self, center_info: CenterInfoWithLink, page: Page):
        super().__init__(center_info, page)
        self.currentPage = -1
        return

    def crawl(self):
        self.goto_page(self.centerInfo.get_link())
        for _ in range(0, self.pageCount):
            self.get_loaded_lecture_url()
            self.load_more()
        return

    def goto_page(self, url: str) -> None:
        self.page.goto(url, timeout=0)
        total: int = int(self.page.inner_text("#main > div > div.l-wrap.l-wrap--lg > div.tit > p > span > em"))
        if total == 0:
            return
        else:
            self.total = total
            self.pageCount = math.ceil(total / 12)
            self.currentPage = 0
        return

    def load_more(self):
        pagination_hrefs = self.page.locator("#main > div > div.l-wrap.l-wrap--lg > div.pagination > a").all()
        for href in pagination_hrefs:
            data_page: str = href.get_attribute("data-page")
            if data_page is not None and self.currentPage + 1 == int(data_page):
                href.click(timeout=50000, delay=20)
                time.sleep(10)
            else:
                continue
        return

    def get_loaded_lecture_url(self):
        loaded_lectures = self.page.locator("#main > div > div.l-wrap.l-wrap--lg > div.lecture-list > div").all()
        for lecture in loaded_lectures:
            href: str = lecture.locator("div.item-cont > a").get_attribute("href")
            if href is not None:
                self.lectureHrefs.append("https://dept.galleria.co.kr" + href)
            else:
                continue
        return

    def extract_lecture_info(self, url: str, page: Page, info: dict):
        page.goto(url, timeout=0)
        time.sleep(5)

        lecture: LectureType = LectureType()
        lecture.url = page.url
        lecture.address = info.get("address")
        lecture.branch = info.get("branch")
        lecture.region = info.get("region")
        lecture.category = info.get("category")
        lecture.crawlerIndex = info.get("crawler_index")
        lecture.center = "GALLERIA"
        lecture.type = "백화점"

        lecture.src = page.get_attribute("#main > div > section > div.article-pic-mb > img", "src", timeout=6000)
        lecture.title = page.inner_text("#main > div > section > div.article-side.article-side--gray > h1", timeout=6000)

        enroll_dates: list[str] = page.inner_text("#main > div > section >\
         div.article-side.article-side--gray > dl > dd:nth-child(4)", timeout=6000).split("~")
        lecture.enrollStart = enroll_dates[0].replace(".", "-").replace(" ", "")
        lecture.enrollEnd = enroll_dates[1].replace(".", "-").replace(" ", "")

        lecture_spans: list[str] = page.inner_text("#main > div > section > div.article-detail >\
         div > div.summary > div.summary-cont > dl > dd:nth-child(2)", timeout=6000).split("~")
        lecture_spans[0] = lecture_spans[0].replace(".", "-").replace(" ", "")
        lecture_spans[1] = lecture_spans[1].replace(".", "-").replace(" ", "")
        lecture_date_detail: str = page.inner_text("#main > div > section > div.article-detail > div > div.summary >\
         div.summary-cont > dl > dd:nth-child(4)")
        lecture_count = re.search(r"[0-9]{1,3}\s?회", lecture.title)
        if lecture_count is not None:
            lecture.set_lecture_held_dates(lecture_spans, lecture_date_detail,
                                           int(lecture_count.group().replace("회", "")))
        else:
            lecture.set_lecture_held_dates(lecture_spans, lecture_date_detail, 1)

        price_str: str = page.inner_text("#main > div > section > div.article-detail >\
         div > div.summary > div.summary-cont > dl > dd:nth-child(8) > b", timeout=6000)
        lecture.price = int(price_str.replace(",", ""))

        lecture.content = page.inner_text("#main > div > section > div.article-detail > div > div.detail > div > p", timeout=6000)

        lecture.classId = ClassIdInfos.make_class_id(lecture)

        yield lecture

        self.lectureInfos.append(lecture)
        return
