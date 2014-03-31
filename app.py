# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import os
import sass
from ecqopcd import db, tpl
from flask import Flask, render_template, g
from flask.ext.assets import Environment, Bundle
from flask.ext.cache import Cache

APP_NAME = 'ecqopcd'

# a large portion of this code comes from github.com/bfontaine/web-pp


def scss(_in, out, **kw):
    """sass compilation"""
    out.write(sass.compile(string=_in.read()))

app = Flask(__name__)
app.debug = True

## caching
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

## assets
assets = Environment(app)

### CSS
css = Bundle('normalize.css',
             '%s.scss' % APP_NAME,
             filters=(scss, 'cssmin',), output='%s.min.css' % APP_NAME)
assets.register('css_all', css)


@cache.cached(timeout=600)  # 10 minutes
@app.route('/')
def index():
    setattr(g, 'title', 'Est-ce qu’on peut courir demain ?')
    setattr(g, 'data', tpl.tpl_vals())
    return render_template('main.html')
