# -*- coding: utf-8 -*-
"""
All database abstractions for threads and comments
go in this file.

CREATE TABLE `thread_upvotes` (
  `user_id` int(11) DEFAULT NULL,
  `thread_id` int(11) DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `thread_id` (`thread_id`),
  CONSTRAINT `thread_upvotes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`),
  CONSTRAINT `thread_upvotes_ibfk_2` FOREIGN KEY (`thread_id`) REFERENCES `threads_thread` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1

CREATE TABLE `comment_upvotes` (
  `user_id` int(11) DEFAULT NULL,
  `comment_id` int(11) DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `comment_id` (`comment_id`),
  CONSTRAINT `comment_upvotes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`),
  CONSTRAINT `comment_upvotes_ibfk_2` FOREIGN KEY (`comment_id`) REFERENCES `threads_comment` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 |
"""
from flask_reddit import db
from flask_reddit.threads import constants as THREAD
from flask_reddit import utils
from flask_reddit import media
from math import log
import datetime

thread_upvotes = db.Table('thread_upvotes',
    db.Column('user_id', db.Integer, db.ForeignKey('users_user.id')),
    db.Column('thread_id', db.Integer, db.ForeignKey('threads_thread.id'))
)

comment_upvotes = db.Table('comment_upvotes',
    db.Column('user_id', db.Integer, db.ForeignKey('users_user.id')),
    db.Column('comment_id', db.Integer, db.ForeignKey('threads_comment.id'))
)

class Thread(db.Model):
    """
    We will mimic reddit, with votable threads. Each thread may have either
    a body text or a link, but not both.
    """
    __tablename__ = 'threads_thread'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(THREAD.MAX_TITLE))
    text = db.Column(db.String(THREAD.MAX_BODY), default=None)
    link = db.Column(db.String(THREAD.MAX_LINK), default=None)
    thumbnail = db.Column(db.String(THREAD.MAX_LINK), default=None)

    user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))
    subreddit_id = db.Column(db.Integer, db.ForeignKey('subreddits_subreddit.id'))

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    comments = db.relationship('Comment', backref='thread', lazy='dynamic')

    status = db.Column(db.SmallInteger, default=THREAD.ALIVE)

    votes = db.Column(db.Integer, default=1)
    hotness = db.Column(db.Float(15,6), default=0.00)

    def __init__(self, title, text, link, user_id, subreddit_id):
        self.title = title
        self.text = text
        self.link = link
        self.user_id = user_id
        self.subreddit_id = subreddit_id
        self.extract_thumbnail()

    def __repr__(self):
        return '<Thread %r>' % (self.title)

    def get_comments(self, order_by='timestamp'):
        """
        default order by timestamp
        return only top levels!
        """
        if order_by == 'timestamp':
            return self.comments.filter_by(depth=1).\
                order_by(db.desc(Comment.created_on)).all()[:THREAD.MAX_COMMENTS]
        else:
            return self.comments.filter_by(depth=1).\
                order_by(db.desc(Comment.created_on)).all()[:THREAD.MAX_COMMENTS]

    def get_status(self):
        """
        returns string form of status, 0 = 'dead', 1 = 'alive'
        """
        return THREAD.STATUS[self.status]

    def get_age(self):
        """
        returns the raw age of this thread in seconds
        """
        return (self.created_on - datetime.datetime(1970, 1, 1)).total_seconds()

    def get_hotness(self):
        """
        returns the reddit hotness algorithm (votes/(age^1.5))
        """
        order = log(max(abs(self.votes), 1), 10) # Max/abs are not needed in our case
        seconds = self.get_age() - 1134028003
        return round(order + seconds / 45000, 6)

    def set_hotness(self):
        """
        returns the reddit hotness algorithm (votes/(age^1.5))
        """
        self.hotness = self.get_hotness()
        db.session.commit()

    def pretty_date(self, typeof='created'):
        """
        returns a humanized version of the raw age of this thread,
        eg: 34 minutes ago versus 2040 seconds ago.
        """
        if typeof == 'created':
            return utils.pretty_date(self.created_on)
        elif typeof == 'updated':
            return utils.pretty_date(self.updated_on)

    def add_comment(self, comment_text, comment_parent_id, user_id):
        """
        add a comment to this particular thread
        """
        if len(comment_parent_id) > 0:
            # parent_comment = Comment.query.get_or_404(comment_parent_id)
            # if parent_comment.depth + 1 > THREAD.MAX_COMMENT_DEPTH:
            #    flash('You have exceeded the maximum comment depth')
            comment_parent_id = int(comment_parent_id)
            comment = Comment(thread_id=self.id, user_id=user_id,
                    text=comment_text, parent_id=comment_parent_id)
        else:
            comment = Comment(thread_id=self.id, user_id=user_id,
                    text=comment_text)

        db.session.add(comment)
        db.session.commit()
        comment.set_depth()
        return comment

    def get_voter_ids(self):
        """
        return ids of users who voted this thread up
        """
        select = thread_upvotes.select(thread_upvotes.c.thread_id==self.id)
        rs = db.engine.execute(select)
        ids = rs.fetchall() # list of tuples
        return ids

    def has_voted(self, user_id):
        """
        did the user vote already
        """
        select_votes = thread_upvotes.select(
                db.and_(
                    thread_upvotes.c.user_id == user_id,
                    thread_upvotes.c.thread_id == self.id
                )
        )
        rs = db.engine.execute(select_votes)
        return False if rs.rowcount == 0 else True

    def vote(self, user_id):
        """
        allow a user to vote on a thread. if we have voted already
        (and they are clicking again), this means that they are trying
        to unvote the thread, return status of the vote for that user
        """
        already_voted = self.has_voted(user_id)
        vote_status = None
        if not already_voted:
            # vote up the thread
            db.engine.execute(
                thread_upvotes.insert(),
                user_id   = user_id,
                thread_id = self.id
            )
            self.votes = self.votes + 1
            vote_status = True
        else:
            # unvote the thread
            db.engine.execute(
                thread_upvotes.delete(
                    db.and_(
                        thread_upvotes.c.user_id == user_id,
                        thread_upvotes.c.thread_id == self.id
                    )
                )
            )
            self.votes = self.votes - 1
            vote_status = False
        db.session.commit() # for the vote count
        return vote_status

    def extract_thumbnail(self):
        """
        ideally this type of heavy content fetching should be put on a
        celery background task manager or at least a crontab.. instead of
        setting it to run literally as someone posts a thread. but once again,
        this repo is just a simple example of a reddit-like crud application!
        """
        DEFAULT_THUMBNAIL = 'https://reddit.codelucas.com/static/imgs/reddit-camera.png'
        if self.link:
            thumbnail = media.get_top_img(self.link)
        if not thumbnail:
            thumbnail = DEFAULT_THUMBNAIL
        self.thumbnail = thumbnail
        db.session.commit()


class Comment(db.Model):
    """
    This class is here because comments can only be made on threads,
    so it is contained completly in the threads module.

    Note the parent_id and children values. A comment can be commented
    on, so a comment has a one to many relationship with itself.

    Backrefs:
        A comment can refer to its parent thread with 'thread'
        A comment can refer to its parent comment (if exists) with 'parent'
    """
    __tablename__ = 'threads_comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(THREAD.MAX_BODY), default=None)

    user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))
    thread_id = db.Column(db.Integer, db.ForeignKey('threads_thread.id'))

    parent_id = db.Column(db.Integer, db.ForeignKey('threads_comment.id'))
    children = db.relationship('Comment', backref=db.backref('parent',
            remote_side=[id]), lazy='dynamic')

    depth = db.Column(db.Integer, default=1) # start at depth 1

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    votes = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<Comment %r>' % (self.text[:25])

    def __init__(self, thread_id, user_id, text, parent_id=None):
        self.thread_id = thread_id
        self.user_id = user_id
        self.text = text
        self.parent_id = parent_id

    def set_depth(self):
        """
        call after initializing
        """
        if self.parent:
            self.depth = self.parent.depth + 1
            db.session.commit()

    def get_comments(self, order_by='timestamp'):
        """
        default order by timestamp
        """
        if order_by == 'timestamp':
            return self.children.order_by(db.desc(Comment.created_on)).\
                all()[:THREAD.MAX_COMMENTS]
        else:
            return self.comments.order_by(db.desc(Comment.created_on)).\
                all()[:THREAD.MAX_COMMENTS]

    def get_margin_left(self):
        """
        nested comments are pushed right on a page
        -15px is our default margin for top level comments
        """
        margin_left = 15 + ((self.depth-1) * 32)
        margin_left = min(margin_left, 680)
        return str(margin_left) + "px"

    def get_age(self):
        """
        returns the raw age of this thread in seconds
        """
        return (self.created_on - datetime.datetime(1970,1,1)).total_seconds()

    def pretty_date(self, typeof='created'):
        """
        returns a humanized version of the raw age of this thread,
        eg: 34 minutes ago versus 2040 seconds ago.
        """
        if typeof == 'created':
            return utils.pretty_date(self.created_on)
        elif typeof == 'updated':
            return utils.pretty_date(self.updated_on)

    def vote(self, direction):
        """
        """
        pass

    def comment_on(self):
        """
        when someone comments on this particular comment
        """
        pass
