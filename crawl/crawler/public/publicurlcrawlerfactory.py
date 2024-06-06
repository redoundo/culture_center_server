from bs4 import BeautifulSoup as bs
import html5lib
import re
from urllib import request
from crawl.typeclass.PublicLibrary import PublicLibrary
from crawl.typeclass.LectureType import LectureType


class PublicUrlCrawlerFactory:

    def __init__(self):
        return

    def __ever_learning(self, url: str, center_info: PublicLibrary):
        with request.urlopen(url) as u:
            html = u.read().decode('utf-8')

        soup = bs(html, "html5lib")
        lecture: LectureType = LectureType()
        lecture.center = "에버러닝"
        lecture.url = url
        lecture.type = "공공기관"
        lecture.region = center_info.get_addresses()
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
        lecture.src = soup.select_one("#cntntsView > div.rveInfo > div.img > p > img").get_attribute_list("src")[0]
        lecture.branch = soup.select_one("#cntntsView > div.rveInfo > div.infoBox > ul > li:nth-child(1)").get_text(separator="@", strip=True).split("@")[1]
        lecture.target = soup.select_one("#cntntsView > div.rveInfo > div.infoBox > ul > li:nth-child(8)").get_text(separator="@", strip=True).split("@")[-1]
        start_span = soup.select_one("#cntntsView > div.rveInfo > div.infoBox > ul > li:nth-child(2)").get_text(separator="@", strip=True).split("@")[-1]
        lecture_start = re.search(r"", start_span)



        return






















