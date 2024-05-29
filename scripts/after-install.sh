#!/bin/bash
echo "after-install executed!!"
sudo chmod 666 /var/run/docker.sock
docker kill crawl_container
docker kill server_container
sudo docker image prune -a --force
sudo docker container prune --force