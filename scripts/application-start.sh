#!/bin/bash
echo "application-start executed!!"
sudo chmod 666 /var/run/docker.sock
cd /home/app
docker image build -t crawlers:latest -f Dockerfile .
docker container run -d --name crawl_container --restart=always --env-file .env -v /home/app/crawl/sample:/crawl/sample crawlers:latest

docker image build -t java-server:latest -f Dockerfile-java .
docker container run -p 8079:8079 -d --name server_container --restart=always --env-file .env -v /home/app/sample:/java-server/sample java-server:latest