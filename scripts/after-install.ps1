python install pip
pip install --upgrade pip
pip install --upgrade setuptools
pip install APScheduler Flask PyJWT SQLAlchemy firebase-admin mysql-connector-python requests python-dotenv werkzeug
cd /home/app
docker build -t crawlers:latest -f Dockerfile .
docker run -d --env-file .env -v crawled:/home/app/crawl crawlers:latest