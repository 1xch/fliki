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
        Fliki(self.app, datastore=datastore.filesystem.FileSystemDatastore('/tmp/fliki-content'))
        self.fliki = a.extensions['fliki']
        self.client = self.app.test_client()

    def tearDown(self):
        shutil.rmtree('/tmp/fliki-content')

    def _get(self, route, content_type=None, follow_redirects=None, headers=None):
        return self.client.get(route, follow_redirects=follow_redirects,
                               content_type=content_type or 'text/html',
                               headers=headers)

    def assertIn(self, member, container, msg=None):
        if hasattr(TestCase, 'assertIn'):
            return TestCase.assertIn(self, member, container, msg)

        return self.assertTrue(member in container)
