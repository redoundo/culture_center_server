import os
import time
import asyncio
import psutil
from crawl.crawler.crawlerabstract import NoLinkCrawler, WithLinkCrawler
from crawl.crawler.unwrapcenterinfo import unwrap_no_link, unwrap_with_link
from server.app.crawl.db.MysqlActions import MysqlActions
from server.app.crawl.crawler.crawlerfactory import NoLinkCrawlerFactory, WithLinkCrawlerFactory
from playwright.sync_api import Playwright, Page, sync_playwright, Browser
import threading
import queue
from utils.util import json_data

database: MysqlActions = MysqlActions()


def url_crawling(href_queue: queue.Queue):
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
                            # message_queue.put(f"{center} 사이트의 {info.get_region()} 지역의 {info.get_branch()}\
                            #  지점을 크롤링 하려고 했으나, 크롤링 할 url 이 존재 하지 않아 다음 지점으로 넘어 갑니다.")
                            continue
                        need_crawl_urls: list[str] = database.skip_saved_url(info, lecture_hrefs)
                        if need_crawl_urls is None or len(need_crawl_urls) < 1:
                            # message_queue.put(f"{center} 사이트의 {info.get_region()} 지역의 {info.get_branch()} \
                            #     지점을 크롤링 하려고 했으나, 이미 크롤링이 완료 된 지점으로 파악 되어 다음 지점으로 넘어 갑니다.")
                            continue
                        href_queue.put({"center_info": info, "urls": need_crawl_urls, "name": center}, block=True, timeout=None)
                    except Exception as e:
                        href_queue.put(None)
                        center_crawler.page.close()
                        print(e)
                        # message_text: str = f"in url_crawling#_crawling exception occurred!!! {e} \
                        # current region is {info.get_region()} \n current branch is {info.get_branch()}\
                        # current center name is {info.get_center_name()}"
                        # message_queue.put(message_text)
            except Exception as e:
                href_queue.put(None)
                print(e)
                # message_text: str = f"exception occurred in url_crawling !!! {e}  \n  current center name is {center}"
                # message_queue.put(message_text)
    return


def info_crawling(href_queue: queue.Queue):
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
                # message_text: str = f"exception occurred in info_crawling!!! {e}  \
                # current region is {data.get('center_info').get_region()} \
                #  current branch is {data.get('center_info').get_branch()}  current center name is {data.get('name')}"
                # message_queue.put(message_text)
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
                # message_text: str = f"exception occurred in _extract_info!!! {e}  \n  current url is {url} \
                #   current region is {info.get_region()} \n current branch is {info.get_branch()} \
                #    current center name is {info.get_center_name()}"
                # message_queue.put(message_text)
                continue
        page.close()
    return


if __name__ == '__main__':
    url_queue: queue.Queue = queue.Queue(maxsize=5)
    url_thread: threading.Thread = threading.Thread(daemon=True, target=url_crawling, args=[url_queue, ])
    info_thread: threading.Thread = threading.Thread(daemon=True, target=info_crawling, args=[url_queue, ])

    url_thread.start()
    info_thread.start()

    url_thread.join()
    info_thread.join()


