# -*- coding: utf-8 -*-
"""
Simple module for searching the sql-alchemy database based
on user queries.
"""
from flask_reddit.threads.models import Thread, Comment
from flask_reddit import db

def search(query, orderby='creation', filter_user=None, search_title=True,
            search_text=True, subreddit=None, limit=100):
    """
    search for threads (and maybe comments in the future)
    """
    if not query:
        return []
    query = query.strip()
    base_query = '%' + query + '%'

    base_qs = Thread.query

    title_clause = Thread.title.like(base_query) if search_title else False
    text_clause = Thread.text.like(base_query) if search_text else False
    # TODO: Searching by subreddit requires joining, leave out for now.
    # subreddit_clause = Thread.subreddit.name.like(subreddit.name) if subreddit else False

    or_clause = db.or_(title_clause, text_clause)

    base_qs = base_qs.filter(or_clause)

    if orderby == 'creation':
        base_qs = base_qs.order_by(db.desc(Thread.created_on))
    elif orderby == 'title':
        base_qs = base_qs.order_by(Thread.title)
    elif orderby == 'numb_comments':
        pass

    base_qs = base_qs.limit(limit)
    return base_qs
