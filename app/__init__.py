#!/usr/bin/env python
# encoding: utf-8
__author__ = 'deng_lingfei'

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

def calc_width_height(videos):
    video_count = len(videos)
    if video_count <= 5:
        return 300, 240
    elif video_count <= 10:
        return 200, 160
    else:
        return 100, 80

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.add_template_global(calc_width_height, 'calc_width_height')

    return app

