import datetime
from pytz import timezone
from crawler.crawlerabstract import NoLinkCrawler, WithLinkCrawler
from crawler.unwrapcenterinfo import unwrap_no_link, unwrap_with_link
from messages.messenger import DiscordMessenger
from crawler.db.MysqlActions import MysqlActions
from crawler.crawlerfactory import NoLinkCrawlerFactory, WithLinkCrawlerFactory
from playwright.sync_api import Page, sync_playwright, Browser
import threading

from typeclass.CenterInfo import CenterInfoWithLink
from typeclass.CenterInfoNoLink import CenterInfoNoLink
from typeclass.restartcontext import UrlContext, InfoContext
from crawler.crawlmain import Controller
import sys
import json
import queue

database: MysqlActions = MysqlActions()
sys.path.append("..")


def json_data(path: str, how: str):
    with open(path, how, encoding='utf-8-sig') as j:
        data = json.load(j)
    return data


class ContentCrawler:
    controller: Controller
    messageQueue: queue.Queue[str]
    hrefQueue = queue.Queue
    contentThreads: list[threading.Thread]

    def __init__(self, controller: Controller, message_queue: queue.Queue, href_queue: queue.Queue):
        self.controller = controller
        self.messageQueue = message_queue
        self.hrefQueue = href_queue
        return

    def run(self, error_data: queue.Queue = None):
        if error_data is not None:
            content_thread2 = threading.Thread = threading.Thread(target=self.info_crawling, args=(error_data, ))
            content_thread2.start()
            content_thread2.join()
            return
        content_thread1: threading.Thread = threading.Thread(target=self.info_crawling)
        content_thread1.start()
        content_thread1.join()
        return

    def info_crawling(self, context_queue: queue.Queue = None):
        while True:
            if context_queue is not None:
                data = context_queue.get(block=True, timeout=None)
            else:
                data = self.hrefQueue.get(block=True, timeout=None)
            if data in [None]:
                break
            else:
                if len(data.keys()) < 1:
                    continue
                try:
                    info = data.get("center_info")
                    urls: list[str] = data.get("urls")
                    self._extract_info(urls=urls, info=info)
                except Exception as e:
                    print(e)
                    # 문제가 발생 했을 경우,
                    self.controller.dump_error_context(
                        context=InfoContext(center=data.get("center_info").get_center_name(),
                                            urls=data.get("urls"), info=data.get("center_info")), party="info")
                    now: str = datetime.datetime.now(timezone("Asia/Seoul")).strftime('%Y/%m/%d, %H:%M:%S')
                    message_text: str = f"전체 url 내용 추출 도중 문제 발생!!!!\n발생 시각:  {now}\n오류 내용:  {e}\n센터 이름:\
    {data.get('name')}\n크롤링 지역:  {data.get('center_info').get_region()}\n크롤링 지점:  {data.get('center_info').get_branch()}"
                    self.messageQueue.put(message_text)
                    continue
        return

    def _extract_info(self, urls: list[str], info):
        with sync_playwright() as playwright:
            info_browser: Browser = playwright.chromium.launch(headless=True, timeout=0)
            page: Page = info_browser.new_page()
            for url in urls:
                center: str = info.get_center_name()
                if center in NoLinkCrawlerFactory.get_all_center_names():
                    no_link_crawler: NoLinkCrawler = NoLinkCrawlerFactory.get_crawler(center)
                    center_crawler: NoLinkCrawler = no_link_crawler(NoLinkCrawlerFactory.get_url(center),
                                                                    info, page)
                else:
                    with_link_crawler: WithLinkCrawler = WithLinkCrawlerFactory.get_crawler(center)
                    center_crawler: WithLinkCrawler = with_link_crawler(info, page)

                try:
                    lecture_info = center_crawler.extract_lecture_info(url, page, info.__getstate__())
                    database.insert_into_db(next(lecture_info))
                except Exception as e:
                    print(e)
                    self.controller.dump_error_context(context=InfoContext(center=info.get_center_name(), url=url, urls=urls, info=info), party="info")
                    now: str = datetime.datetime.now(timezone("Asia/Seoul")).strftime('%Y/%m/%d, %H:%M:%S')
                    message_text: str = f"url 내용 추출 도중 에러 발생!!!\n발생 시각:  {now}\n에러 내용:  {e}\n현재 url:\
    {url}\n센터 이름:  {info.get_center_name()}\n크롤링 지역:  {info.get_region()}\n크롤링 지점:  {info.get_branch()}"
                    self.messageQueue.put(message_text)
                    continue
            page.close()
        return


class UrlCrawler:
    messageQueue: queue.Queue
    hrefQueue: queue.Queue
    controller: Controller

    def __init__(self, message_queue: queue.Queue, href_queue: queue.Queue, controller: Controller):
        self.controller = controller
        self.messageQueue = message_queue
        self.hrefQueue = href_queue
        return

    def __get_branches(self, center: str) -> list:
        return database.all_branch_names(center)

    def run(self, data: list = None):
        if data is not None:
            url_thread1: threading.Thread = threading.Thread(target=self.url_crawling, args=(data, ))
            url_thread1.start()
            url_thread1.join()
            return
        url_thread2: threading.Thread = threading.Thread(target=self.url_crawling)
        url_thread2.start()
        url_thread2.join()
        return

    def url_crawling(self, context: list[CenterInfoNoLink | CenterInfoWithLink] = None):
        """
        url 을 가져오기 위한 crawler 설정과 가져오는 과정 포함.
        :return:
        """
        centers: dict = dict()
        centers.update(NoLinkCrawlerFactory.get_all_center_paths())
        centers.update(WithLinkCrawlerFactory.get_all_center_paths())

        with sync_playwright() as playwright:
            url_browser: Browser = playwright.chromium.launch(headless=True, timeout=0)
            for center in list(centers.keys()):
                try:
                    if center in NoLinkCrawlerFactory.get_all_center_names():
                        paths = NoLinkCrawlerFactory.get_all_center_paths()
                        unwrap = unwrap_no_link
                    else:
                        paths = WithLinkCrawlerFactory.get_all_center_paths()
                        unwrap = unwrap_with_link

                    data: list[CenterInfoNoLink | CenterInfoWithLink] = context
                    if data is None:
                        data = unwrap(json_data(paths[center], "r"), center)

                    for info in data:
                        if center in NoLinkCrawlerFactory.get_all_center_names():
                            no_link_crawler: NoLinkCrawler = NoLinkCrawlerFactory.get_crawler(center)
                            center_crawler: NoLinkCrawler = no_link_crawler(NoLinkCrawlerFactory.get_url(center),
                                                                            info, url_browser.new_page())
                        else:
                            with_link_crawler: WithLinkCrawler = WithLinkCrawlerFactory.get_crawler(center)
                            center_crawler: WithLinkCrawler = with_link_crawler(info, url_browser.new_page())

                        try:
                            center_crawler.branches = self.__get_branches(center)

                            center_crawler.crawl()
                            center_crawler.page.close()

                            lecture_hrefs: list[str] = center_crawler.lectureHrefs
                            if lecture_hrefs is None or len(lecture_hrefs) < 1:
                                now: str = datetime.datetime.now(timezone("Asia/Seoul")).strftime('%Y/%m/%d, %H:%M:%S')
                                self.messageQueue.put(f"강좌 부재\n{center} 사이트의 {info.get_region()} 지역의 {info.get_branch()}\
                                 지점을 크롤링 하려고 했으나, 크롤링 할 url 이 존재 하지 않아 {now} 현재 다음 지점으로 넘어 갑니다.")
                                continue
                            need_crawl_urls: list[str] = database.skip_saved_url(info, lecture_hrefs)
                            if need_crawl_urls is None or len(need_crawl_urls) < 1:
                                now: str = datetime.datetime.now(timezone("Asia/Seoul")).strftime('%Y/%m/%d, %H:%M:%S')
                                self.messageQueue.put(f"지점 스킵\n{center} 사이트의 {info.get_region()} 지역의 {info.get_branch()}\
                                    지점을 크롤링 하려고 했으나, 이미 크롤링이 완료 된 지점으로 파악 되어 {now} 현재 다음 지점으로 넘어 갑니다.")
                                continue
                            self.hrefQueue.put({"center_info": info, "urls": need_crawl_urls, "name": center},
                                               block=True, timeout=None)
                        except Exception as e:
                            if e.args[0] == "BRANCH_UNMATCH":
                                # 지점 불일치 시 controller 에서 해당 사이트 지점 확인을 위한 thread 생성 및 실행
                                self.controller.branch_mismatch(center)
                            self.hrefQueue.put(None)
                            center_crawler.page.close()
                            print(e)
                            self.controller.dump_error_context(context=UrlContext(info.get_center_name(), info), party="url")
                            now: str = datetime.datetime.now(timezone("Asia/Seoul")).strftime('%Y/%m/%d, %H:%M:%S')
                            message_text: str = f"사이트 url 수집 중에 오류 발생!!!\n발생 시각:  {now}\n오류 내용:  {e}\n센터 이름:\
                            {info.get_center_name()}\n현재 지역:  {info.get_region()}\n현재 지점:  {info.get_branch()}"
                            self.messageQueue.put(message_text)
                            continue
                except Exception as e:
                    self.hrefQueue.put(None)
                    print(e)
                    now: str = datetime.datetime.now(timezone("Asia/Seoul")).strftime('%Y/%m/%d, %H:%M:%S')
                    message_text: str = f"크롤러 설정 중 오류 발생!!!\n발생 시각:  {now}\n오류 내용:  {e}\n센터 이름:  {center}"
                    self.messageQueue.put(message_text)
                    continue
        return


browser: Browser = sync_playwright().start().chromium.launch(headless=True, timeout=0)

if __name__ == '__main__':
    crawler_controller: Controller = Controller(browser)
    url_queue: queue.Queue = queue.Queue(maxsize=5)
    message_queue: queue.Queue = queue.Queue(maxsize=10)

    url_crawler: UrlCrawler = UrlCrawler(message_queue=message_queue, href_queue=url_queue, controller=crawler_controller)
    info_crawler: ContentCrawler = ContentCrawler(message_queue=message_queue, href_queue=url_queue, controller=crawler_controller)

    messenger: DiscordMessenger = DiscordMessenger(message_queue=message_queue)
    message_thread: threading.Thread = threading.Thread(daemon=True, target=messenger.send_message)
    url_thread: threading.Thread = threading.Thread(target=url_crawler.run)
    content_thread: threading.Thread = threading.Thread(target=info_crawler.run)
    url_thread.start()
    content_thread.start()

    url_thread.join()
    content_thread.join()

    url_data: list = crawler_controller.load_error_context(party="url")
    context_data: queue.Queue = crawler_controller.load_error_context(party="info")

    if context_data is not None:
        error_context_thread: threading.Thread = threading.Thread(target=info_crawler.run, args=(context_data,))
    else:
        error_context_thread: threading.Thread = threading.Thread(target=info_crawler.run)
    error_context_thread.start()

    if url_data is not None and len(url_data) > 0:
        error_url_thread: threading.Thread = threading.Thread(target=url_crawler.run, args=(url_data, ))
        error_url_thread.start()
        error_url_thread.join()
    error_context_thread.join()

    database.create_train_sample(queue=message_queue)
    database.connection.close()

    message_thread.join()
