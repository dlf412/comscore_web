#!/usr/bin/env python
# encoding: utf-8
__author__ = 'deng_lingfei'

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors