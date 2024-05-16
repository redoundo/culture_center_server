cd /home/app
python app.py
docker build -t crawlers:latest -f Dockerfile .
docker run -d --name crawl_container --env-file .env -v crawled:/home/app/crawl crawlers:latest