from crawler.crawlerabstract import WithLinkCrawler
from typeclass.LectureType import LectureType
from typeclass.ClassIdInfoType import ClassIdInfos
import time
import re
from playwright.sync_api import Page


class LotteCrawler(WithLinkCrawler):

    def crawl(self):
        self.goto_page(self.centerInfo.get_link())
        self.load_more()
        self.get_loaded_lecture_url()
        return

    def goto_page(self, url: str) -> None:
        self.page.goto(url, timeout=0)
        total: int = int(self.page.inner_text("#totCnt", timeout=60000).replace("개", ""))
        if total == 0:
            return
        else:
            self.total = total
            self.pageCount = int(total / 20)
        return

    def load_more(self):
        if self.pageCount < 0:
            return
        else:
            for _ in range(0, self.pageCount):
                self.page.click("#moreBtn > a", timeout=50000, delay=20)
                time.sleep(10)
        return

    def get_loaded_lecture_url(self):
        if self.total < 0:
            return
        else:
            all_hrefs = self.page.locator("#listContainer > div").all()
            for href in all_hrefs:
                lecture_href: str = href.locator("a").get_attribute("href", timeout=60000)
                if lecture_href is not None:
                    self.lectureHrefs.append("https://culture.lotteshopping.com" + lecture_href)
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
        lecture.target = info.get("target")
        lecture.crawlerIndex = info.get("crawler_index")
        lecture.type = "백화점"
        lecture.center = "LOTTE"
        #
        lecture.src = page.get_attribute(
            "#wrap > div.cont_wrap > div > div.page_cont_area.no_padding > div.bg_inner.pd_bot > div > div > div.fixed_content_area > div > div.shadow_div > div:nth-child(1) > div.pop_wrap > div > div.for_padding > div > div.pop_head > div.tit_box > p > img",
            "src", timeout=6000)
        titles = page.locator(
            "#wrap > div.cont_wrap > div > div.page_cont_area.no_padding > div.bg_inner.pd_bot > div > div > div.fixed_content_area > div > div.shadow_div > div:nth-child(1) > div.pop_wrap > div > div.for_padding > div > div.pop_head > div.tit_box > div > p").all()
        if len(titles) > 1:
            main_title = page.inner_text(
                "#wrap > div.cont_wrap > div > div.page_cont_area.no_padding > div.bg_inner.pd_bot > div > div > div.fixed_content_area > div > div.shadow_div > div:nth-child(1) > div.pop_wrap > div > div.for_padding > div > div.pop_head > div.tit_box > div > p.tit.lectNm",
                timeout=6000)
            sub_title = page.inner_text(
                "#wrap > div.cont_wrap > div > div.page_cont_area.no_padding > div.bg_inner.pd_bot > div > div > div.fixed_content_area > div > div.shadow_div > div:nth-child(1) > div.pop_wrap > div > div.for_padding > div > div.pop_head > div.tit_box > div > p.desc.lectExpl",
                timeout=6000)
            lecture.title = main_title + " \n " + sub_title
        else:
            lecture.title = page.inner_text(
                "#wrap > div.cont_wrap > div > div.page_cont_area.no_padding > div.bg_inner.pd_bot > div > div > div.fixed_content_area > div > div.shadow_div > div:nth-child(1) > div.pop_wrap > div > div.for_padding > div > div.pop_head > div.tit_box > div > p.tit.lectNm",
                timeout=6000)

        # lecture.branch = self.page.inner_text("#wrap > div.cont_wrap > div > div.page_cont_area.no_padding >\
        #  div.bg_inner.pd_bot > div > div > div.pin-spacer > div > div > div.shadow_div > div:nth-child(1) >\
        #   div.pop_wrap > div > div.for_padding.on > div > div.box_con > div > div > div > div > dl:nth-child(1) > dd")

        lecture_spans: list[str] = (page.inner_text(
            "#wrap > div.cont_wrap > div > div.page_cont_area.no_padding > div.bg_inner.pd_bot > div > div > div.fixed_content_area > div > div.shadow_div > div:nth-child(1) > div.pop_wrap > div > div.for_padding > div > div.box_con > div > div > div > div > dl:nth-child(5) > dd",
            timeout=6000).split("~"))
        lecture_spans[0] = lecture_spans[0].replace(".", "-").replace(" ", "")
        lecture_spans[1] = lecture_spans[1].replace(".", "-").replace(" ", "")
        lecture_date_detail: str = page.inner_text(
            "#wrap > div.cont_wrap > div > div.page_cont_area.no_padding > div.bg_inner.pd_bot > div > div > div.fixed_content_area > div > div.shadow_div > div:nth-child(1) > div.pop_wrap > div > div.for_padding > div > div.box_con > div > div > div > div > dl:nth-child(6) > dd > p",
            timeout=6000)
        lecture_count: str = page.inner_text(
            "#wrap > div.cont_wrap > div > div.page_cont_area.no_padding > div.bg_inner.pd_bot > div > div > div.fixed_content_area > div > div.shadow_div > div:nth-child(1) > div.pop_wrap > div > div.for_padding > div > div.box_con > div > div > div > div > dl:nth-child(7) > dd",
            timeout=6000)
        lecture.set_lecture_held_dates(lecture_spans, lecture_date_detail, int(lecture_count.split("회")[0]))

        enroll_dates: list[str] = page.inner_text(
            "#wrap > div.cont_wrap > div > div.page_cont_area.no_padding > div.bg_inner.pd_bot > div > div > div.pin-spacer > div > div > div.shadow_div > div:nth-child(1) > div.pop_wrap > div > div.for_padding.on > div > div.box_con > div > div > div > div > dl:nth-child(11) > dd",
            timeout=6000).split("~")
        lecture.enrollStart = enroll_dates[0].replace(".", "-").replace(" ", "")
        lecture.enrollEnd = enroll_dates[1].replace(".", "-").replace(" ", "")

        lecture_locators = page.locator("#wrap > div.cont_wrap > div > div.page_cont_area.no_padding >\
         div.bg_inner.pd_bot > div > div > div.flow_txt_area > div.anchor_con.info_img_inner > div.info_img_txt > div").all()
        if len(lecture_locators) > 1:
            content_list: list[str] = []
            for locator in lecture_locators:
                locator_text: str = locator.inner_text(timeout=6000)
                if len(locator_text) > 3:
                    content_list.append(locator_text)
            lecture.content = " \n  ".join(content_list)
        else:
            lecture.content = page.inner_text("#wrap > div.cont_wrap > div > div.page_cont_area.no_padding >\
         div.bg_inner.pd_bot > div > div > div.flow_txt_area > div.anchor_con.info_img_inner > div.info_img_txt > div",
                                              timeout=6000)

        curriculum_count: int = int(lecture_count.split("회")[0])
        curriculum_locator = page.locator(
            "#wrap > div.cont_wrap > div > div.page_cont_area.no_padding > div.bg_inner.pd_bot > div > div > div.flow_txt_area > div.anchor_con.info_img_inner > div.mobile_acco_div.open > div > div").all()
        curriculum_dict: dict = {}
        for locator in curriculum_locator:
            locator_text = locator.locator("a > div > p").inner_text(timeout=6000)
            if "강의일정" in locator_text:
                curriculums = locator.locator("div > div").all()
                for curriculum in curriculums:
                    if curriculums.index(curriculum) < curriculum_count:
                        curriculum_date: str = curriculum.locator("p.date.f_body2").inner_text(timeout=6000)

                        curriculum_info: str = curriculum.locator("p.txt.f_body2").inner_text(timeout=6000)
                        curriculum_text = re.sub(r"'", "''", curriculum_info)
                        curriculum_sub = re.sub(r'"', '\\"', curriculum_text)

                        if len(curriculum_sub) > 3:
                            curriculum_dict[curriculums.index(curriculum)] = curriculum_date + "  " + curriculum_sub
                    else:
                        break
            elif "준비물/특이사항" in locator_text:
                supplies = locator.locator("div > div > p").all()
                supply_list: list[str] = []
                for supply in supplies:
                    supply_text: str = supply.inner_text()
                    if len(supply_text) > 3:
                        supply_list.append(supply_text)
                    else:
                        continue
                if len(supply_list) > 1:
                    lecture.lectureSupplies = " \n ".join(supply_list)
            else:
                break
        lecture.set_curriculum(curriculum_dict)
        lecture.classId = ClassIdInfos.make_class_id(lecture)

        yield lecture

        self.lectureInfos.append(lecture)
        return


