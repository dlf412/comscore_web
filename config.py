#!/usr/bin/env python
# encoding: utf-8
__author__ = 'deng_lingfei'

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '%#*@(#_!@#$%'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app): pass


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql://mediawise:123@192.168.1.34/comScoreXX'
    FLASKY_POSTS_PER_PAGE = 10

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql://mediawise:123@192.168.1.34/comScoreXX'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql://mediawise:123@192.168.1.34/comScoreXX'


config = {'development': DevelopmentConfig,
          'tesing': TestingConfig,
          'production': ProductionConfig,
          'default': DevelopmentConfig}

