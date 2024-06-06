import queue
from pytz import timezone
from mysql.connector import connection
from crawl.typeclass.CenterInfoNoLink import CenterInfoNoLink
from crawl.typeclass.CenterInfoWithLink import CenterInfoWithLink
from crawl.typeclass.ClassIdInfoType import ClassIdInfos
from crawl.typeclass.LectureType import LectureType
from dotenv import load_dotenv
import os
import json
import datetime

load_dotenv()
databaseName: str = os.getenv("DATABASE_NAME")
databasePassword: str = os.getenv("DATABASE_PASSWORD")
databaseUser: str = os.getenv("DATABASE_USERNAME")
databaseHost: str = os.getenv("DATABASE_HOST")
databasePort: str = os.getenv("DATABASE_PORT")


def add_json_data(path: str, how: str, value: any):
    with open(path, how, encoding='utf-8-sig') as J:
        json.dump(value, J, ensure_ascii=False, indent=4)


def str_to_date(date: str) -> str:
    """
    문자열 날짜를  mysql 에서 datetime 으로 사용할 수 있게 끔 str_to_date 적용.
    :param date: 문자열로 된 날짜
    :return:
    """
    if date == 'NULL'.replace("'", "''"):
        return date
    if len(date) < 6:
        return f"STR_TO_DATE('{str(datetime.datetime.now(timezone('Asia/Seoul')).year)}-{date[0:2]}-{date[3:5]}', '%Y-%m-%d')"
    return f"STR_TO_DATE('{date[0:4]}-{date[5:7]}-{date[8:10]}', '%Y-%m-%d')"


def single_quote_escape(text: str) -> str:
    """
    쿼리를 만들 때 '()' 안에 넣어야 되는 문자열 중 '을 가지고 있을 것을 대비하여 '을 ''으로 변경해 에러 방지.
    :param text: 작은 따옴표가 들어있을 수 있는 문자열
    :return: '이 ''으로 바뀐 문자열
    """
    return text.replace("'", "''")


class MysqlActions:
    """
        mysql db 연결 담당. 데이터 처리 및 데이터 저장 진행.
        단 한번만 생성해야하며 각 크롤러에서 mysqlactions 객체를 불러와 db 작업 진행.
    """

    connection: connection.MySQLConnection

    def __init__(self) -> None:
        """
            db 연결 풀 생성. auto commit 설정 되어있음.
        """
        self.connection = connection.MySQLConnection(user=databaseUser, database=databaseName,
                                                     password=databasePassword, host=databaseHost, port=int(databasePort))

        return

    def insert_into_db(self, data: LectureType) -> None:
        """
        db 연결 풀에서 연결을 가져와 크롤링한 내용을 저장한다.
        :param data: 저장할 데이터
        :return:
        """
        try:
            cursor: connection.MySQLCursor = self.connection.cursor()

            casted_json = single_quote_escape('NULL')
            if data.curriculum != casted_json:
                casted_json = f"CAST('{data.curriculum}' AS JSON)"

            sql: str = "INSERT INTO lectures(lectureId, type, center, region, branch, address, target, category,"
            sql += "url, src, title, price, content, curriculum, lectureSupplies, lectureStart, lectureEnd, enrollStart"
            sql += ",enrollEnd, lectureHeldDates)"
            sql += f" VALUES('{data.classId}', '{data.type}', '{data.center}', '{data.region}',\
               '{data.branch}', '{data.address}', '{data.target}', '{data.category}', '{data.url}', '{data.src}',\
                '{single_quote_escape(data.title)}', {data.price}, '{single_quote_escape(data.content)}',\
                 {casted_json}, '{single_quote_escape(data.lectureSupplies)}',\
                  {str_to_date(data.lectureStart)}, {str_to_date(data.lectureEnd)} , \
                  {str_to_date(data.enrollEnd)}, '{data.crawlerIndex}', '{data.lectureHeldDates}');"
            cursor.execute(sql)
        except Exception as e:
            print(e)
        finally:
            self.connection.commit()
        return

    def most_recent_crawler_index(self) -> str:
        """
        db 에서 crawledDate 를 기준으로 한 가장 최신의 crawlerIndex 를 가져온다.
        가져 오는데 실패 했다면 'null' 을 반환 한다.
        :return: 'null' || 'NO_00' || 'WITH_00'
        """
        crawler_index: str = "null"
        try:
            cursor: connection.MySQLCursor = self.connection.cursor()
            sql: str = "SELECT crawlerIndex FROM lectures ORDER BY crawledDate DESC LIMIT 0,1;"
            cursor.execute(sql)
            crawler_index = cursor.fetchone()[0]
        except Exception as e:
            print(e)
        finally:
            connection.commit()
        return crawler_index

    def skip_exist_url(self, index: str, urls: list):
        crawl_urls: list[str] = []
        try:
            cursor: connection.MySQLCursor = self.connection.cursor()
            sql: str = f"SELECT url FROM lectures WHERE crawlerIndex = '{index}';"
            cursor.execute(sql)
            exist_urls: list = []
            for url in cursor.fetchall():
                exist_urls.append(url[0])

            for url in urls:
                if url not in exist_urls:
                    crawl_urls.append(url)
        except Exception as e:
            print(e)
        finally:
            self.connection.commit()
        return crawl_urls

    def skip_saved_url(self, info: CenterInfoNoLink | CenterInfoWithLink, urls: list[str]) -> list[str]:
        need_crawl_urls: list[str] = []
        now: datetime = datetime.datetime.now(timezone("Asia/Seoul"))
        try:
            cursor: connection.MySQLCursor = self.connection.cursor()

            expired_sql: str = f"SELECT lectureId FROM lectures WHERE lectureStart < STR_TO_DATE('{now.year}-{now.month}-{now.day}', '%Y-%m-%d');"
            cursor.execute(expired_sql)
            expired_lecture_id: list[str] = []
            for lectureId in cursor.fetchall():
                expired_lecture_id.append(lectureId[0])
            if len(expired_lecture_id) > 0:
                for expired in expired_lecture_id:
                    delete_sql: str = f"DELETE FROM lectures WHERE lectureId='{expired}';"
                    cursor.execute(delete_sql)
                    connection.commit()

            lecture_id: str = f"{ClassIdInfos.get_type_by_center_name(info.get_center_name())}_{info.get_center_name()}_{info.get_region()}_{info.get_branch()}%"
            sql: str = f"SELECT url FROM lectures WHERE lectureId LIKE '{lecture_id}';"
            cursor.execute(sql)
            exist_urls: list = []
            for url in cursor.fetchall():
                exist_urls.append(url[0])

            for url in urls:
                if url not in exist_urls:
                    need_crawl_urls.append(url)
                else:
                    continue

        except Exception as e:
            print(e)
        finally:
            self.connection.commit()
        return need_crawl_urls

    def create_train_sample(self, queue: queue.Queue):
        """
        크롤링한 내용을 라벨링 하기 위해 각 센터별 각 카테고리와 각 대상 마다 각각 100개씩 모은다.
        :return:
        """
        centers: list[str] = self.get_all_centers()
        targets: dict = self.all_distinct_target(centers)
        categories: dict = self.all_distinct_category(centers)
        cursor: connection.MySQLCursor = self.connection.cursor()
        train_samples: list = []
        try:
            for center in centers:
                for target in targets[center]:
                    for category in categories[center]:
                        sql: str = f"SELECT title FROM lectures WHERE center='{center}' AND\
                         target='{target}' AND category='{category}' ORDER BY crawledDate DESC LIMIT 1,100;"
                        cursor.execute(sql)
                        for title in cursor.fetchall():
                            sample: dict = dict()
                            sample_list: list[str] = [title[0], center, target, category]
                            sample["title"] = "  @  ".join(sample_list)
                            sample["Classify"] = 0
                            train_samples.append(sample)

            today: datetime = datetime.datetime.now(timezone("Asia/Seoul"))
            path: str = "/crawl/sample/train_sample.json"
            add_json_data(path=path, value=train_samples, how="a")

            queue.put(
                f"train sample 이 생성 되었습니다. 현재 시각은 {today.year}-{today.month}-{today.day} {today.hour}:{today.minute}:{today.second} 입니다. 빠르게 다운 받아 주시기 바랍니다.")
        except Exception as e:
            print(e)
        finally:
            self.connection.commit()
        return

    def get_all_centers(self) -> list[str]:
        centers: list[str] = list()
        cursor: connection.MySQLCursor = self.connection.cursor()
        try:
            sql: str = f"SELECT DISTINCT(center) AS center FROM lectures;"
            cursor.execute(sql)
            for center in cursor.fetchall():
                centers.append(center[0])
        except Exception as e:
            print(e)
        finally:
            self.connection.commit()
        return centers

    def all_distinct_target(self, centers: list[str]) -> dict:
        targets: dict = dict()
        cursor: connection.MySQLCursor = self.connection.cursor()
        try:
            for center in centers:
                center_target: list[str] = []
                sql: str = f"SELECT DISTINCT(target) AS target FROM lectures WHERE center='{center}';"
                cursor.execute(sql)
                for target in cursor.fetchall():
                    center_target.append(target[0])
                targets[center] = center_target
        except Exception as e:
            print(e)
        finally:
            self.connection.commit()
        return targets

    def all_distinct_category(self, centers: list[str]) -> dict:
        categories: dict = dict()
        cursor: connection.MySQLCursor = self.connection.cursor()
        try:
            for center in centers:
                sql: str = f"SELECT DISTINCT(category) AS category FROM lectures WHERE center='{center}';"
                cursor.execute(sql)
                center_category: list[str] = []
                for category in cursor.fetchall():
                    center_category.append(category[0])
                categories[center] = center_category
        except Exception as e:
            print(e)
        finally:
            self.connection.commit()
        return categories
