#import binascii
#import hashlib
#import os
#import re
#import markdown
#import json
#from functools import wraps
#from flask import (Flask, render_template, flash, redirect, url_for, request, abort)
from werkzeug.local import LocalProxy
from .wiki import Wiki
from .views import create_blueprint
from .util import get_config

# Convenient references
_fliki = LocalProxy(lambda: current_app.extensions['fliki'])


_default_config = {
    'BLUEPRINT_NAME': 'wiki',
    'URL_PREFIX': None,
    'SUBDOMAIN': None,
    'EDITABLE': True,
    'SECURABLE': True,
    'CONTENT_DIR': 'fliki-content',
    'INDEX_URL': '/wiki',
    'DISPLAY_VIEW': 'wiki/display.html',
    'CREATE_VIEW': 'wiki/create.html',
    'MOVE_VIEW': 'wiki/move.html',
    'EDIT_VIEW': 'wiki/editor.html'
}


_default_messages = {}


def _get_wiki(app, **kwargs):
    for key, value in get_config(app).items():
        kwargs[key.lower()] = value

    kwargs.update(dict(
            app=app,
            #_ctxs={},
        ))

    wiki = Wiki(**kwargs)
    return wiki


class Fliki(object):
    def __init__(self, app=None, **kwargs):
        self.app = app

        if self.app is not None:
            self._wiki = self.init_app(app, **kwargs)

    def init_app(self, app, register_blueprint=True, **kwargs):
        for key, value in _default_config.items():
            app.config.setdefault('WIKI_' + key, value)

        for key, value in _default_messages.items():
            app.config.setdefault('WIKI_MSG_' + key, value)

        wiki = _get_wiki(app, **kwargs)

        if register_blueprint:
            app.register_blueprint(create_blueprint(wiki, __name__))

        app.extensions['fliki'] = wiki

        return wiki

    def __getattr__(self, name):
        return getattr(self._wiki, name, None)
