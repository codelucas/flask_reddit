# -*- coding: utf-8 -*-
"""
Utilities for our views and models.
"""
import string
import random
import os
from datetime import datetime

# Instance folder path, make it independent.
INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')

ALLOWED_AVATAR_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def get_current_time():
    return datetime.utcnow()

def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"

    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"

    return str(day_diff/365) + " years ago"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_AVATAR_EXTENSIONS

def id_generator(size=10, chars=string.ascii_letters + string.digits):
    #return base64.urlsafe_b64encode(os.urandom(size))
    return ''.join(random.choice(chars) for x in range(size))

def make_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception, e:
        raise e

