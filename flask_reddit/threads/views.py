# -*- coding: utf-8 -*-
"""
"""
from flask import (Blueprint, request, render_template, flash, g, session,
    redirect, url_for, abort)
from flask_reddit.threads.forms import SubmitForm
from flask_reddit.threads.models import Thread
from flask_reddit.users.models import User
from flask_reddit.subreddits.models import Subreddit
from flask_reddit.frontends.views import get_subreddits
from flask_reddit import db

mod = Blueprint('threads', __name__, url_prefix='/threads')

#######################
#### Threads Views ####
#######################

@mod.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

def meets_thread_criterea(thread):
    """
    """
    if not thread.title:
        flash('You must include a title!', 'danger')
        return False
    if not thread.text and not thread.link:
        flash('You must post either body text or a link!', 'danger')
        return False

    dup_link = Thread.query.filter_by(link=thread.link).first()
    if not thread.text and dup_link:
        flash('someone has already posted the same link as you!', 'danger')
        return False

    return True

@mod.route('/<subreddit_name>/submit/', methods=['GET', 'POST'])
def submit(subreddit_name=None):
    """
    """
    if g.user is None:
        flash('You must be logged in to submit posts!', 'danger')
        return redirect(url_for('frontends.login', next=request.path))
    user_id = g.user.id

    subreddit = Subreddit.query.filter_by(name=subreddit_name).first()
    if not subreddit:
        abort(404)

    form = SubmitForm(request.form)
    if form.validate_on_submit():
        title = form.title.data.strip()
        link = form.link.data.strip()
        text = form.text.data.strip()
        thread = Thread(title=title, link=link, text=text,
                user_id=user_id, subreddit_id=subreddit.id)

        if not meets_thread_criterea(thread):
            return render_template('threads/submit.html', form=form, user=g.user,
                cur_subreddit=subreddit.name)

        db.session.add(thread)
        db.session.commit()
        thread.set_hotness()

        flash('thanks for submitting!', 'success')
        return redirect(url_for('subreddits.permalink', subreddit_name=subreddit.name))
    return render_template('threads/submit.html', form=form, user=g.user,
            cur_subreddit=subreddit, subreddits=get_subreddits())

@mod.route('/delete/', methods=['GET', 'POST'])
def delete():
    """
    """
    pass

@mod.route('/edit/', methods=['GET', 'POST'])
def edit():
    """
    """
    pass

@mod.route('/<subreddit_name>/<thread_id>/<path:title>/', methods=['GET', 'POST'])
def thread_permalink(subreddit_name=None, thread_id=None, title=None):
    """
    """
    thread_id = thread_id or -99
    thread = Thread.query.get_or_404(int(thread_id))
    subreddit = Subreddit.query.filter_by(name=subreddit_name).first()
    subreddits = get_subreddits()
    return render_template('threads/permalink.html', user=g.user, thread=thread,
            cur_subreddit=subreddit, subreddits=subreddits)

##########################
##### Comments Views #####
##########################

@mod.route('/comments/submit/', methods=['GET', 'POST'])
def submit_comment():
    """
    """
    pass

@mod.route('/comments/delete/', methods=['GET', 'POST'])
def delete_comment():
    """
    """
    pass

@mod.route('/comments/<comment_id>/', methods=['GET', 'POST'])
def comment_permalink():
    """
    """
    pass

