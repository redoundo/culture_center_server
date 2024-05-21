cd /home/app
docker build -t crawlers:latest -f Dockerfile .
docker run -rm -d --name crawl_container --env-file .env -v crawled:/home/app/crawl crawlers:latest
python app.py