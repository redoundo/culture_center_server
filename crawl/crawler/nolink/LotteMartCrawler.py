from crawl.typeclass.CenterInfoNoLink import CenterInfoNoLink
from server.app.crawl.typeclass.LectureType import LectureType
from server.app.crawl.crawler.crawlerabstract import NoLinkCrawler
from server.app.crawl.typeclass.ClassIdInfoType import ClassIdInfos
import re
import time
import datetime
from playwright.sync_api import Page


class LotteMartCrawler(NoLinkCrawler):
    tagId: str
    currentPage: int

    def __init__(self, url: str, center_info: CenterInfoNoLink, page: Page):
        super().__init__(url, center_info, page)
        self.tagId = ""
        self.currentPage = -1
        return

    def crawl(self):
        self.search_option_setting()

        self.check_lecture_total()
        self.load_more()

        self.get_loaded_lecture_url()
        return

    def search_option_setting(self):
        self.page.goto(self.url, timeout=0)
        self.page.reload(timeout=50000)  # 새로 고침 으로 검색 조건 초기화

        region_index: int = self.centerInfo.get_region_index()
        branch_index: int = self.centerInfo.get_branch_index()

        self.page.click('#chooseStore', delay=200)  # 지점 선택 시작
        if not self.page.is_visible("#frm > div > ul > li:nth-child(1) > div > div.branch_find-wrap.branch_selc-wrap\
                 > div > ul > li", timeout=6000):  # 지역 선택을 위한 팝업이 떠야 진행 가능.
            self.page.click('#chooseStore', delay=200, timeout=4000)  # 지점 선택 버튼 다시 클릭
        else:
            pass

        self.page.click(f"#frm > div > ul > li:nth-child(1) > div > div.branch_find-wrap.branch_selc-wrap > div > ul > li:nth-child({region_index + 1})", delay=200, timeout=3000)  # 검색 지역 클릭

        # 검색할 지역 탭으로 전환 되어져 있는지 확인
        if not self.page.is_visible(f"#frm > div > ul > li:nth-child(1) > div > div.branch_find-wrap.branch_selc-wrap \
                > div > div:nth-child({region_index + 2}) > ul > li:nth-child({branch_index + 1}) > a", timeout=6000):
            self.page.click('#chooseStore', delay=200, timeout=4000)  # 지점 선택 버튼 다시 클릭
            self.page.click(f"#frm > div > ul > li:nth-child(1) > div > div.branch_find-wrap.branch_selc-wrap >\
                             div > ul > li:nth-child({region_index + 1})", delay=200, timeout=3000)  # 검색할 지역 다시 클릭
        else:
            pass

        self.tagId = self.page.get_attribute(f"#frm > div > ul > li:nth-child(1) > div > div.branch_find-wrap.branch_selc-wrap > div > div:nth-child({region_index + 2}) > ul > li:nth-child({branch_index + 1})", "tagid", timeout=60000)  # 강의 링크 생성에 필요한 tagid 내용 가져 오기

        # lotte mart 는 지역과 지점이 같은 div 안에 있어서 지점을 설정 하려면 div:nth-child({region_index + 1})로 진행 해야함
        self.page.click(f"#frm > div > ul > li:nth-child(1) > div > div.branch_find-wrap.branch_selc-wrap \
                > div > div:nth-child({region_index + 2}) > ul > li:nth-child({branch_index + 1}) > a",
                        delay=200, timeout=5000)  # 검색할 지점 클릭.
        time.sleep(5)
        self.page.click("#frm > div > ul > li.li-srch > a", delay=20, timeout=5000)  # 검색 버튼 클릭

        return

    def load_more(self):
        count: int = 1
        while count <= self.pageCount:
            self.page.click("#contents > div.srch_rslt-box.tbl_list-area > div.btn_more-area.courseAdd > a", delay=20,
                            timeout=5000)
            time.sleep(10)
            count += 1
        return

    def check_lecture_total(self):
        self.page.click("#accepttotcnt > a", delay=20, timeout=5000)
        time.sleep(10)
        raw_total: str = self.page.inner_text("#accepttotcnt > a", timeout=5000)
        total = re.search(r"[0-9]{1,5}", raw_total)
        if total is not None:
            self.total = int(total.group())
            self.pageCount = int(self.total / 18)
        return

    def get_loaded_lecture_url(self):
        locators = self.page.locator("#course_data > tr").all()
        for locator in locators:
            param: str = locator.locator("td.align-l.dis-first > div.info-txt > a").get_attribute("onclick",
                                                                                                  timeout=6000)
            if param is None:
                param = self.page.get_attribute(f"#course_data > tr:nth-child({locators.index(locator)}) >\
                         td.align-l.dis-first > div.info-txt > a", "onclick", timeout=6000)
            else:
                pass
            query_string: str = param.replace("fn_clsView('", "").replace("')", "")
            lecture_href: str = f"https://culture.lottemart.com/cu/gus/course/courseinfo/courseview.do?search_list_type=&search_str_cd={self.tagId}&search_order_gbn=&search_reg_status=1&is_category_open=N&from_fg=&cls_cd={query_string}&fam_no=&wish_typ=&search_term_cd={query_string[0:6]}&search_day_fg=&search_cls_nm=&search_cat_cd=&search_opt_cd=&search_tit_cd="
            self.lectureHrefs.append(adjust_white_space(lecture_href))
        return

    def extract_lecture_info(self, url: str, page: Page, info: dict):
        page.goto(url, timeout=0)
        time.sleep(8)

        lecture: LectureType = LectureType()
        lecture.url = page.url
        lecture.address = info.get("address")
        lecture.branch = info.get("branch")
        lecture.region = info.get("region")
        lecture.crawlerIndex = info.get("crawler_index")
        lecture.type = "대형마트"
        lecture.center = "LOTTEMART"

        title: str = page.inner_text("#contents > div.lct_tit-area.mt30 > h2", timeout=6000)
        lecture.title = title

        src: str = page.get_attribute("#contents > div.lct_head-area.mt20 > div.lct-visual.left > img",
                                      "src", timeout=6000)
        lecture.src = src

        target: str = page.inner_text("#contents > div.lct_head-area.mt20 > div.tbl_view-area.right > div.view-table.th_align-l > table > tbody > tr:nth-child(2) > td:nth-child(4)", timeout=2000)

        category: str = page.inner_text("#contents > div.lct_tit-area.mt30 > span.lct-depth", timeout=6000)
        lecture.target = target
        lecture.category = category.replace(target, "").replace(" ", "")

        price_str: str = page.inner_text("#contents > div.lct_head-area.mt20 > div.tbl_view-area.right >\
         div.view-table.th_align-l > table > tbody > tr:nth-child(4) > td", timeout=6000)
        prices: list[str] = re.findall(r"[0-9,]+원", price_str)
        if len(prices) >= 1:
            price: int = int(prices[-1].replace("원", "").replace(",", "").replace(" ", ""))
            lecture.price = price
        else:
            lecture.price = 0

        lecture_span: list[str] = (page.inner_text("#contents > div.lct_head-area.mt20 > div.tbl_view-area.right > \
                div.view-table.th_align-l > table > tbody > tr:nth-child(2) > td:nth-child(2)", timeout=6000)
                                   .split("~", 1))
        lecture_span[0] = lecture_span[0].replace(" ", "").replace(".", "-")
        lecture_span[1] = lecture_span[1].replace(" ", "").replace(".", "-")
        lecture_date_detail: str = page.inner_text("#contents > div.lct_head-area.mt20 > div.tbl_view-area.right >\
         div.view-table.th_align-l > table > tbody > tr:nth-child(3) > td:nth-child(2)")
        lecture_count = re.search(r"[0-9]{1,3}\s?회", price_str)
        if lecture_count is not None:
            lecture.set_lecture_held_dates(lecture_span, lecture_date_detail,
                                           int(lecture_count.group().replace("회", "")))
        else:
            lecture.set_lecture_held_dates(lecture_span, lecture_date_detail, 1)

        supplies: str = page.inner_text("#contents > div.lct_head-area.mt20 > div.tbl_view-area.right >\
                 div.view-table.th_align-l > table > tbody > tr:nth-child(6) > td", timeout=6000)
        if len(supplies) > 0:
            lecture.lectureSupplies = supplies

        contents: str = page.inner_text("#lctInfo > table > tbody > tr:nth-child(2) > td", timeout=6000)
        if len(contents) > 0:
            lecture.content = contents

        check_no_curriculum = page.inner_text("#lctPlan", timeout=6000)
        if "강의계획서가 존재하지 않습니다." not in check_no_curriculum:
            curriculum = {}
            all_curriculum = page.locator("#lctPlan > table > tbody > tr").all()
            for locator in all_curriculum:
                curriculum_info: str = locator.locator("td.pd").inner_text(timeout=6000)
                if len(curriculum_info) > 3:
                    curriculum_text = re.sub(r"'", "''", curriculum_info)
                    text_curriculum = re.sub(r"'", "''", curriculum_text)
                    curriculum_sub = re.sub(r"\n", "", text_curriculum)
                    text_sub = re.sub(r'"', '\\"', curriculum_sub)

                    curriculum[all_curriculum.index(locator) + 1] = text_sub
            lecture.set_curriculum(curriculum)

        lecture.classId = ClassIdInfos.make_class_id(lecture)

        yield lecture

        self.lectureInfos.append(lecture)
        return
