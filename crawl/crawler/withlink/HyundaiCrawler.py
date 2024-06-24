import math
import re
import time

from typeclass.CenterInfoWithLink import CenterInfoWithLink
from crawler.crawlerabstract import WithLinkCrawler
from typeclass.LectureType import LectureType
from typeclass.ClassIdInfoType import ClassIdInfos
from playwright.sync_api import Page


class HyundaiCrawler(WithLinkCrawler):

    currentPage: int
    lectureCount: int

    def __init__(self, center_info: CenterInfoWithLink, page: Page):
        super().__init__(center_info, page)
        self.currentPage = -1
        self.lectureCount = 0
        return

    def crawl(self):
        self.goto_page(self.centerInfo.get_link())
        for _ in range(0, self.pageCount):
            self.get_loaded_lecture_url()
            if self.lectureCount < 36:
                break
            self.load_more()
        return

    def goto_page(self, url: str):
        self.page.goto(url, timeout=0)
        total: str = (self.page.inner_text("#applyForm > div.lec_wrap > div.top_option > div:nth-child(1) > span")
                      .replace("건", ""))
        if int(total) == 0:
            return
        else:
            self.total = int(total)
        self.pageCount = math.ceil(self.total/36)
        return

    def load_more(self):
        if self.pageCount == 1:
            return
        if self.currentPage == self.pageCount:
            return
        pagination = self.page.locator("#applyForm > div.lec_wrap > div.culture_list > div > div > div > a").all()
        for aPage in pagination:
            pagination_href: str = aPage.get_attribute("href")
            if pagination_href is not None and f"page={self.currentPage + 1}" in pagination_href:
                aPage.click(timeout=5000, delay=20)
                time.sleep(10)
                self.currentPage += 1
                break
            else:
                continue
        return

    def get_loaded_lecture_url(self):
        self.lectureCount = 0  # 만약 한 페이지에 있는 모든 강좌가 신청 가능 혹은 마감 임박인데 36개 미만일 경우 어떻게 처리 해야 하는지 정하지 않았다.
        loaded_list = self.page.locator("#applyForm > div.lec_wrap > div.culture_list > ul > li").all()
        for locator in loaded_list:
            lecture_status: str = locator.locator("a > div > span.state").inner_text()
            if lecture_status in ["신청가능", "마감임박"]:
                href: str = locator.locator("a").get_attribute("href")
                if "https://www.ehyundai.com" not in href:
                    self.lectureHrefs.append("https://www.ehyundai.com" + href)
                else:
                    self.lectureHrefs.append(href)
                self.lectureCount += 1
            else:
                break
        return

    def extract_lecture_info(self, url: str, page: Page, info: dict):
        page.goto(url, timeout=0)
        time.sleep(10)

        lecture: LectureType = LectureType()
        lecture.url = page.url
        lecture.address = info.get("address")
        lecture.branch = info.get("branch")
        lecture.region = info.get("region")
        lecture.category = info.get("category")
        lecture.crawlerIndex = info.get("crawler_index")
        lecture.center = "HYUNDAI"
        lecture.type = "백화점"

        lecture.title = page.inner_text("#contents > div > div > div > div.lecture_detail_wrap > h4", timeout=6000)
        lecture.url = page.url
        lecture.src = page.get_attribute("#contents > div > div > div > div.lecture_detail_wrap \
        > div.detail_info > div.pic > img", "src", timeout=6000)

        branch_name: str = page.inner_text("#contents > div > div > div > div.lecture_detail_wrap >\
         div.detail_info > div.info > div > table > tbody > tr:nth-child(1) > td:nth-child(4)", timeout=6000).split("(")[0]
        lecture.branch = branch_name

        price: str = page.inner_text("#contents > div > div > div > div.lecture_detail_wrap >\
         div.detail_info > div.info > div > table > tbody > tr:nth-child(4) > td:nth-child(4)", timeout=6000)
        lecture.price = int(price.replace("원", "").replace(",", ""))

        contents = page.locator("#contents > div > div > div > div.lecture_detail_wrap > div.detail_info >\
         div.info > div > table > tbody > tr:nth-child(5) > td > div > p").all()
        lecture_content: list[str] = []
        for content in contents:
            content_text: str = content.inner_text(timeout=6000)
            if re.search(r"준비물\s?[:-]\s?", content_text) is not None and len(content_text) > 3:
                lecture.lectureSupplies = content_text
            if re.search(r"취소\s?·\s?환불\s?규정|■\s?유의\s?사항|환불\s?·?\s?연기\s?불가", content_text) is not None:
                break
            else:
                if len(content_text) > 3:
                    lecture_content.append(content_text)
        if len(lecture_content) > 1:
            lecture.content = " \n ".join(lecture_content)

        lecture_count_str: str = page.inner_text("#contents > div > div > div > div.lecture_detail_wrap\
         > div.detail_info > div.info > div > table > tbody > tr:nth-child(4) > td:nth-child(2)", timeout=6000)
        lecture_count: int = int(lecture_count_str.replace("회", ""))

        lecture_spans: list[str] = (page.inner_text("#contents > div > div > div > div.lecture_detail_wrap > div.detail_info > div.info > div > table > tbody > tr:nth-child(3) > td", timeout=6000)
                                    .split("~", 1))
        lecture_spans[0] = lecture_spans[0].replace(".", "-")
        lecture_spans[1] = lecture_spans[1].replace(".", "-")
        lecture_date_detail: str = page.inner_text("#contents > div > div > div > div.lecture_detail_wrap > div.detail_info > div.info > div > table > tbody > tr:nth-child(2) > td")
        trim_lecture_date_detail: str = re.search(r"\(?\s?[월화수목금토일]\s?\)?\s?[0-9]{2}\s?:\s?[0-9]{2}\s?[-~]\s?[0-9]{2}\s?:\s?[0-9]{2}",
                                                  lecture_date_detail).group()
        lecture.set_lecture_held_dates(lecture_spans, trim_lecture_date_detail, lecture_count)

        curriculum_infos: dict = {}
        all_curriculums = page.locator("#tab01_1 > div.table_wrap.col > table > tbody > tr").all()
        for curriculum in all_curriculums:
            if all_curriculums.index(curriculum) > lecture_count:
                break
            else:
                curriculum_info: str = curriculum.locator("td.al_left").inner_text(timeout=6000)

                curriculum_text = re.sub(r"'", "''", curriculum_info)
                text_curriculum = re.sub(r'"', '\\"', curriculum_text)
                curriculum_sub = re.sub(r"\n", "", text_curriculum)

                curriculum_infos[all_curriculums.index(curriculum) + 1] = curriculum_sub
        lecture.set_curriculum(curriculum_infos)

        lecture.classId = ClassIdInfos.make_class_id(lecture)

        yield lecture

        self.lectureInfos.append(lecture)
        return

