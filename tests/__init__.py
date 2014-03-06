from __future__ import with_statement
import sys
import os
from flask import Flask, render_template, current_app, g, request, redirect
from flask.ext.fliki import Fliki
import unittest

class FlikiTest(unittest.TestCase):
    def setUp(self):
        a = Flask(__name__)
        self.app = a
        Fliki(self.app)
        self.fliki = a.extensions['fliki']
