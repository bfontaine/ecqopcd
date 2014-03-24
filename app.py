# -*- coding: UTF-8 -*-

import os
import sass
from ecqopcd import db, tpl
from flask import Flask, render_template, g
from flask.ext.assets import Environment, Bundle
from flask.ext.cache import Cache
from htmlmin.minify import html_minify

APP_NAME = 'ecqopcd'

# a large portion of this code comes from github.com/bfontaine/web-pp


def iife(_in, out, **kw):
    """
    'iife' filter for webassets. It wraps a JS bundle in an IIFE, thus
    preventing global leaks.
    """
    out.write(';!function(){')
    out.write(_in.read())
    out.write('}();')


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

### JS
js = Bundle('%s.js' % APP_NAME,
            filters=(iife, 'closure_js'), output='%s.min.js' % APP_NAME)
assets.register('js_all', js)

### CSS
css = Bundle('normalize.css',
             'ss-forecast.css',
             '%s.scss' % APP_NAME,
             filters=(scss, 'cssmin',), output='%s.min.css' % APP_NAME)
assets.register('css_all', css)

#@cache.cached(timeout=600)  # 10 mins


@app.route('/')
def index():
    setattr(g, 'title', 'ECQPCD?')
    setattr(g, 'data', tpl.tpl_vals())
    html = render_template('main.html')
    return html_minify(html, ignore_comments=False)
