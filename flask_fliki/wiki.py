from datastore.core import Key
from markdown import Markdown


class Page(object):
    def __init__(self, k, content, processor):
        self.key = k
        self.html = processor.convert(content)
        self.meta = processor.Meta
        self.raw = content
        processor.reset()

    def __html__(self):
        return self.html


class Wiki(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)
        if self.markup_processor:
            self.processor = self.markup_processor
        else:
            self.processor = Markdown(['meta', 'extra', 'sane_lists'])
        self.has_index()

    def has_index(self):
        if not self.exists(self.key("index")):
            self.put('index', "Title: index\nSummary: base page for wiki\n\nWelcome to your flask-wiki, index page is blank")

    def key(self, item):
        return Key(item)

    def exists(self, key):
        return self.datastore.contains(key)

    def get(self, item):
        k = self.key(item)
        if self.exists(k):
            content = self.datastore.get(k)
            return Page(k, content, self.processor)
        return None

    def put(self, item, contents):
        k = self.key(item)
        self.datastore.put(k, contents)
        if self.exists(k):
            return True

    def move(self, item, newitem):
        k1, k2 = self.key(item), self.key(newitem)
        if self.exists(k1) and not self.exists(k2):
            i = self.datastore.get(k1)
            self.datastore.put(k2, i)
            self.delete(k1)
            return True

    def delete(self, item):
        k = self.key(item)
        if self.exists(k):
            self.datastore.delete(k)
            return True
        return False
