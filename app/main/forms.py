#!/usr/bin/env python
# encoding: utf-8
__author__ = 'deng_lingfei'


from flask_wtf import Form
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import NumberRange, UUID

class TopForm(Form):
    rank = IntegerField('Top:',
                       validators=[NumberRange(min=1, message='top must greator than 1')])
    submit = SubmitField('Submit')

class MetaQueryForm(Form):
    metaID = StringField('MetaID:',
                       validators=[UUID(message="metaID like 'ea0244d6-eb53-0ac5-9f34-9e7421593a54' uuid")])
    submit = SubmitField('Query')


