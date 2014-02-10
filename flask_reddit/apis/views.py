# -*- coding: utf-8 -*-
"""
"""
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify
from werkzeug import check_password_hash, generate_password_hash

from flask_reddit import db
from flask_reddit.users.models import User
from flask_reddit.threads.models import Thread, Comment
from flask_reddit.users.decorators import requires_login

mod = Blueprint('apis', __name__, url_prefix='/apis')

@mod.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@mod.route('/comments/submit/', methods=['POST'])
@requires_login
def submit_comment():
    """
    Submit comments via ajax
    """
    thread_id = int(request.form['thread_id'])
    comment_text = request.form['comment_text']
    parent_id = request.form['parent_id'] # empty means none
    if len(parent_id) > 0:
        parent_id = int(parent_id)
        comment = Comment(thread_id=thread_id, user_id=g.user.id,
                text=comment_text, parent_id=parent_id)
    else:
        comment = Comment(thread_id=thread_id, user_id=g.user.id, text=comment_text)
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment_text=comment_text, date=comment.pretty_date(),
            username=g.user.username)

