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


class AkplazaCrawler(NoLinkCrawler):

    currentPage: int

    def __init__(self, url: str, center_info: CenterInfoNoLink, page: Page):
        super().__init__(url, center_info, page)
        self.currentPage = 0
        return

    def crawl(self):
        self.search_option_setting()
        self.check_lecture_total()
        return

    def search_option_setting(self) -> None:
        self.page.goto(self.url, timeout=0)

        # 지점을 바꾸기 위해 점포 선택/ my 아카데미 버튼 클릭
        self.page.click("#header > div.header-wr.table > div.nav-r > ul > li > a", timeout=3000, delay=2000)
        # 지점을 바꾸는 사이드 바가 열렸다면 class 이름에 active 를 포함 한다.
        setting_branch = self.page.get_attribute("#header > div:nth-child(4)", "class", timeout=6000)
        time.sleep(10)
        if setting_branch is None or "active" not in setting_branch:
            self.page.click("#header > div.header-wr.table > div.nav-r > ul > li > a", timeout=3000, delay=2000)
            time.sleep(10)
        # 지점을 바꾸는 select 클릭
        self.page.click("#header > div.myaca-wrap.active > div.aca-wr > div > div > div > div", timeout=300, delay=20)
        # 지점들이 다 보이는지 확인. class 가 select-box select-box-no on 이여야 함.
        open_branch = self.page.get_attribute("#header > div.myaca-wrap.active > div.aca-wr >\
         div > div > div > div", "class", timeout=6000)
        if open_branch is None or open_branch == "select-box select-box-no":
            self.page.click("#header > div.myaca-wrap.active > div.aca-wr > div > div > div > div", timeout=300, delay=20)
        # 지점 클릭
        self.page.click(f"#header > div.myaca-wrap.active > div.aca-wr > div > div >\
         div > div > ul > li:nth-child({self.centerInfo.get_branch_index() + 1})", timeout=3000, delay=20)

        return

    def load_more(self):
        pagination = self.page.locator("body > div.all-wrap > div.cours-sec.cours-sec01.bg-gray >\
         div > div.paging > ul > li").all()

        for page in pagination:
            page_index_str = page.locator("a").get_attribute("onclick", timeout=6000)
            if page_index_str is not None:
                pag_index: int = int(page_index_str.replace("javascript:pageMoveAjax(", "").replace(");", ""))
                if pag_index == self.currentPage + 1:
                    page.locator("a").click(timeout=5000, delay=20)
                    self.currentPage = pag_index
                    time.sleep(4)
                    break
                else:
                    continue
            else:
                break
        return

    def check_lecture_total(self):

        while self.check_lecture_status() == 9:
            self.get_loaded_lecture_url()
            self.load_more()

        rest_of_page: int = self.check_lecture_status()  # 페이지 확인이 끝난 마지막 장에 남은 접수 가능 , 마감 임박 이 들어간 강의의 개수
        total_page: int = copy.copy(self.currentPage)  # 현재 페이지 초기화를 위한 값 보존.

        if rest_of_page > 1:
            self.get_loaded_lecture_url()

        self.pageCount = total_page
        # 강좌 개수가 9개 보다 작은 마지막 장은 total_page 로 가지 않고 rest_of_page 로 취급
        self.total = (total_page - 1) * 9 + rest_of_page

        self.currentPage = 0  # 현재 페이지 초기화
        self.page.reload(timeout=3000)  # 새로고침을 하면 화면 내용이 1 페이지로 초기화 된다.
        return

    def check_lecture_status(self) -> int:
        lectures = self.page.locator("#list_target > tr").all()
        ing: int = 0
        for lecture in lectures:
            status = lecture.locator("td:nth-child(10)").inner_text(timeout=6000)
            if status not in ["접수가능", "마감임박"]:
                break
            else:
                ing += 1
        return ing

    def get_loaded_lecture_url(self):
        lectures = self.page.locator("#list_target > tr").all()

        for lecture in lectures:
            href = lecture.get_attribute("onclick", timeout=6000)
            if href is not None:
                lecture_href: str = href.split("','")[1].replace("')", "")
                self.lectureHrefs.append(f"https://culture.akplaza.com{lecture_href}&expired=F")

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
        lecture.type = "백화점"
        lecture.center = "AKPLAZA"

        lecture.title = page.inner_text("#lect_nm", timeout=6000)
        lecture.target = page.inner_text("body > div.all-wrap > div.cours-sec.cours-sec01.bg-gray > div >\
         div > div.cour-detop.table > div > table > tbody > tr:nth-child(2) > td:nth-child(2)", timeout=6000)
        lecture.category = page.inner_text("body > div.all-wrap > div.cours-sec.cours-sec01.bg-gray > div >\
         div > div.cour-detop.table > div > table > tbody > tr:nth-child(2) > td:nth-child(4)", timeout=6000)
        price_text: str = page.inner_text("body > div.all-wrap > div.cours-sec.cours-sec01.bg-gray > div >\
         div > div.cour-detop.table > div > table > tbody > tr:nth-child(3) > td:nth-child(2)", timeout=6000)

        lecture.price = int(price_text.replace("원", "").replace(",", ""))
        lecture.content = page.inner_text("#lect_info")
        raw_lecture_curriculum = page.inner_text("#lect_info_area", timeout=6000)

        lecture_count: int = int(page.inner_text("#lect_cnt", timeout=6000).replace("회", ""))

        curriculums: list[str] = re.split(r"[0-9]{1,3}\s?회차\s?:\s?", raw_lecture_curriculum, 1)
        if len(curriculums) > 0:
            curriculum_dict: dict = {}
            for curriculum in curriculums:
                if len(curriculum) > 1 and curriculums.index(curriculum) <= lecture_count:

                    curriculum_text = re.sub(r"'", "''", curriculum)
                    curriculum_sub = re.sub(r"\n", "", curriculum_text)
                    text_sub = re.sub(r'"', '\\"', curriculum_sub)

                    curriculum_dict[curriculums.index(curriculum)] = re.sub(r"\n[0-9]{1,3}\s?회차", "", text_sub)
            lecture.set_curriculum(curriculum_dict)

        # akplaza 날짜 형식 03/15 - 05/31
        lecture_spans: list[str] = page.inner_text("#lect_schedule", timeout=6000).split(" - ")  # [03/15, 05/31]
        lecture_start_split_date: list[str] = lecture_spans[0].split("/")
        lecture_end_split_date: list[str] = lecture_spans[1].split("/")

        now: datetime = datetime.datetime.now(timezone("Asia/Seoul"))
        lecture_full_start_date: str = f"{str(now.year)}-{lecture_start_split_date[0]}-{lecture_start_split_date[1]}"
        lecture_full_end_date: str = f"{str(now.year)}-{lecture_end_split_date[0]}-{lecture_end_split_date[1]}"
        # 날짜 형식 조정 후 강의일 추출.
        lecture_date_detail = page.inner_text("body > div.all-wrap > div.cours-sec.cours-sec01.bg-gray > div >\
         div > div.cour-detop.table > div > table > tbody > tr:nth-child(1) > td:nth-child(4)")
        lecture.set_lecture_held_dates([lecture_full_start_date, lecture_full_end_date],
                                       lecture_date_detail, lecture_count)

        lecture.classId = ClassIdInfos.make_class_id(lecture)

        yield lecture

        self.lectureInfos.append(lecture)
        return