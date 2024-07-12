#!/bin/bash
sudo chmod 666 /var/run/docker.sock
cd /home/app
docker image build -t crawlers:latest -f Dockerfile .
docker container run -d --name crawl_container --env-file .env -v /home/app/crawl/sample:/crawl/sample crawlers:latest

docker image build -t java-server:latest -f Dockerfile-java .
docker container run -p 8079:8079 -d --name server_container --restart always --env-file .env \
--health-cmd='curl -f http://localhost:8079/health/check || kill 1' --health-interval=1m --health-retries=5 --health-timeout=20s\
--health-start-period=3m30s --health-start-interval=1m	\
 -v /var/log/spring_boot:/var/log/spring-boot -v /var/log/nginx:/var/log/nginx \
 -v /home/app/sample:/java-server/sample java-server:latest