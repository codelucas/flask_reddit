# -*- coding: utf-8 -*-
"""
"""
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from flask_reddit import db
from flask_reddit.users.models import User
from flask_reddit.users.decorators import requires_login

mod = Blueprint('users', __name__, url_prefix='/users')

@mod.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@mod.route('/me/')
@requires_login
def home_page():
    return render_template('users/profile.html', user=g.user)

