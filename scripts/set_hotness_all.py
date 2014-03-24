#!/usr/bin/env python2.7
"""
"""
import os
import sys
sys.path.insert(0, '/home/lucas/www/reddit.lucasou.com/reddit-env/flask_reddit')
import readline
from pprint import pprint

from flask import *
from flask_reddit import *

from flask_reddit.users.models import *
from flask_reddit.threads.models import *
from flask_reddit.subreddits.models import *
from flask_reddit.threads.models import thread_upvotes, comment_upvotes

threads = Thread.query.all()
for thread in threads:
    thread.set_hotness()

import time
print 'Hotness values have been computed for all threads without error on', \
    time.strftime("%H:%M:%S"), \
    time.strftime("%d/%m/%Y")
