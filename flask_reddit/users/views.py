# -*- coding: utf-8 -*-
"""
"""
from flask import (Blueprint, request, render_template, flash, g, session,
    redirect, url_for, abort)

from flask_reddit import db
from flask_reddit.users.models import User
from flask_reddit.frontends.views import get_subreddits
from flask_reddit.users.decorators import requires_login

mod = Blueprint('users', __name__, url_prefix='/users')

@mod.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@mod.route('/<username>/')
def home_page(username=None):
    if not username:
        abort(404)
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    return render_template('users/profile.html', user=g.user, current_user=user,
            subreddits = get_subreddits())

