import queue
from playwright.sync_api import Browser
from crawler.settingcrawler.settingcrawlerabstract import SettingCrawler
from crawler.settingcrawler.settingcrawlerfactory import SettingCrawlerFactory
import threading
import json
from typeclass.restartcontext import Context


class Controller:
    """
    """
    urlContextPath: str = "crawler/urlcontexts.json"
    infoContextPath: str = "crawler/infocontexts.json"
    browser: Browser

    def __init__(self, page: Browser):
        self.browser = page
        return

    def json_data(self, how: str, party: str, context: list = None) -> list | None:
        if party == "url":
            path = self.urlContextPath
        else:
            path = self.infoContextPath
        with open(path, how, encoding='utf-8-sig') as j:
            if how == "r" and context is None:
                data = json.load(j)
                return data
            else:
                json.dump(context, j, ensure_ascii=False, indent=4)
                return None

    def dump_error_context(self, context: Context, party: str):
        data: list = self.json_data(how="r", party=party)
        data.append(context.__getstate__())
        self.json_data(how="w", party=party, context=[data])
        return

    def load_error_context(self, party: str) -> queue.Queue | list | None:
        """
        에러가 발생한 내용들을 다시 실행 하기 위해 반환.
        :param party:
        :return:
        """
        data: list = self.json_data(how="r", party=party)
        self.json_data(how="w", party=party, context=[])
        if len(data) < 1:
            return None
        if party == "info":
            info_details: queue.Queue = queue.Queue()
            for d in data:
                info = d.get("info").__setstate__()
                d["info"] = info
                info_details.put(d)
            return info_details
        else:
            for d in data:
                url = d.get("info").__setstate__()
                d["info"] = url
                del d["centerName"]
            return data

    def branch_mismatch(self, center: str):
        crawler: SettingCrawler = SettingCrawlerFactory.get_crawler(center)
        threading.Thread(target=crawler(self.browser.new_page()).crawl)
        return



