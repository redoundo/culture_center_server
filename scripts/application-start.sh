#!/bin/bash
echo "application-start executed!!"
sudo chmod 666 /var/run/docker.sock
cd /home/app
docker image build -t crawlers:latest -f Dockerfile .
docker container run -d --name crawl_container --env-file .env -v /home/app/crawl/sample:/crawl/sample crawlers:latest

docker image build -t flask-server:latest -f Dockerfile-flask .
docker container run -p 8077:8077 -d --name server_container --env-file .env -v /home/app/sample:/flask-server/sample flask-server:latest