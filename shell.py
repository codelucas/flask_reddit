#!/usr/bin/env python
"""
/shell.py will allow you to get a console and enter commands within your flask environment.
"""

import os
import readline
from pprint import pprint

from flask import *
from flask_reddit import *

from flask_reddit.users import models
from flask_reddit.threads import models

os.environ['PYTHONINSPECT'] = 'True'
