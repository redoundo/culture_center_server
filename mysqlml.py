import os
import dotenv
from mysql.connector import connection

dotenv.load_dotenv()


class MySql:
    databaseName: str = os.getenv("DATABASE_NAME")
    databasePassword: str = os.getenv("DATABASE_PASSWORD")
    databaseUser: str = os.getenv("DATABASE_USERNAME")
    databaseHost: str = os.getenv("DATABASE_HOST")
    connection: connection.MySQLConnection

    tag: dict[int, any] = {0: [20, 30], 1: [21, 31], 2: [22, 32], 3: [23, 33], 4: [24, 34], 5: [25, 35],
                           6: [11, 31], 7: [14, 35], 8: [15, 32], 9: [19, 34], 10: [17, 33],
                           11: "육아·자녀교육", 12: "음악·악기", 13: "미술·공예", 14: "라이프스타일", 15: "댄스·피트니스",
                           16: "어학", 17: "인문학", 18: "재테크", 19: "요리",
                           20: "공연·놀이", 21: "음악·악기", 22: "신체활동", 23: "교육·체험", 24: "요리", 25: "미술·공예",
                           30: "공연·놀이", 31: "음악·악기", 32: "신체활동", 33: "교육·체험", 34: "요리", 35: "미술·공예"}

    def __init__(self):
        self.connection = connection.MySQLConnection(user=self.databaseUser, database=self.databaseName,
                                                     password=self.databasePassword, host=self.databaseHost)
        return

    def insert_classified_data(self, init_datas: list[str], classified_datas: list[int]):
        row_sql: str = "UPDATE lectures SET "
        cursor: connection.MySQLCursor = self.connection.cursor()
        for classified in classified_datas:
            index: int = classified_datas.index(classified)
            title, name, target, category = init_datas[index].split("  @  ")
            trim_title: str = title.replace("'", "''")
            trim_category: str = category.replace("'", "''")
            where_sql: str = f" WHERE title='{trim_title}' AND center='{name}' AND target='{target}' AND category='{trim_category}';"

            format_targets: dict[int, str] = {1: "adult", 2: "kid", 3: "baby"}
            if classified < 11:
                set_sql: str = f"{format_targets[self.tag[classified][0] // 10]}='{self.tag[self.tag[classified][0]]}', {format_targets[self.tag[classified][1] // 10]}='{self.tag[self.tag[classified][1]]}'"
                sql: str = row_sql + set_sql + where_sql
            else:
                target_number: int = classified // 10
                sql: str = row_sql + f"{format_targets[target_number]}='{self.tag[target_number]}'" + where_sql
            cursor.execute(sql)
            self.connection.commit()
        cursor.close()
        return

    def classify_examples(self) -> list | None:
        sql: str = "SELECT title, center, target, category FROM lectures WHERE adult IS NONE AND kid IS NONE AND baby IS NONE;"
        examples: list = []

        cursor: connection.MySQLCursor = self.connection.cursor()
        cursor.execute(sql)

        for title, center, target, category in cursor.fetchall():
            example: list[str] = [title, center, target, category]
            example_str = "  @  ".join(example)
            examples.append([example_str, 0])

        cursor.close()

        if len(examples) > 1:
            return examples
        else:
            return None

