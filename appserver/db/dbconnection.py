from sqlalchemy import create_engine, Engine, URL, Connection
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

load_dotenv()


class DbConnection:
    url: URL
    engine: Engine

    def __init__(self):
        self.url = URL.create(drivername=os.getenv("MYSQL_DRIVER_NAME"), username=os.getenv("MYSQL_USER"),
                              host=os.getenv("MYSQL_HOST"), password=os.getenv("MYSQL_PASSWORD"),
                              database=os.getenv("MYSQL_DATABASE"), port=os.getenv("MYSQL_PORT"))
        self.engine = create_engine(self.url, echo=True, pool_size=5)
        return

    def get_session(self) -> Session:
        connection: Connection = self.engine.connect()
        return sessionmaker(bind=connection, autoflush=False, expire_on_commit=True)()
