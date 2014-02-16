#!/usr/bin/env python2.7
"""
/shell.py will allow you to get a console and enter commands within your flask environment.
"""
import os
import readline
from pprint import pprint

from flask import *
from flask_reddit import *

from flask_reddit.users.models import *
from flask_reddit.threads.models import *
from flask_reddit.subreddits.models import *

os.environ['PYTHONINSPECT'] = 'True'
