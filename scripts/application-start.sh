#!/bin/bash
echo "application-start executed!!"
sudo chmod 666 /var/run/docker.sock
cd /home/app
docker image build -t crawlers:latest -f Dockerfile .
docker container run -d --name crawl_container --env-file .env -v /home/app/crawl/sample:/crawl/sample crawlers:latest

docker image build -t django-server:latest -f Dockerfile-django .
docker container run -p 8079:8079 -d --name server_container --env-file .env -v /home/app/sample:/django-server/sample django-server:latest

crontab -e
0 0 1,5,9,13,17,21,23 * ? /usr/bin/python3 /home/app/crawl/checkcrawlerstatus.py