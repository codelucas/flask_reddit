#!/usr/bin/env python2.7
"""
This script instantiates critical components of our webapps.
We need at least one home subreddit to get things going.
We also need a first user to admin our first subreddit.
"""
import os
import readline
from pprint import pprint

from flask import *
from werkzeug import check_password_hash, generate_password_hash
from flask_reddit import *

from flask_reddit.users.models import *
from flask_reddit.threads.models import *
from flask_reddit.subreddits.models import *

first_user = User(username='root', email='louyang@uci.edu', \
        password=generate_password_hash('password'))

db.session.add(first_user)
db.session.commit()

first_subreddit = Subreddit(name='home', desc='Welcome to Reddit! Here is our homepage.',
        admin_id=first_user.id)

db.session.add(first_subreddit)
db.session.commit()

session.pop('user_id', None)
