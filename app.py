# -*- coding: UTF-8 -*-

import os
from flask import Flask, render_template
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
css = Bundle('normalize.css', '%s.css' % APP_NAME,
             filters=('cssmin',), output='%s.min.css' % APP_NAME)
assets.register('css_all', css)


#@cache.cached(timeout=600)  # 10 mins
@app.route('/')
def index():
    html = render_template('main.html')
    return html_minify(html)
