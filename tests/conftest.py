import pytest
from flask import Flask
from flask.ext.fliki import Fliki
import datastore.filesystem
import shutil


def remove_data():
    shutil.rmtree('/tmp/fliki-content')


@pytest.fixture
def app(request):
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['WIKI_URL_PREFIX'] = '/test'
    Fliki(app, datastore=datastore.filesystem.FileSystemDatastore('/tmp/fliki-content'))
    app.extensions['fliki'].put('random_page', "A random page")
    request.addfinalizer(remove_data)
    return app


@pytest.fixture
def client(app):
    return app.test_client()
