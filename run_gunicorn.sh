#!/bin/bash

# cd /home/lucas/www/reddit.codelucas.com/reddit-env;
# source bin/activate;

/home/lucas/www/reddit.codelucas.com/reddit-env/bin/gunicorn -c /home/lucas/www/reddit.codelucas.com/reddit-env/flask_reddit/server/gunicorn_config.py flask_reddit.wsgi;
