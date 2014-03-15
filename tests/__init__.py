from __future__ import with_statement
import sys
import os
from flask import Flask, render_template, current_app, g, request, redirect
from flask.ext.fliki import Fliki
from unittest import TestCase
import datastore.filesystem
import shutil

class FlikiTest(TestCase):
    def setUp(self):
        a = Flask(__name__)
        self.app = a
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SECRET_KEY'] = 'secret_key'
        self.app.config['WIKI_URL_PREFIX'] = '/test'
        Fliki(self.app, datastore=datastore.filesystem.FileSystemDatastore('/tmp/fliki-content'))
        self.fliki = a.extensions['fliki']
        self.client = self.app.test_client()
        self.fliki.put('random_page', "A random page")

    def tearDown(self):
        self.app = None
        self.client = None
        shutil.rmtree('/tmp/fliki-content')

    def _get(self, route, content_type=None, follow_redirects=True, headers=None):
        return self.client.get(route, follow_redirects=follow_redirects,
                               content_type=content_type or 'text/html',
                               headers=headers)

    def _post(self, route, data=None, content_type=None, follow_redirects=True, headers=None):
        return self.client.post(route, data=data,
                                follow_redirects=follow_redirects,
                                content_type=content_type or 'application/x-www-form-urlencoded',
                                headers=headers)

    def assertIn(self, member, container, msg=None):
        if hasattr(TestCase, 'assertIn'):
            return TestCase.assertIn(self, member, container, msg)

        return self.assertTrue(member in container)
