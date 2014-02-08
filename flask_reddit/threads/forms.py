# -*- coding: utf-8 -*-
"""
"""
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required

class SubmitForm(Form):
    title = TextField('Title', [Required()])
    text = TextAreaField('Body text')
    link = TextField('Link')
