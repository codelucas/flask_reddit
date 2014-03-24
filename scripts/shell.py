#!/usr/bin/env python2.7
"""
/shell.py will allow you to get a console and enter commands within your flask environment.
"""
import os
import sys
import readline
from pprint import pprint

from flask import *

sys.path.insert(0, '/home/lucas/www/reddit.lucasou.com/reddit-env/flask_reddit')
from flask_reddit import *
from flask_reddit.users.models import *
from flask_reddit.threads.models import *
from flask_reddit.subreddits.models import *
from flask_reddit.threads.models import thread_upvotes, comment_upvotes

os.environ['PYTHONINSPECT'] = 'True'
