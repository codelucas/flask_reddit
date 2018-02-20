# -*- coding: utf-8 -*-
"""
Logic handling user specific input forms such as logins and registration.
"""
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, BooleanField
from flask_wtf.recaptcha import RecaptchaField
from wtforms.validators import Required, EqualTo, Email


class LoginForm(FlaskForm):
    email = TextField('Email address', [Required(), Email()])
    password = PasswordField('Password', [Required()])


class RegisterForm(FlaskForm):
    username = TextField('NickName', [Required()])
    email = TextField('Email address', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    confirm = PasswordField('Repeat Password', [
        Required(),
        EqualTo('password', message='Passwords must match')
    ])
    accept_tos = BooleanField('I accept the Terms of Service.', [Required()])
    recaptcha = RecaptchaField()
