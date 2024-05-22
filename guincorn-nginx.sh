#echo $0
#!bin/bash
gunicorn -w 1 --bind 13.125.183.196:8079 wsgi:flask_app
nginx