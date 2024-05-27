FROM python:3.12

WORKDIR /crawl

COPY crawl /crawl

RUN pip install playwright mysql-connector-python python-dotenv python-dateutil requests pytz

ENV DATABASE_NAME=culture_center_db
ENV DATABASE_USERNAME=culturecenter
ENV DATABASE_PORT=7007


CMD ["python3", "crawlingprocess.py"]