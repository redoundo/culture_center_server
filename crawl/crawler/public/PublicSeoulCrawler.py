from crawl.crawler.crawlerabstract import PublicCenterCrawler
from crawl.typeclass.PublicLibrary import PublicLibrary
from crawl.typeclass.LectureType import LectureType
from playwright.sync_api import Page, Locator, Browser
import re
from datetime import datetime
import time
from crawl.crawler.utils.utils import validate_string, trim_lecture_time, trim_lecture_price


class PublicSeoulCrawler(PublicCenterCrawler):

    def crawl(self):
        return

    def __ever_learning(self, center_info: PublicLibrary):
        page: Page = self.browser.new_page()
        url: str = center_info.get_link()
        page.goto(url, timeout=0)

        time.sleep(2)

        lecture_count: str = (page.inner_text("#contentcore > div.contentArea > div.pagingWrap > p")
                              .replace("총 ", "").replace("건", ""))
        if int(lecture_count) < 1:
            return

        page_count: int = int(
            page.inner_text("#contentcore > div.contentArea > div.pagingWrap > div > a.btn-paging.last")
            .replace("javascript:fnList(", "").replace(");", ""))
        lecture_href: list[str] = []
        current_page: int = 1

        for p in range(0, page_count):
            locators = page.locator("#contentcore > div.contentArea > div.boardWrap > table > tbody > tr").all()
            for locator in locators:
                lecture_id: str = (locator.locator("td.list-title > div > a").get_attribute("onclick")
                                   .replace("fnDetail('", "").replace("');", ""))
                lecture_href.append(f"https://everlearning.sen.go.kr/ever/menu/10010/program/30002/lectureDetail.do?currentPageNo={p + 1}&searchCondition=title&searchYmdCondition=applyYmd&lectureId={lecture_id}&searchType=LECTURE&searchStatusCd=ONABLE&searchOrganNm=&searchSigungu=ALL&searchTarget=&searchDayOfWeek=&searchDayStartTm=&searchPay=ALL")
            if len(locators) < 10 or current_page > page_count:
                break  # 페이지 이동 실행 X
            else:
                page_nums = page.locator("#contentcore > div.contentArea > div.pagingWrap > div > a").all()
                for page_num in page_nums:
                    num_text: str = page_num.get_attribute("href").replace("javascript:fnList(", "").replace(");", "")
                    if int(num_text) == current_page + 1:
                        page_num.click()
                        current_page += 1
                        time.sleep(2)
                        break
                    else:
                        continue
        page.close()

        return

    def __national_lib_ko(self, center_info: PublicLibrary):
        page: Page = self.browser.new_page()
        page.goto(center_info.get_link(), timeout=0)
        time.sleep(2)

        lecture_count: int = int(page.inner_text("#listForm > div.search_wrap > div > div.result_info > span.total_num"))

        if lecture_count < 1:
            return

        page_count: int = (lecture_count // 100) + 1  # 전체 페이지 수
        lecture_hrefs: list[str] = []
        for count in range(0, page_count):
            lectures = page.locator("#sub_content > div.content_wrap > div > div > div.ucreq7_wrap > ul > li").all()
            for lecture in lectures:
                is_ing: str = lecture.locator("div > div.ucreq7_cell.ucreq7_cell_color > span").inner_text()
                if is_ing == "신청가능":
                    lecture_id: str = (lecture.locator("div > div:nth-child(2) > h4 > a").get_attribute("href")
                                       .replace("fn_goView('", "").replace("');", ""))
                    lecture_hrefs.append(f"https://www.nl.go.kr/NL/contents/N30901000000.do?viewCount=100&ordBy=desc&libraryEducationId={lecture_id}&schM=view")
                else:
                    break
            if page_count - 1 > count:
                page.click("#sub_content > div.content_wrap > div > div > div:nth-child(5) > div > a.sp.sp_next")
                time.sleep(2)
        page.close()
        return

    def __busan_pen_edu(self, center_info: PublicLibrary):
        page: Page = self.browser.new_page()
        page.goto(center_info.get_link(), timeout=0)
        time.sleep(2)

        lecture_count: int = int(page.inner_text("#srchForm > div.rvelstOpt.brdForm.mgt40 > div > span"))
        page_count: int = lecture_count // 50 + 1
        lecture_href: list[str] = []
        for count in range(0, page_count):
            lecture_id: str = page.get_attribute("#cntntsView > div.rvelst.mgt10.tbl_st > table > tbody > tr:nth-child(1) > td.al > p.pc_blue > a", "data-id")
            lecture_href.append(f"https://home.pen.go.kr/yeyak/edu/lib/selectEduInfo.do?mi=14556&eduSeq={lecture_id}&srchRsSysId=&srchEduCtgry=&currPage={count + 1}&srchRsvSttus=REQST&srchPeriodDiv=rcept&srchRsvBgnde=&srchRsvEndde=&srchRsvValue=&pageIndex=50")

            if page_count - 1 > count:
                page.click("#cntntsView > form:nth-child(5) > div > ul > li.page-next > a")
                time.sleep(2)
        page.close()
        return

    def __ulsan_donggu(self, center_info: PublicLibrary):
        page: Page = self.browser.new_page()
        page.goto(center_info.get_link(), timeout=0)
        time.sleep(2)

        lecture_count: int = int(page.inner_text("#board > div.board_total > div.board_total_left > strong"))
        if lecture_count < 1:
            return
        month: int = datetime.now().month
        date: int = datetime.now().day
        return

    def __ice_edu_lib(self, center_info: PublicLibrary):
        """
        인천 광역시 교육청 통합 공공 도서관
        :param center_info:
        :return:
        """
        page: Page = self.browser.new_page()
        page.goto(center_info.get_link(), timeout=0)
        time.sleep(2)

        pagination = page.locator("#board_paging > span > a").all()
        lecture_href: list[str] = []
        for num in pagination:
            num.click()
            time.sleep(2)
            lectures = page.locator("#teach > div.op_wrap > div > div").all()
            for lecture in lectures:
                homepage_id: str = lecture.locator("div.op_title.category > a").get_attribute("keyvalue")
                group_idx: str = lecture.locator("div.op_title.category > a").get_attribute("keyvalue1")
                category_idx: str = lecture.locator("div.op_title.category > a").get_attribute("keyvalue2")
                teach_idx: str = lecture.locator("div.op_title.category > a").get_attribute("keyvalue3")
                lecture_href.append(f"https://lib.ice.go.kr/ice/module/teach/detail.do?homepage_id={homepage_id}&group_idx={group_idx}&category_idx={category_idx}&teach_idx={teach_idx}&menu_idx=92")
        page.close()
        return

    def __jbe_edu_lib(self, center_info: PublicLibrary):
        """
        전북특별자치도교육청통합도서관/교육문화회관
        :param center_info:
        :return:
        """
        page: Page = self.browser.new_page()
        page.goto(center_info.get_link(), timeout=0)
        time.sleep(2)

        pagination = page.locator("#board_paging > span > a").all()
        lecture_href: list[str] = []

        for num in pagination:
            num.click()
            time.sleep(2)
            lectures = page.locator("#teach > div.op_wrap > div > div").all()
            for lecture in lectures:
                homepage_id: str = lecture.locator("div.op_title.category > a").get_attribute("keyvalue")
                group_idx: str = lecture.locator("div.op_title.category > a").get_attribute("keyvalue1")
                category_idx: str = lecture.locator("div.op_title.category > a").get_attribute("keyvalue2")
                teach_idx: str = lecture.locator("div.op_title.category > a").get_attribute("keyvalue3")
                detail_menu_idx: str = lecture.locator("div.op_title.category > a").get_attribute("keyvalue4")
                lecture_href.append(f"https://lib.jbe.go.kr/jbe/module/teach/detail.do?homepage_id={homepage_id}&group_idx={group_idx}&category_idx={category_idx}&teach_idx={teach_idx}&menu_idx=17&detail_menu_idx={detail_menu_idx}")
        page.close()
        return

    def __gwangju_seogu_edu_lib(self, center_info: PublicLibrary):
        page: Page = self.browser.new_page()
        page.goto(center_info.get_link(), timeout=0)
        time.sleep(2)

        pagination = page.locator("#board_paging > span > a").all()
        lecture_href: list[str] = []
        for num in pagination:
            num.click()
            time.sleep(2)
            lectures = page.locator("#content > table > tbody > tr").all()
            for lecture in lectures:
                status: str = lecture.locator("td:nth-child(7) > span").inner_text()
                if status == "접수중":
                    cul_edu_id: str = lecture.locator("td.title > a").get_attribute("href").replace("javascript:cultureEduInfoView('", "").replace("')", "")
                    lecture_href.append(f"https://library.seogu.gwangju.kr/library/index.9is?contentUid=9be5df89604f89ac01604fa17b160145&culEduId={cul_edu_id}")
        return





