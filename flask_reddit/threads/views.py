# -*- coding: utf-8 -*-
"""
"""
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask_reddit.threads.forms import SubmitForm
from flask_reddit.threads.models import Thread
from flask_reddit.users.models import User
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
        flash('You must include a title!')
        return False
    if not thread.text and not thread.link:
        flash('You must post either body text or a link!')
        return False

    dup_link = Thread.query.filter_by(link=thread.link).first()
    if not thread.text and dup_link:
        flash('someone has already posted the same link as you!')
        return False

    return True

@mod.route('/submit/', methods=['GET', 'POST'])
def submit():
    """
    """
    if g.user is None:
        flash('You must be logged in to submit posts!')
        return redirect(url_for('frontends.login'))
    user_id = g.user.id

    form = SubmitForm(request.form)
    if form.validate_on_submit():
        title = form.title.data.strip()
        link = form.link.data.strip()
        text = form.text.data.strip()
        thread = Thread(title=title, link=link, text=text,
                user_id=user_id, subreddit_id=1)

        if not meets_thread_criterea(thread):
            return render_template('threads/submit.html', form=form, user=g.user)

        db.session.add(thread)
        db.session.commit()

        flash('thanks for submitting!')
        return redirect(url_for('frontends.home'))
    return render_template('threads/submit.html', form=form, user=g.user)

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

@mod.route('/<thread_id>/<path:title>/', methods=['GET', 'POST'])
def thread_permalink(thread_id=None, title=None):
    """
    """
    thread_id = thread_id or -99
    thread = Thread.query.get_or_404(int(thread_id))
    return render_template('threads/permalink.html', user=g.user, thread=thread)

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

