cd /home/app
docker image build -t crawlers:latest -f Dockerfile .
docker container run -d --name crawl_container --env-file .env -v crawled:/home/app/crawl crawlers:latest
python app.py