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
        thread = Thread(title=form.title.data, link=form.link.data,
                text=form.text.data, user_id=user_id)
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

@mod.route('/<thread_id>/<thread_title>/', methods=['GET', 'POST'])
def thread_permalink():
    """
    """
    pass

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

