FROM python:3.11

WORKDIR /crawl

COPY crawler /crawl/crawler
COPY db /crawl/db
COPY resource /crawl/resource
COPY typeclass /crawl/typeclass
COPY crawlingprocess.py /crawl


RUN pip install playwright mysql-connector-python python-dotenv python-dateutil

ENV DATABASE_NAME=culture-centers
ENV DATABASE_USERNAME=culturecenter


ENTRYPOINT ["python", "crawlingprocess.py"]