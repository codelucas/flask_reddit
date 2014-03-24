# Refer to the following link for help:
# http://docs.gunicorn.org/en/latest/settings.html
command = '/home/lucas/www/reddit.lucasou.com/reddit-env/bin/gunicorn'
pythonpath = '/home/lucas/www/reddit.lucasou.com/reddit-env/flask_reddit'
bind = '127.0.0.1:8040'
workers = 1
user = 'lucas'
accesslog = '/home/lucas/logs/reddit.lucasou.com/gunicorn-access.log'
errorlog = '/home/lucas/logs/reddit.lucasou.com/gunicorn-error.log'
