from setuptools import setup, find_packages

setup(
    name='culturecenter',
    version='0.0.1',
    packages=find_packages(include=['appserver', 'crawl', "utils", ".github"]),
    install_requires=[
         "pip", "APScheduler", "Flask", "PyJWT", "SQLAlchemy", "firebase-admin", "python-dateutil", "pytz",
        "mysql-connector-python", "playwright", "requests", "python-dotenv", "werkzeug", "Flask-Cors"
    ]
)


