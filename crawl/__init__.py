from typeclass import ClassIdInfoType, CenterInfoNoLink, CenterInfoWithLink, LectureType
from db import MysqlActions
from messages import messenger
from crawler import crawlerfactory, crawlerabstract, unwrapcenterinfo
from crawler.nolink import AkplazaCrawler, EmartCrawler, HomePlusCrawler, LotteMartCrawler
from crawler.withlink import GalleriaCrawler, LotteCrawler, HyundaiCrawler


class_info_type = ClassIdInfoType
center_info_no_link = CenterInfoNoLink
center_info_with_link = CenterInfoWithLink
lecture_type = LectureType
crawler_factory = crawlerfactory
crawler_abstract = crawlerabstract
unwrap_center_info = unwrapcenterinfo
mysql_actions = MysqlActions
messenger = messenger
galleria_crawler = GalleriaCrawler
lotte_crawler = LotteCrawler
hyundai_crawler = HyundaiCrawler
akplaza_crawler = AkplazaCrawler
emart_crawler = EmartCrawler
home_plus_crawler = HomePlusCrawler
lotte_mart_crawler = LotteMartCrawler
