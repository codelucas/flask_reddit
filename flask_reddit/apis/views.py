# -*- coding: utf-8 -*-
"""
All view code for async get/post calls towards the server
must be contained in this file.
"""
from flask import (Blueprint, request, render_template, flash, g,
        session, redirect, url_for, jsonify, abort)
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
    comment_parent_id = request.form['parent_id'] # empty means none

    if not comment_text:
        abort(404)

    thread = Thread.query.get_or_404(int(thread_id))
    comment = thread.add_comment(comment_text, comment_parent_id,
            g.user.id)

    return jsonify(comment_text=comment.text, date=comment.pretty_date(),
            username=g.user.username, comment_id=comment.id,
            margin_left=comment.get_margin_left())

@mod.route('/threads/vote/', methods=['POST'])
@requires_login
def vote_thread():
    """
    Submit votes via ajax
    """
    thread_id = int(request.form['thread_id'])
    user_id = g.user.id

    if not thread_id:
        abort(404)

    thread = Thread.query.get_or_404(int(thread_id))
    vote_status = thread.vote(user_id=user_id)
    return jsonify(new_votes=thread.votes, vote_status=vote_status)

@mod.route('/comments/vote/', methods=['POST'])
@requires_login
def vote_comment():
    """
    Submit votes via ajax
    """
    comment_id = int(request.form['comment_id'])
    user_id = g.user.id

    if not comment_id:
        abort(404)

    comment = Comment.query.get_or_404(int(comment_id))
    comment.vote(user_id=user_id)
    return jsonify(new_votes=comment.get_votes())

