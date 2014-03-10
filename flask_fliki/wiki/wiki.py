import os
from flask import current_app
import datastore
from markdown import Markdown


class Page(object):
    def __init__(self, k, content, processor):
        self.key = k
        self.content = content
        self.html = processor.convert(self.content)

    def __html__(self):
        return self.html


class Wiki(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)
        if self.markup_processor:
            self.processor = self.markup_processor
        else:
            self.processor = Markdown(extensions=['meta', 'extra', 'sane_lists'])
        self.has_index()

    def has_index(self):
        if not self.exists(self.key("index")):
            self.put('index', "Title: index\nSummary: base page for wiki\n\nWelcome to your flask-wiki, index page is blank")

    def key(self, item):
        return datastore.Key(item)

    def exists(self, key):
        return self.datastore.contains(key)

    def get(self, item):
        k = self.key(item)
        if self.exists(k):
            x = self.datastore.get(k)
            return Page(k, x, self.processor)
        return None

    def get_bare(self, url):
        k = self.key(item)
        if self.exists(k):
            return False
        return Page(self.default_processor, k, new=True)

    def put(self, item, contents):
        self.datastore.put(self.key(item), contents)

    def move(self, item, newitem):
        k1, k2 = self.key(item), self.key(newitem)
        if self.exists(k1) and not self.exists(k2):
            i = self.get(k1)
            self.put(k2, i)
            self.delete(k1)

    def delete(self, url):
        k = self.key(item)
        if self.exists(k):
            self.datastore.delete(k)
            return True
        return False
