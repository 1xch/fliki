from werkzeug.local import LocalProxy
from .wiki import Wiki
from .views import create_blueprint
from .util import get_config, url_for_wiki, _wiki


_default_config = {
    'BLUEPRINT_NAME': 'wiki',
    'URL_PREFIX': '/wiki',
    'SUBDOMAIN': None,
    'FLASH_MESSAGES': True,
    'EDITABLE': True,
    'SECURABLE': True,
    'MARKUP_PROCESSOR': None,
    'CONTENT_DIR': 'fliki-content',
    'DISPLAY_VIEW': 'wiki/display.html',
    'EDIT_VIEW': 'wiki/editor.html'
}


_default_messages = {
    'MOVE_PAGE_SUCCESS': ('{old_page} was moved to {new_page}', 'success'),
    'MOVE_PAGE_FAIL': ('Unable to move {old_page}', 'error'),
    'EDIT_PAGE_SUCCESS': ('{page} successfully edited', 'success'),
    'EDIT_PAGE_FAIL': ('Unable to edit {page}', 'error'),
    'DELETE_PAGE_SUCCESS': ('{page} sucessfully deleted', 'success'),
    'DELETE_PAGE_FAIL': ('Unable to delete {page}', 'error'),
}


def _context_processor(wiki):
    ctx_prcs = {}
    ctx_prcs.update({'url_for_wiki': url_for_wiki, 'wiki':_wiki})
    return ctx_prcs


def _get_wiki(app, datastore, **kwargs):
    for key, value in get_config(app).items():
        kwargs[key.lower()] = value

    kwargs.update(dict(
            app=app,
            datastore=datastore,
        ))

    wiki = Wiki(**kwargs)
    return wiki


class Fliki(object):
    def __init__(self, app=None, datastore=None, **kwargs):
        self.app = app
        self.datastore = datastore

        if self.app is not None and self.datastore is not None:
            self._wiki = self.init_app(self.app, self.datastore, **kwargs)

    def init_app(self, app, datastore, register_blueprint=True, **kwargs):
        for key, value in _default_config.items():
            app.config.setdefault('WIKI_' + key, value)

        for key, value in _default_messages.items():
            app.config.setdefault('WIKI_MSG_' + key, value)

        wiki = _get_wiki(app, datastore, **kwargs)

        if register_blueprint:
            app.register_blueprint(create_blueprint(wiki, __name__))

        app.extensions['fliki'] = wiki

        self.register_context_processors(app, _context_processor(wiki))

        return wiki

    def register_context_processors(self, app, context_processors):
        app.jinja_env.globals.update(context_processors)

    def __getattr__(self, name):
        return getattr(self._wiki, name, None)
