# -*- coding: utf-8 -*-
"""
"""
from functools import wraps
from flask import g, flash, redirect, url_for, request

def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash(u'You need to be signed in for this page.')
            return redirect(url_for('frontends.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

