from bs4 import BeautifulSoup as bs
from crawl.typeclass.ClassIdInfoType import ClassIdInfos
import re
from urllib import request
from typeclass.PublicLibrary import PublicLibrary
from typeclass.LectureType import LectureType
from crawler.utils.utils import validate_string, trim_lecture_time, trim_lecture_price, trim_lecture_span_str, weekday_from_date_str


class PublicUrlCrawlerFactory:

    urlCrawler: dict

    def __init__(self):
        self.urlCrawler = {
            "__ever_learning": self.__ever_learning,
            "__national_lib_ko": self.__national_lib_ko,
            "__busan_pen_edu": self.__busan_pen_edu,
            "__tong_yeong_lib": self.__tong_yeong_lib,
            "__ice_edu_lib": self.__ice_edu_lib,
            "__gwangju_seogu_edu_lib": self.__gwangju_seogu_edu_lib
        }
        return

    def url_executor(self, crawler_name: str, **kwargs):
        """
        url crawler 이름을 넣으면(url 추출 크롤러와 이름 동일) 해당 이름의 크롤러 실행
        :param crawler_name: 크롤러의 이름
        :param kwargs: 크롤러를 실행 하는데 필요한 매개 변수들.
        :return:
        """
        return self.urlCrawler[crawler_name](kwargs)

    def __ever_learning(self, url: str, center_info: PublicLibrary):
        """
        에버러닝 강좌 내용 수집
        :param url:  내용을 수집할 url
        :param center_info: 에버러닝에서 연결 해주는 도서관의 address 를 찾기 위해 필요.
        :return:
        """
        with request.urlopen(url) as u:
            html = u.read().decode('utf-8')

        soup = bs(html, "html5lib")
        lecture: LectureType = LectureType()
        lecture.center = "에버러닝"
        lecture.url = url
        lecture.type = "공공기관"
        lecture.title = soup.select_one("#contentcore > div.contentArea > div.boardWrap > div > ul > li.title > div").get_text(strip=True)
        lecture.target = soup.select_one("#contentcore > div.contentArea > div.boardWrap > div > ul > li:nth-child(13) > div > div.txt").get_text(strip=True)
        lecture.category = soup.select_one("#contentcore > div.contentArea > div.boardWrap > div > ul > li:nth-child(6) > div > div.txt").get_text(strip=True)
        lecture.branch = soup.select_one("#contentcore > div.contentArea > div.boardWrap > div > ul > li:nth-child(2) > div > div.txt").get_text(strip=True)
        lecture.content = soup.select_one("#contentcore > div.contentArea > div.boardWrap > div > ul > li.conArea > div > div").get_text(strip=True)
        price: str = soup.select_one("#contentcore > div.contentArea > div.boardWrap > div > ul > li:nth-child(17) > div > div.txt").get_text(strip=True)
        if price not in ["무료", ""]:
            lecture.price = int(price.replace("원", "").replace(",", ""))
        else:
            lecture.price = 0
        lecture.address = center_info.get_addresses().get(lecture.branch)
        lecture.region = lecture.address.split(" ")[0]

        src: bs | None = soup.select_one("#contentcore > div.contentArea > div.boardWrap > div > ul > li.conArea > div > div > img")
        if src is not None:
            lecture.src = src.get_attribute_list("src")[0]
        lecture_start: str = soup.select_one("#contentcore > div.contentArea > div.boardWrap > div > ul > li:nth-child(7) > div > div.txt").get_text(strip=True)
        lecture_end: str = soup.select_one("#contentcore > div.contentArea > div.boardWrap > div > ul > li:nth-child(8) > div > div.txt").get_text(strip=True)
        enroll_start: str = soup.select_one("#contentcore > div.contentArea > div.boardWrap > div > ul > li:nth-child(19) > div > div.txt").get_text(strip=True)
        enroll_end: str = soup.select_one("#contentcore > div.contentArea > div.boardWrap > div > ul > li:nth-child(20) > div > div.txt").get_text(strip=True)
        detail_date: str = soup.select_one("#contentcore > div.contentArea > div.boardWrap > div > ul > li:nth-child(11) > div > div.txt > p").get_text(strip=True)
        lecture_count: str = soup.select_one("#contentcore > div.contentArea > div.boardWrap > div > ul > li:nth-child(9) > div > div.txt").get_text(strip=True)

        start_span: list[str] = [re.search(r"[0-9]{4}[.-][0-9]{2}[.-][0-9]{2}", lecture_start).group(),
                                 re.search(r"[0-9]{4}[.-][0-9]{2}[.-][0-9]{2}", lecture_end).group()]
        lecture.set_lecture_held_dates(start_span, detail_date, int(lecture_count))

        lecture.enrollEnd = re.search(r"[0-9]{4}[.-][0-9]{2}[.-][0-9]{2}", enroll_end).group()
        lecture.enrollStart = re.search(r"[0-9]{4}[.-][0-9]{2}[.-][0-9]{2}", enroll_start).group()

        return

    def __national_lib_ko(self, url: str, center_info: PublicLibrary):
        with request.urlopen(url) as u:
            html = u.read().decode('utf-8')

        soup = bs(html, "html5lib")
        lecture: LectureType = LectureType()
        lecture.url = url
        lecture.type = "공공기관"
        lecture.address = center_info.get_addresses().get("국립중앙도서관")
        lecture.region = lecture.address.split(" ")[0]
        lecture.title = soup.select_one("#sub_content > div.content_wrap > div > div > div.ucreq7_detail > div.title_wrap > strong > span.title").get_text(strip=True)
        lecture.price = 0
        images = soup.select("img")
        for image in images:
            src: str = image.get_attribute_list("src")[0]
            if "https://" in src:
                lecture.src = src
                break
            else:
                continue
        lecture.branch = "국립중앙도서관"
        lecture.center = "국립중앙도서관"
        # todo: 국립 중앙 도서관은 가져오기가 까다로워서 뒤로 미루게 되었음.
        contents = soup.select("#sub_content > div.content_wrap > div > div > div.ucreq7_detail > div.board_file_wrap > div")

        return

    def __busan_pen_edu(self, url: str, center_info: PublicLibrary):
        with request.urlopen(url) as u:
            html = u.read().decode('utf-8')

        soup = bs(html, "html5lib")
        lecture: LectureType = LectureType()
        lecture.url = url
        lecture.type = "공공기관"

        lecture.src = soup.select_one("#cntntsView > div.rveInfo > div.img > p > img").get_attribute_list("src")[0]
        lecture.branch = soup.select_one("#cntntsView > div.rveInfo > div.infoBox > ul > li:nth-child(1)").get_text(separator="@", strip=True).split("@")[1]

        lecture.address = center_info.get_addresses().get(lecture.branch)
        lecture.region = lecture.address.split(" ")[0]

        lecture.target = soup.select_one("#cntntsView > div.rveInfo > div.infoBox > ul > li:nth-child(8)").get_text(separator="@", strip=True).split("@")[-1]
        lecture.title = soup.select_one("#cntntsView > div.rveInfo > div.infoBox > h3").get_text(strip=True)
        lecture.category = lecture.title  # 카테고리가 따로 존재 하지 않아 제목으로 대체
        
        start_span = soup.select_one("#cntntsView > div.rveInfo > div.infoBox > ul > li:nth-child(2)").get_text(separator="@", strip=True).split("@")[-1].replace("\n", "").replace("\t", "")
        lecture_start: list[str] = re.findall(r"[0-9]{4}\s?[/.-]\s?[0-9]{2}\s?[/.-]\s?[0-9]{2}|[월화수목금토일,\s]+\s?[])]?\s?[0-9]{2}\s?:\s?[0-9]{2}\s?[-~]\s?[0-9]{2}\s?:\s?[0-9]{2}", start_span)
        lecture.set_lecture_held_dates([lecture_start[0], lecture_start[1]], lecture_start[-1])

        enroll_span = soup.select_one("#cntntsView > div.rveInfo > div.infoBox > ul > li:nth-child(3)").get_text(separator="@", strip=True).split("@")[-1].replace("\n", "").replace("\t", "")
        enroll_start: list[str] = re.findall(r"[0-9]{4}\s?[/.-]\s?[0-9]{2}\s?[/.-]\s?[0-9]{2}", enroll_span)
        lecture.enrollEnd = enroll_start[-1]
        lecture.enrollStart = enroll_start[0]

        lecture.content = soup.select_one("#cntntsView > div.box_st1.mgt20 > div.list_st1.mg10.cnDivEduCn.ViewImg100").get_text(strip=True, separator="\n")

        return

    def __tong_yeong_lib(self, url: str, center_info: PublicLibrary):
        """
        통영시립도서관 크롤러
        :param url: 내용을 가져올 url
        :param center_info: 통영시립도서관 address 를 받기 위해 필요.
        :return:
        """
        with request.urlopen(url) as u:
            html = u.read().decode('utf-8')

        soup = bs(html, "html5lib")
        lecture: LectureType = LectureType()
        lecture.url = url
        lecture.type = "공공기관"
        lecture.center = "통영시립도서관"
        lecture.branch = lecture.center
        lecture.address = center_info.get_addresses().get(lecture.branch)
        lecture.region = lecture.address.split(" ")[0]

        lecture.title = soup.select_one("#program > div > div.lecture_view > h4").get_text(strip=True)
        str_price: str = soup.select_one("#program > div > div.lecture_view >\
                     div:nth-child(5) > dl > dd:nth-child(4)").get_text(strip=True)
        lecture.price = trim_lecture_price(str_price)

        lecture.content = soup.select_one("#program > div > div.lecture_view > div.lecture_contents").get_text(strip=True)
        lecture.content = (lecture.content + "@#$" + soup.select_one("#program > div > div.lecture_view >\
                     div.lecture_contents > p:nth-child(5) > img").get_attribute_list("src")[0])

        enroll_start_end: dict = trim_lecture_time(soup.select_one("#program > div > div.lecture_view >\
                     div.lecture_view_detail > div.row_info2 > dl > dd:nth-child(2) > strong").get_text(strip=True), "~")
        lecture.enrollStart = enroll_start_end[0]
        lecture.enrollEnd = enroll_start_end[1]

        lecture_start_end: dict = trim_lecture_time(soup.select_one("#program > div > div.lecture_view >\
                     div.lecture_view_detail > div.row_info2 > dl > dd:nth-child(4)").get_text(strip=True), "~")
        lecture.lectureStart = lecture_start_end[0]
        lecture.lectureEnd = lecture_start_end[1]

        lecture.target = soup.select_one("#program > div > div.lecture_view > div:nth-child(2) > dl > dd.wpix").get_text(strip=True)
        supplies = soup.select_one("#program > div > div.lecture_view > div:nth-child(5) > dl > dd.wpix").get_text(strip=True)
        if validate_string(supplies):
            lecture.lectureSupplies = supplies
        return

    def __lib_union_gimhae(self, url: str, center_info: PublicLibrary):
        with request.urlopen(url) as u:
            html = u.read().decode('utf-8')

        soup = bs(html, "html5lib")
        lecture: LectureType = LectureType()
        lecture.url = url
        lecture.type = "공공기관"
        lecture.center = "김해통합도서관"
        lecture.branch = lecture.center
        lecture.address = center_info.get_addresses().get(lecture.branch)
        lecture.region = lecture.address.split(" ")[0]

        lecture.title = soup.select_one("#body_content > div > div.cp20view1 > div.hg1 > h2").get_text(strip=True)
        str_price: str = soup.select_one("#body_content > div > div.cp20view1 > div.even-grid.float-left >\
                     div:nth-child(2) > div > div.cp20dlist1 > ul > li:nth-child(7) > span").get_text(strip=True)
        lecture.price = trim_lecture_price(str_price)

        lecture.content = soup.select_one("#tabs1pane1 > div")
        lecture.content = (lecture.content + "@#$" +
                           soup.select_one("#tabs1pane1 > div > div > p:nth-child(3) > img").get_attribute_list("src")[0])
        lecture.src = soup.select_one("#body_content > div > div.cp20view1 > div.even-grid.float-left >\
                     div:nth-child(1) > div > p.p1 > img").get_attribute_list("src")[0]

        if len(soup.select("#tabs1pane1 > h3")) > 2:  # 강의 계획서가 이미지로라도 존재 하면 가지고 온다.
            lecture.set_curriculum({1: soup.select_one("#tabs1pane1 > p > img").get_attribute_list("src")[0]})

        enroll_start_end: dict = trim_lecture_time(soup.select_one("#body_content > div > div.cp20view1 >\
                     div.even-grid.float-left > div:nth-child(2) > div > div.cp20dlist1 > ul > li.di.bdt0 > span").get_text(strip=True), "~")
        lecture.enrollStart = enroll_start_end[0]
        lecture.enrollEnd = enroll_start_end[1]

        lecture_start_end: dict = trim_lecture_time(soup.select_one("#body_content > div > div.cp20view1 >\
                     div.even-grid.float-left > div:nth-child(2) > div > div.cp20dlist1 > ul > li:nth-child(2) > span").get_text(strip=True),
                                                    "~")
        lecture.lectureStart = lecture_start_end[0]
        lecture.lectureEnd = lecture_start_end[1]

        lecture.target = soup.select_one("#body_content > div > div.cp20view1 >\
                     div.even-grid.float-left > div:nth-child(2) > div > div.cp20dlist1 > ul > li:nth-child(4) > span")
        lecture.lectureSupplies = soup.select_one("#body_content > div > div.cp20view1 > div.even-grid.float-left >\
                     div:nth-child(2) > div > div.cp20dlist1 > ul > li:nth-child(8) > span")
        return

    def __ice_edu_lib(self, url: str, center_info: PublicLibrary):
        """
        인천 광역시 교육청 통합 공공 도서관
        인천광역시교육청북구도서관:  인천 부평구 신트리로 21 (부평동)
        인천광역시교육청부평도서관:  인천 부평구 경원대로 1191 (십정동)
        인천광역시교육청중구도서관:  인천 부평구 신트리로 21 (부평동)
        인천광역시교육청중앙도서관:  인천 남동구 정각로 9 (구월동)
        인천광역시교육청주안도서관:  인천 미추홀구 구월남로 27 (주안동)
        인천광역시교육청화도진도서관:  인천 동구 화도진로 122 (화수동)
        인천광역시교육청서구도서관:  인천 서구 건지로 334번길 45 (가좌동)
        인천광역시교육청계양도서관:  인천 계양구 계양산로134번길 18 (계산동)
        인천광역시교육청연수도서관:  인천 연수구 함박뫼로152번길 96 (연수동)
        :param url:
        :param center_info:
        :return:
        """
        with request.urlopen(url) as u:
            html = u.read().decode('utf-8')

        soup = bs(html, "html5lib")
        lecture: LectureType = LectureType()
        lecture.url = url
        lecture.type = "공공기관"
        # todo: 통합 도서관에서 가져오는 경우 별도의 주소가 있기 때문에 수정 필요.
        lecture.center = "인천광역시교육청통합공공도서관"
        lecture.branch = lecture.center
        lecture.address = center_info.get_addresses().get(lecture.branch)
        lecture.region = lecture.address.split(" ")[0]

        lecture.content = soup.select_one("#teach_table > tbody > tr:nth-child(3) > td").get_text(strip=True)
        lecture.title = soup.select_one("#contentArea > div > div > div.teach_top > h3").get_text(strip=True)
        lecture.target = soup.select_one("#teach_table > tbody > tr:nth-child(12) > td.last.td2").get_text(strip=True)

        start_detail: str = soup.select_one("#teach_table > tbody > tr:nth-child(9) > td.last.td2").get_text(strip=True)
        enroll_span: list[str] = soup.select_one("#teach_table > tbody > tr:nth-child(16) > td.td1").get_text(separator="@", strip=True).split("@")
        start_span: list[str] = soup.select_one("#teach_table > tbody > tr:nth-child(7) > td").get_text(separator="@", strip=True).split("@")

        enroll_trim: tuple = trim_lecture_span_str("~".join(enroll_span))
        lecture.enrollStart = enroll_trim[0]
        lecture.enrollEnd = enroll_trim[1]
        lecture.set_lecture_held_dates(lecture_start_end=start_span, detail=start_detail)

        return

    def __jbe_edu_lib(self, url: str, center_info: PublicLibrary):
        """
        전북특별자치도교육청통합도서관/교육문화회관
        :param url:
        :param center_info:
        :return:
        """
        with request.urlopen(url) as u:
            html = u.read().decode('utf-8')

        soup = bs(html, "html5lib")
        lecture: LectureType = LectureType()
        lecture.url = url
        lecture.type = "공공기관"
        # todo: 통합 도서관에서 가져오는 경우 별도의 주소가 있기 때문에 수정 필요.
        lecture.center = "전북특별자치도교육청통합도서관/교육문화회관"
        lecture.branch = lecture.center
        lecture.address = center_info.get_addresses().get(lecture.branch)
        lecture.region = lecture.address.split(" ")[0]

        lecture.title = soup.select_one("#contentArea > div > div > div.teach_top > h3").get_text(strip=True)
        lecture.target = soup.select_one("#teach_table > tbody > tr:nth-child(11) > td.last.td2").get_text(strip=True)
        lecture.content = soup.select_one("#teach_table > tbody > tr:nth-child(2) > td").get_text(strip=True)
        lecture.category = soup.select_one("#teach_table > tbody > tr.first > td").get_text(strip=True)

        start_detail: str = soup.select_one("#teach_table > tbody > tr:nth-child(8) > td.last.td2").get_text(strip=True)
        start_span: list[str] = soup.select_one("#teach_table > tbody > tr:nth-child(6) > td").get_text(separator="@", strip=True).split("@")
        enroll_span: str = soup.select_one("#teach_table > tbody > tr:nth-child(16) > td.td1").get_text(strip=True)
        start, end = trim_lecture_span_str(enroll_span)
        lecture.enrollStart = start
        lecture.enrollEnd = end
        lecture.set_lecture_held_dates(start_span, start_detail)

        image = soup.select_one("#teach_table > tbody > tr.first > th > img")
        if image is not None:
            lecture.src = image.get_attribute_list("src")[0]

        supplies: str = soup.select_one("#teach_table > tbody > tr:nth-child(3) > td.last.td2").get_text(strip=True)
        if validate_string(supplies):
            lecture.lectureSupplies = supplies

        lecture.classId = ClassIdInfos.make_class_id(lecture)
        return

    def __gwangju_seogu_edu_lib(self, url: str, center_info: PublicLibrary):
        """
        상록도서관  :  광주광역시 서구 상무대로1171번길 11(농성동)
        어린이생태학습도서관  :   광주광역시 서구 풍암공원로 8(풍암동)
        서빛마루도서관  :   광주광역시 서구 풍암공원로30(풍암동)
        서구공공도서관  :   광주광역시 서구 마재로 3(금호동)
        :param url:
        :param center_info:
        :return:
        """
        with request.urlopen(url) as u:
            html = u.read().decode('utf-8')

        soup = bs(html, "html5lib")
        lecture: LectureType = LectureType()
        lecture.url = url
        lecture.type = "공공기관"
        # todo: 통합 도서관에서 가져오는 경우 별도의 주소가 있기 때문에 수정 필요.
        lecture.center = "광주광역시서구통합도서관"
        lecture.branch = soup.select_one("#content > table > tbody > tr:nth-child(1) > td:nth-child(4)").get_text(strip=True)
        lecture.address = center_info.get_addresses().get(lecture.branch)
        lecture.region = lecture.address.split(" ")[0]

        lecture.title = soup.select_one("#content > table > tbody > tr:nth-child(2) > td").get_text(strip=True)
        lecture.content = soup.select_one("#content > table > tbody > tr:nth-child(7) > td").get_text(strip=True, separator="\n")
        lecture.target = soup.select_one("#content > table > tbody > tr:nth-child(1) > td:nth-child(2)").get_text(strip=True)
        price_str: str = soup.select_one("#content > table > tbody > tr:nth-child(6) > td:nth-child(4)").get_text(strip=True)
        lecture.price = trim_lecture_price(price_str)

        enroll_span: str = soup.select_one("#content > table > tbody > tr:nth-child(3) > td:nth-child(2)").get_text(strip=True)
        start, end = trim_lecture_span_str(enroll_span)
        lecture.enrollStart = start
        lecture.enrollEnd = end

        start_span: list[str] = soup.select_one("#content > table > tbody > tr:nth-child(3) > td:nth-child(4)").get_text(separator="@", strip=True).split("@")
        start_detail: str = weekday_from_date_str(start_span[0])
        lecture.set_lecture_held_dates(start_span, start_detail)
        return
















