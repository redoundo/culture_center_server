import math
import re
import time
import datetime
from crawl.typeclass.LectureType import LectureType
from crawl.crawler.crawlerabstract import NoLinkCrawler
from crawl.typeclass.ClassIdInfoType import ClassIdInfos
from playwright.sync_api import Page


class EmartCrawler(NoLinkCrawler):

    def crawl(self):
        self.search_option_setting()

        self.check_lecture_total()
        self.load_more()

        self.get_loaded_lecture_url()
        return

    def search_option_setting(self) -> None:
        self.page.goto(self.url, timeout=0)
        self.page.reload(timeout=5000)
        region_index: int = self.centerInfo.get_region_index()
        branch_index: int = self.centerInfo.get_branch_index()

        self.page.click("#container > div > div.filter.active > div.filter-wrap > div.ft-tab > ul >\
                 li:nth-child(1) > a", timeout=50000, delay=20)
        self.page.click(f"#container > div > div.filter.active > div.filter-wrap > div.ft-cont >\
                 div.ft-branch.active > ul > li:nth-child({region_index + 1}) > div.ft-accor-title > a",
                        timeout=50000, delay=30)
        if not self.page.is_visible("#container > div > div.filter.active > div.filter-wrap > div.ft-cont >\
                 div.ft-branch.active > ul > li.ft-accor-item.active > div.ft-accor-cont.scroll > ul >\
                  li:nth-child(1) > label", timeout=60000):
            self.page.click(f"#container > div > div.filter.active > div.filter-wrap > div.ft-cont >\
                             div.ft-branch.active > ul > li:nth-child({region_index + 1}) > div.ft-accor-title > a",
                            timeout=50000, delay=30)
        self.page.click(f"#container > div > div.filter.active > div.filter-wrap > div.ft-cont >\
                 div.ft-branch.active > ul > li.ft-accor-item.active > div.ft-accor-cont.scroll > ul >\
                  li:nth-child({branch_index + 1}) > label", timeout=50000, delay=200)

        self.page.click(
            "#container > div > div.filter.active > div.filter-wrap > div.ft-tab > ul > li:nth-child(4) > a",
            timeout=50000, delay=50)
        if not self.page.is_visible("#container > div > div.filter.active > div.filter-wrap > div.ft-cont >\
                 div.ft-detail.active > ul > li:nth-child(2) > div.ft-accor-title > a", timeout=60000):
            self.page.click(
                "#container > div > div.filter.active > div.filter-wrap > div.ft-tab > ul > li:nth-child(4) > a",
                timeout=50000, delay=20)
        self.page.click("#container > div > div.filter.active > div.filter-wrap > div.ft-cont >\
                 div.ft-detail.active > ul > li:nth-child(2) > div.ft-accor-title > a", timeout=50000, delay=20)

        if not self.page.is_visible("#container > div > div.filter.active > div.filter-wrap > div.ft-cont >\
                 div.ft-detail.active > ul > li.ft-accor-item.active > div.ft-accor-cont.scroll > ul > li:nth-child(2) > label",
                                    timeout=60000):
            self.page.click("#container > div > div.filter.active > div.filter-wrap > div.ft-cont >\
                             div.ft-detail.active > ul > li:nth-child(2) > div.ft-accor-title > a", timeout=50000,
                            delay=20)
        self.page.click("#container > div > div.filter.active > div.filter-wrap > div.ft-cont >\
                 div.ft-detail.active > ul > li.ft-accor-item.active > div.ft-accor-cont.scroll > ul > li:nth-child(2) > label",
                        timeout=50000, delay=20)
        return

    def load_more(self):
        if self.total < 0 and self.pageCount < 0:
            return
        else:
            for _ in range(0, self.pageCount):
                self.page.evaluate("() => window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(10)
        return

    def check_lecture_total(self):
        total_str: str = self.page.inner_text("#container > div > div.sort > div.sort-total > em", timeout=60000)
        if int(total_str) == 0:
            return
        else:
            self.total = int(total_str)
            self.pageCount = math.ceil(self.total / 20)
        return

    def get_loaded_lecture_url(self):
        all_lectures = self.page.locator("#container > div > ul > li").all()
        for lecture in all_lectures:
            href: str = lecture.locator("div.cls-item-in > div.cls-txt > div.cls-title > a").get_attribute("href")
            if href is not None:
                self.lectureHrefs.append("https://www.cultureclub.emart.com" + href)
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
        lecture.center = "EMART"
        lecture.type = "대형마트"

        lecture.category = page.inner_text("#container > div > div.clsdtl-info > div.clsdtl-txt > div.clsdtl-cate",
                                           timeout=6000)
        lecture.title = page.inner_text("#container > div > div.clsdtl-info > div.clsdtl-txt > h1", timeout=6000)
        prices: str = page.inner_text(
            "#container > div > div.clsdtl-info > div.clsdtl-txt > div.clsdtl-price > dl > dd > strong", timeout=6000)
        lecture.price = int(prices.replace(",", ""))
        # lecture.branch = self.page.inner_text("#container > div > div.clsdtl-info >\
        #  div.clsdtl-txt > dl > dd:nth-child(4)")
        lecture.src = page.get_attribute("#container > div > div.clsdtl-info > div.clsdtl-vis > img", "src",
                                         timeout=6000)

        if lecture.category in ["Club Originals"]:
            lecture.target = "Club Originals 클럽 오리지널"
        elif lecture.category in ["Arts", "Language", "Economy", "Beauty & Design", "Dance & Exercise", "Music & Play",
                                  "Drawing", "Crafts", "Pet"]:
            lecture.target = "Culture Club 성인"
        elif lecture.category in ["Parents education", "With Mom", "With mom(event)", "Kids & Children",
                                  "Kids & Children(event)", "Pre-Parent"]:
            lecture.target = "Little Club 자녀"
        else:
            lecture.target = "Cooking Club 쿠킹"

        # 이마트 강의 일정 형식 : 월 14:00-15:00 (05.27-06.03) 2회
        lecture_count_span: list[str] = page.inner_text(
            "#container > div > div.clsdtl-info > div.clsdtl-txt > dl > dd:nth-child(2)", timeout=6000).split(
            " (")  # 05.27-06.03) 2회
        lecture_raw_span: list[str] = lecture_count_span[1].split(") ")  # ['05.27-06.03', '2회']
        lecture_count: int = int(lecture_raw_span[1].replace("회", ""))  # 2

        lecture_spans: list[str] = lecture_raw_span[0].split("-")  # 05.27 | 06.03
        lecture_start_split_date: list[str] = lecture_spans[0].split(".")  # [05, 27]
        lecture_end_split_date: list[str] = lecture_spans[1].split(".")  # [06, 03]

        now: datetime = datetime.datetime.now()
        # 2024-05-27
        lecture_full_start_date: str = f"{str(now.year)}-{lecture_start_split_date[0]}-{lecture_start_split_date[1]}"
        # 2024-06-03
        lecture_full_end_date: str = f"{str(now.year)}-{lecture_end_split_date[0]}-{lecture_end_split_date[1]}"
        # 2024-05-27!2024-06-03
        lecture.set_lecture_held_dates([lecture_full_start_date, lecture_full_end_date],
                                       lecture_count_span[0], lecture_count)

        contents = page.locator("#clsdtl-intro > div").all()
        for content in contents:
            content_class: str = content.get_attribute("class")
            if content_class not in ["g-head-3", "g-head-4"]:
                continue
            if content_class == "g-head-4":
                content_title: str = content.locator("h3").inner_text()
            else:
                content_title: str = content.locator("h2").inner_text()
            content_index: int = contents.index(content) + 2
            if content_title == "이런 걸 배울 거예요":
                curriculum_dict: dict = {}
                curriculums = page.locator(f"#clsdtl-intro > div:nth-child({content_index}) > div").all()
                for curriculum in curriculums:
                    # 커리큘럼 외의 내용을 적어놓는 경우가 있는데 이를 저장하는 걸 방지.
                    if lecture_count < curriculums.index(curriculum):
                        break
                    curriculum_text = curriculum.locator("div:nth-child(1) > b > h3").inner_text(timeout=6000)

                    escape_single_quote = re.sub(r"'", "''", curriculum_text)
                    escape_double_quote = re.sub(r'"', '\\"', escape_single_quote)

                    curriculum_count = curriculum.locator("div:nth-child(1) > b > h3 > span").inner_text(timeout=6000)
                    curriculum_replace_text: str = escape_double_quote.replace(curriculum_count, "")
                    if len(curriculum_replace_text) > 3:
                        curriculum_dict[curriculums.index(curriculum)] = curriculum_replace_text
                lecture.set_curriculum(curriculum_dict)  # json.dumps 처리 후 저장.

            elif content_title == "클래스 상세정보":
                lecture_contents = page.locator(
                    f"#clsdtl-intro > div:nth-child({content_index}) > div > p > span").all()
                content_list: list[str] = []
                for lecture_content in lecture_contents:
                    content_text: str = lecture_content.inner_text()
                    if content_text is None:
                        continue
                    elif re.search(r"※\s?문화\s?센터\s?변경\s?및\s?취소\s?규정\s?안내\s?※|\[엄마랑 아가랑 정규강좌 및 특강안내]|\s?ex\)아이\s?1인\s?55,000원\s?\+\s?보호자\s?1인\s?55,000원\s?=\s?총\s?110,000원\s?\(2인\s?결제\)\s?|◇정규\s?강좌\s?등록시|<특강\s?강좌\s?규정\s?안내>", content_text) is not None:
                        break
                    else:
                        if len(content_text) > 3:
                            content_list.append(content_text)

                joined_content: str = " \n ".join(content_list)
                lecture.content = joined_content
            else:
                continue

        supplies = page.locator("#clsdtl-intro > table > tbody > tr").all()
        if len(supplies) > 1:
            lecture.lectureSupplies = page.inner_text("#clsdtl-intro > table > tbody > tr:nth-child(2) > td",
                                                      timeout=6000)

        lecture.classId = ClassIdInfos.make_class_id(lecture)
        yield lecture

        self.lectureInfos.append(lecture)
        return

