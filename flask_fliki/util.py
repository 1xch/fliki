from flask import current_app

#def get_url(endpoint_or_url):
#    """Returns a URL if a valid endpoint is found. Otherwise, returns the
#    provided value.
#
#    :param endpoint_or_url: The endpoint name or URL to default to
#    """
#    try:
#        return url_for(endpoint_or_url)
#    except:
#        return endpoint_or_url

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
    """Get a Flask-Security configuration value.
    :param key: The configuration key without the prefix `SECURITY_`
    :param app: An optional specific application to inspect. Defaults to Flask's
    `current_app`
    :param default: An optional default value if the value is not set
    """
    app = app or current_app
    return get_config(app).get(key.upper(), default)
