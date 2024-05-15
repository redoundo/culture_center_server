python install pip
pip install --upgrade pip
pip install --upgrade setuptools
pip install APScheduler Flask PyJWT SQLAlchemy firebase-admin mysql-connector-python requests
cd /home/app
docker build -t crawlers:latest -f Dockerfile .
docker run -d --env-file .env crawlers:latest