# -*- coding: utf-8 -*-
"""
"""
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

mod = Blueprint('threads', __name__, url_prefix='/threads')
