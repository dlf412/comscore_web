#!/usr/bin/env python
# encoding: utf-8
__author__ = 'deng_lingfei'

from . import db

class Url(db.Model):

    __tablename__ = 'url'
    id = db.Column(db.Integer, primary_key=True)
    ad_idc = db.Column(db.String(128), nullable=False, unique=True, index=True)
    file_name = db.Column(db.String(256), nullable=False)
    url = db.Column(db.String(2048), nullable=False)
    url_date = db.Column(db.Date, index=True, server_default='0000-00-00', nullable=False)
    domain = db.Column(db.String(256), nullable=False)
    file_md5 = db.Column(db.CHAR(32), index=True)
    csv_file = db.Column(db.String(128), nullable=False)
    csv_file_number = db.Column(db.SmallInteger, server_default='0', nullable=False)
    brother_id = db.Column(db.Integer, server_default='0', nullable=False)
    status = db.Column(db.Enum('new', 'downloading', 'download_failed',
                               'download_success', 'query',
                               'query_sueccess', 'query_failed'),
                        server_default='new', nullable=False)
    error_code = db.Column(db.SmallInteger, nullable=False, server_default='0')
    is_valid_url = db.Column(db.Enum('false', 'true'), nullable=False, server_default='true')
    is_valid_file = db.Column(db.Enum('false', 'true'), server_default='true')
    is_ingested = db.Column(db.Enum('false', 'true'), server_default='false')
    download_speed = db.Column(db.SmallInteger, server_default='0')
    download_count = db.Column(db.SmallInteger, server_default='0')
    file_size = db.Column(db.Integer, server_default="0")
    duration = db.Column(db.SmallInteger, server_default='0')
    video_path = db.Column(db.String(256))
    feature_dir = db.Column(db.String(256))
    query_count = db.Column(db.SmallInteger, server_default='0')
    match_meta = db.Column(db.CHAR(36), index=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP'))
    updated_at = db.Column(db.TIMESTAMP, nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    __table_args__ = (
        db.Index('ix_file_name_domain', 'file_name', 'domain'), #
        {
            "mysql_engine":'InnoDB',
            "mysql_charset":'latin1'
        }
    )
    @classmethod
    def top(cls, n):
        return db.session.query(cls.match_meta, db.func.count('*')).\
            filter(cls.match_meta.isnot(None)).group_by(cls.match_meta).\
            order_by(db.func.count('*').desc()).limit(n).all()

    @classmethod
    def videos(cls, metaID):
        return db.session.query(db.func.distinct(cls.video_path), cls.ad_idc).\
                                filter_by(match_meta=metaID).all()



class Meta(db.Model):
    __tablename__ = 'meta'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(256), nullable=False)
    url_date = db.Column(db.Date, index=True, server_default='0000-00-00', nullable=False)
    video_path = db.Column(db.String(256))
    status = db.Column(db.Enum('new', 'success', 'valid_file', 'failed'))
    is_ingest = db.Column(db.Enum('false', 'true'), server_default='false')
    match_meta = db.Column(db.CHAR(36), index=True)
    error_msg = db.Column(db.BLOB)
    created_at = db.Column(db.TIMESTAMP, nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP'))
    updated_at = db.Column(db.TIMESTAMP, nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    __table_args__ = {"mysql_engine":'InnoDB', "mysql_charset":'latin1'}

    @classmethod
    def top(cls, n):
        if n:
            return db.session.query(cls.match_meta, db.func.count('*')). \
                    filter(cls.match_meta.isnot(None)).group_by(cls.match_meta). \
                    order_by(db.func.count('*').desc()).limit(n)
        else:
            return db.session.query(cls.match_meta, db.func.count('*')). \
                filter(cls.match_meta.isnot(None)).group_by(cls.match_meta). \
                order_by(db.func.count('*').desc())


    @classmethod
    def videos(cls, metaID):
        return db.session.query(db.func.distinct(cls.video_path), cls.file_name).\
                        filter_by(match_meta=metaID)







