#!/bin/bash
echo "after-install executed!!"
sudo chmod 666 /var/run/docker.sock
sudo docker image prune -a --force
sudo docker container prune --force