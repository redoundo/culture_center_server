cd /home/app
docker image build -t crawlers:latest -f Dockerfile .
docker container run -rm -d --name crawl_container --env-file .env -v crawled:/home/app/crawl crawlers:latest
docker image build -t flask-server:latest -f Dockerfile-flask .
docker container run -rm -p 8079:2081 -d --name server_container --env-file .env flask-server:latest