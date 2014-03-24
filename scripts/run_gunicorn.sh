#!/bin/bash

# cd /home/lucas/www/reddit.lucasou.com/reddit-env;
# source bin/activate;

# the following exec is very important for gunicorn!
# without it supervisord won't work because the "exec" 
# has the effect of keeping gunicorn in the same process ID, 
# rather than forking off a new one, and then doing exec.

# Normally, when you type "gunicorn" in your shell, the 
# shell first creates a new process with fork, and 
# then in the new process, runs exec.
exec /home/lucas/www/reddit.lucasou.com/reddit-env/bin/gunicorn -c /home/lucas/www/reddit.lucasou.com/reddit-env/flask_reddit/server/gunicorn_config.py flask_reddit.wsgi;
