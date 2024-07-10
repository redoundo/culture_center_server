#!/bin/bash
sudo chmod 666 /var/run/docker.sock
cd /home/app
docker image build -t crawlers:latest -f Dockerfile .
docker container run -d --name crawl_container --restart=always --env-file .env -v /home/app/crawl/sample:/crawl/sample crawlers:latest

docker image build -t java-server:latest -f Dockerfile-java .
docker container run -p 8079:8079 -d --name server_container --restart=always --env-file .env -v /home/app/sample:/java-server/sample java-server:latest

docker container run -d --name autoheal --restart=always -v /var/run/docker.sock:/var/run/docker.sock -e AUTOHEAL_CONTAINER_LABEL=all -e TZ=Asia/Seoul -e AUTOHEAL_CONTAINER_LABEL=autoheal -e AUTOHEAL_INTERVAL=5 -e AUTOHEAL_START_PERIOD=0 -e AUTOHEAL_DEFAULT_STOP_TIMEOUT=10 -e DOCKER_SOCK=/var/run/docker.sock -e CURL_TIMEOUT=30 willfarrell/autoheal:latest