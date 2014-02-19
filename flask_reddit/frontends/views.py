# -*- coding: utf-8 -*-
"""
"""
from flask import (Blueprint, request, render_template, flash,
    g, session, redirect, url_for)
from werkzeug import check_password_hash, generate_password_hash

from flask_reddit import db
from flask_reddit import search as search_module # don't override function name
from flask_reddit.users.forms import RegisterForm, LoginForm
from flask_reddit.users.models import User
from flask_reddit.threads.models import Thread
from flask_reddit.subreddits.models import Subreddit
from flask_reddit.users.decorators import requires_login

mod = Blueprint('frontends', __name__, url_prefix='')

@mod.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

def home_subreddit():
    return Subreddit.query.get_or_404(1)

def get_subreddits():
    """
    important and widely imported method because a list of
    the top 30 subreddits are present on every page in the sidebar
    """
    subreddits = Subreddit.query.filter(Subreddit.id != 1)[:25]
    return subreddits

def process_thread_paginator(trending=False, rs=None, subreddit=None):
    """
    abstracted because many sources pull from a thread listing
    source (subreddit permalink, homepage, etc)
    """
    threads_per_page = 15
    cur_page = request.args.get('page') or 1
    cur_page = int(cur_page)
    thread_paginator = None

    # if we are passing in a resultset, that means we are just looking to
    # quickly paginate some arbitrary data, no sorting
    if rs:
        thread_paginator = rs.paginate(cur_page, per_page=threads_per_page,
            error_out=True)
        return thread_paginator

    # sexy line of code :)
    base_query = subreddit.threads if subreddit else Thread.query

    if trending:
        thread_paginator = base_query.order_by(db.desc(Thread.votes)).\
        paginate(cur_page, per_page=threads_per_page, error_out=True)
    else:
        thread_paginator = base_query.order_by(db.desc(Thread.hotness)).\
                paginate(cur_page, per_page=threads_per_page, error_out=True)
    return thread_paginator

#@mod.route('/<regex("trending"):trending>/')
@mod.route('/')
def home(trending=False):
    """
    If not trending we order by creation date
    """
    trending = True if request.args.get('trending') else False
    subreddits = get_subreddits()
    thread_paginator = process_thread_paginator(trending)

    return render_template('home.html', user=g.user,
            subreddits=subreddits, cur_subreddit=home_subreddit(),
            thread_paginator=thread_paginator)

@mod.route('/search/', methods=['GET'])
def search():
    """
    Allows users to search threads and comments
    """
    query = request.args.get('query')
    rs = search_module.search(query, orderby='creation', search_title=True,
            search_text=True, limit=100)

    thread_paginator = process_thread_paginator(rs=rs)
    rs = rs.all()
    num_searches = len(rs)
    subreddits = get_subreddits()

    return render_template('home.html', user=g.user,
            subreddits=subreddits, cur_subreddit=home_subreddit(),
            thread_paginator=thread_paginator, num_searches=num_searches)

@mod.route('/login/', methods=['GET', 'POST'])
def login():
    """
    We had to do some extra work to route the user back to
    his or her original place before logging in
    """
    if g.user:
        return redirect(url_for('frontends.home'))

    next = ''
    if request.method == 'GET':
        if 'next' in request.args:
            next = request.args['next']

    form = LoginForm(request.form)
    # make sure data is valid, but doesn't validate password is right
    if form.validate_on_submit():
        # continue where we left off if so
        user = User.query.filter_by(email=form.email.data).first()
        # we use werzeug to validate user's password
        if user and check_password_hash(user.password, form.password.data):
            # the session can't be modified as it's signed,
            # it's a safe place to store the user id
            session['user_id'] = user.id

            if 'next' in request.form and request.form['next']:
                return redirect(request.form['next'])
            return redirect(url_for('frontends.home'))

        flash('Wrong email or password', 'danger')
    return render_template("login.html", form=form, next=next)

@mod.route('/logout/', methods=['GET', 'POST'])
@requires_login
def logout():
    session.pop('user_id', None)
    return redirect(url_for('frontends.home'))

@mod.route('/register/', methods=['GET', 'POST'])
def register():
    """
    """
    next = ''
    if request.method == 'GET':
        if 'next' in request.args:
            next = request.args['next']

    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # create an user instance not yet stored in the database
        user = User(username=form.username.data, email=form.email.data, \
                password=generate_password_hash(form.password.data))
        # Insert the record in our database and commit it
        db.session.add(user)
        db.session.commit()
        # Log the user in, as he now has an id
        session['user_id'] = user.id

        flash('thanks for signing up!', 'success')
        if 'next' in request.form and request.form['next']:
            return redirect(request.form['next'])
        return redirect(url_for('frontends.home'))

    return render_template("register.html", form=form, next=next)

