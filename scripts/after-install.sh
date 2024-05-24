#!bin/bash
sudo chmod 666 /var/run/docker.sock
docker system prune -a --force
chmod +x scripts/application-start.sh