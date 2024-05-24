#!/bin/bash
echo "after-install executed!!"
sudo chmod 666 /var/run/docker.sock
docker system prune -a --force