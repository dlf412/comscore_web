#!/usr/bin/env python
# encoding: utf-8
__author__ = 'deng_lingfei'

from flask import render_template, redirect, url_for, request, make_response, send_file, current_app, abort
from . import main
from .forms import TopForm, MetaQueryForm
from ..models import Url, Meta
from flask_sqlalchemy import Pagination
import os
import sys

def paginate(query, page, per_page=20, error_out=True):
    if error_out and page < 1:
        abort(404)
    limit_c = min(query.count() - (page-1) * per_page, per_page)
    items = query.limit(limit_c).offset((page - 1) * per_page).all()
    if not items and page != 1 and error_out:
        abort(404)
    # No need to count if we're on the first page and there are fewer
    # items than we expected.
    if page == 1 and len(items) < per_page:
        total = len(items)
    else:
        total = query.count()
    return Pagination(query, page, per_page, total, items)

@main.route('/', methods=['GET', 'POST'])
def index():
    top_form = TopForm()
    query_form = MetaQueryForm()

    if top_form.validate_on_submit():
        return redirect(url_for('.top', rank=top_form.rank.data))

    elif query_form.validate_on_submit():
        return redirect(url_for('.meta', uuid=query_form.metaID.data))

    else:
        return render_template('index.html', top_form=top_form, query_form=query_form)


@main.route('/top/')
def top():
    rank = request.args.get('rank', 0)
    try:
        tops = Url.top(rank)
        if not tops:
            tops = Meta.top(rank)
    except Exception:
        tops = Meta.top(rank)
    page = request.args.get('page', 1, type=int)
    pagination = paginate(tops, page, per_page=20, error_out=True)
    tops = pagination.items
    return render_template('top.html', pagination=pagination, rank=rank, tops=tops)


@main.route('/meta/<uuid>')
def meta(uuid):
    try:
        videos = Url.videos(uuid)
        if not videos:
            videos = Meta.videos(uuid)
    except Exception:
        videos = Meta.videos(uuid)
    page = request.args.get('page', 1, type=int)
    pagination = paginate(videos, page, per_page=10, error_out=True)
    videos = pagination.items
    return render_template('meta.html', pagination=pagination, uuid=uuid, videos=videos)


@main.route('/video/')
def video():
    response = 'Bad Argument', 400
    path = request.args.get('path', None)
    url_id = request.args.get('url_id', None)
    meta_id = request.args.get('meta_id', None)
    ad_idc = request.args.get('ad_idc', None)
    if path:
        response = make_response(send_file(path))
        response.headers["Content-disposition"] = "attachment; filename={}".format(
            os.path.basename(path)
        )
        return response
    elif url_id:
        url = Url.query.get_or_404(url_id)
    elif meta_id:
        url = Url.query.filter(meta_id=meta_id, id=Url.brother_id).first_or_404()
    elif ad_idc:
        url = Url.query.filter_by(ad_idc=ad_idc).first_or_404()
    else:
        return response
    response = make_response(send_file(url.video_path))
    response.headers["Content-disposition"] = "attachment; filename={}".format(
        os.path.basename(url.video_path)
    )
    return response


@main.route('/save/')
def videos():
    save_dir = '/home/deng_lingfei/comscore'
    meta_id = request.args.get('meta_id', None)
    videos = Meta.query.filter_by(match_meta=meta_id).all()
    save_path = os.path.join(save_dir, meta_id)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    for video in videos:
        os.system("cp {} {}".format(video.video_path, save_path))

    return "save OK! ", 200






