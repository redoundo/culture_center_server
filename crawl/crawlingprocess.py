import datetime
from pytz import timezone
from crawler.crawlerabstract import NoLinkCrawler, WithLinkCrawler
from crawler.unwrapcenterinfo import unwrap_no_link, unwrap_with_link
from messages.messenger import DiscordMessenger
from db.MysqlActions import MysqlActions
from crawler.crawlerfactory import NoLinkCrawlerFactory, WithLinkCrawlerFactory
from playwright.sync_api import Page, sync_playwright, Browser
import threading
import sys
import json
import queue


database: MysqlActions = MysqlActions()
sys.path.append("..")


def json_data(path: str, how: str):
    with open(path, how, encoding='utf-8-sig') as j:
        data = json.load(j)
    return data


def url_crawling(href_queue: queue.Queue, message_queue: queue.Queue):
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

                for info in unwrap(json_data(paths[center], "r"), center):
                    if center in NoLinkCrawlerFactory.get_all_center_names():
                        no_link_crawler: NoLinkCrawler = NoLinkCrawlerFactory.get_crawler(center)
                        center_crawler: NoLinkCrawler = no_link_crawler(NoLinkCrawlerFactory.get_url(center),
                                                                        info, url_browser.new_page())
                    else:
                        with_link_crawler: WithLinkCrawler = WithLinkCrawlerFactory.get_crawler(center)
                        center_crawler: WithLinkCrawler = with_link_crawler(info, url_browser.new_page())

                    try:
                        center_crawler.crawl()
                        center_crawler.page.close()
                        lecture_hrefs: list[str] = center_crawler.lectureHrefs
                        if lecture_hrefs is None or len(lecture_hrefs) < 1:
                            now: str = datetime.datetime.now(timezone("Asia/Seoul")).strftime('%Y/%m/%d, %H:%M:%S')
                            message_queue.put(f"강좌 부재\n{center} 사이트의 {info.get_region()} 지역의 {info.get_branch()}\
                             지점을 크롤링 하려고 했으나, 크롤링 할 url 이 존재 하지 않아 {now} 현재 다음 지점으로 넘어 갑니다.")
                            continue
                        need_crawl_urls: list[str] = database.skip_saved_url(info, lecture_hrefs)
                        if need_crawl_urls is None or len(need_crawl_urls) < 1:
                            now: str = datetime.datetime.now(timezone("Asia/Seoul")).strftime('%Y/%m/%d, %H:%M:%S')
                            message_queue.put(f"지점 스킵\n{center} 사이트의 {info.get_region()} 지역의 {info.get_branch()}\
                                지점을 크롤링 하려고 했으나, 이미 크롤링이 완료 된 지점으로 파악 되어 {now} 현재 다음 지점으로 넘어 갑니다.")
                            continue
                        href_queue.put({"center_info": info, "urls": need_crawl_urls, "name": center}, block=True, timeout=None)
                    except Exception as e:
                        href_queue.put(None)
                        center_crawler.page.close()
                        print(e)
                        now: str = datetime.datetime.now(timezone("Asia/Seoul")).strftime('%Y/%m/%d, %H:%M:%S')
                        message_text: str = f"사이트 url 수집 중에 오류 발생!!!\n발생 시각:  {now}\n오류 내용:  {e}\n센터 이름:\
                        {info.get_center_name()}\n현재 지역:  {info.get_region()}\n현재 지점:  {info.get_branch()}"
                        message_queue.put(message_text)
            except Exception as e:
                href_queue.put(None)
                print(e)
                now: str = datetime.datetime.now(timezone("Asia/Seoul")).strftime('%Y/%m/%d, %H:%M:%S')
                message_text: str = f"크롤러 설정 중 오류 발생!!!\n발생 시각:  {now}\n오류 내용:  {e}\n센터 이름:  {center}"
                message_queue.put(message_text)
    return


def info_crawling(href_queue: queue.Queue, message_queue: queue.Queue):
    while True:
        data = href_queue.get(block=True, timeout=None)
        if data in [None]:
            break
        else:
            if len(data.keys()) < 1:
                continue
            try:
                info = data.get("center_info")
                urls: list[str] = data.get("urls")
                _extract_info(urls=urls, info=info)
            except Exception as e:
                print(e)
                now: str = datetime.datetime.now(timezone("Asia/Seoul")).strftime('%Y/%m/%d, %H:%M:%S')
                message_text: str = f"전체 url 내용 추출 도중 문제 발생!!!!\n발생 시각:  {now}\n오류 내용:  {e}\n센터 이름:\
{data.get('name')}\n크롤링 지역:  {data.get('center_info').get_region()}\n크롤링 지점:  {data.get('center_info').get_branch()}"
                message_queue.put(message_text)
                continue
    return


def _extract_info(urls: list[str], info):
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
                now: str = datetime.datetime.now(timezone("Asia/Seoul")).strftime('%Y/%m/%d, %H:%M:%S')
                message_text: str = f"url 내용 추출 도중 에러 발생!!!\n발생 시각:  {now}\n에러 내용:  {e}\n현재 url:\
{url}\n센터 이름:  {info.get_center_name()}\n크롤링 지역:  {info.get_region()}\n크롤링 지점:  {info.get_branch()}"
                message_queue.put(message_text)
                continue
        page.close()
    return


if __name__ == '__main__':
    url_queue: queue.Queue = queue.Queue(maxsize=5)
    message_queue: queue.Queue = queue.Queue(maxsize=10)

    messenger: DiscordMessenger = DiscordMessenger(message_queue=message_queue)
    url_thread: threading.Thread = threading.Thread(daemon=True, target=url_crawling, args=[url_queue, message_queue, ])
    info_thread: threading.Thread = threading.Thread(daemon=True, target=info_crawling, args=[url_queue, message_queue, ])
    message_thread: threading.Thread = threading.Thread(daemon=True, target=messenger.send_message)
    url_thread.start()
    info_thread.start()

    url_thread.join()
    info_thread.join()
    database.create_train_sample(queue=message_queue)
    database.connection.close()

    message_thread.join()

