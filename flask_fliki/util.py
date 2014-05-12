import re
from flask import current_app, url_for, flash
from werkzeug import LocalProxy


_wiki = LocalProxy(lambda: current_app.extensions['fliki'])


def get_config(app):
    """Conveniently get the security configuration for the specified
    application without the annoying 'WIKI_' prefix.

    :param app: The application to inspect
    """
    items = app.config.items()
    prefix = 'WIKI_'

    def strip_prefix(tup):
        return (tup[0].replace('WIKI_', ''), tup[1])

    return dict([strip_prefix(i) for i in items if i[0].startswith(prefix)])


def config_value(key, app=None, default=None):
    """Get a configuration value.
    :param key: The configuration key without the prefix `WIKI_`
    :param app: An optional specific application to inspect. Defaults to Flask's
    `current_app`
    :param default: An optional default value if the value is not set
    """
    app = app or current_app
    return get_config(app).get(key.upper(), default)


def get_wiki_endpoint_name(endpoint):
    return '{}.{}'.format(_wiki.blueprint_name, endpoint)


def url_for_wiki(endpoint, **values):
    """Return a URL for the wiki blueprint

    :param endpoint: the endpoint of the URL (name of the function)
    :param values: the variable arguments of the URL rule
    :param _external: if set to `True`, an absolute URL is generated. Server
    address can be changed via `SERVER_NAME` configuration variable which
    defaults to `localhost`.
    :param _anchor: if provided this is added as anchor to the URL.
    :param _method: if provided this explicitly specifies an HTTP method.
    """
    endpoint = get_wiki_endpoint_name(endpoint)
    return url_for(endpoint, **values)


def clean_url(url):
    if url:
        url_core = re.compile("{!s}|edit/|edit".format(_wiki.url_prefix))
        return re.sub(url_core, "", url)
    return None


def flash_next(message, **kwargs):
    return do_flash(*get_message(message, **kwargs))


def do_flash(message, category=None):
    """Flash a message depending on if the `FLASH_MESSAGES` configuration
    value is set.

    :param message: The flash message
    :param category: The flash message category
    """
    if config_value('FLASH_MESSAGES'):
        flash(message, category)


def get_message(key, **kwargs):
    rv = config_value('MSG_' + key)
    return rv[0].format(**kwargs), rv[1]
