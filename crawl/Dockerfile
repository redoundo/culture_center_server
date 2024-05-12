FROM python:3.11

WORKDIR /crawl

COPY crawler /crawl/crawler
COPY db /crawl/db
COPY resource /crawl/resource
COPY typeclass /crawl/typeclass
COPY crawlingprocess.py /crawl


RUN pip install playwright
RUN pip install mysql-connector-python
RUN pip install python-dotenv
RUN pip install python-dateutil

ENV DATABASE_NAME=culture-centers
ENV DATABASE_USERNAME=culturecenter


ENTRYPOINT ["crawlingprocess.py"]