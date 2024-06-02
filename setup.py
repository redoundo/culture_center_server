from setuptools import setup, find_packages

setup(
    name='culturecenter',
    version='0.0.1',
    packages=find_packages(include=['crawl', ".github", "djangoapp", "djangoserver", "scripts", "sample"]),
    install_requires=[
         "pip", "APScheduler", "PyJWT", "firebase-admin", "python-dateutil", "pytz", "django-cors-headers", "Django",
        "mysql-connector-python", "playwright", "requests", "python-dotenv", "djangorestframework", "mysqlclient",
        "python-decouple"
    ]
)


