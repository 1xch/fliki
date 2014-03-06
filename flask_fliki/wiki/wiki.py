import os
from flask import current_app
from .page import Page

class Wiki(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)

    @property
    def root(self):
        return "{}/{}".format(current_app.root_path, self.content_dir)

    def path(self, url):
        return os.path.join(self.root, "{}.md".format(url))

    def exists(self, url):
        return os.path.exists(self.path(url))

    def get(self, url):
        if self.exists(url):
            return Page(self.default_processor, self.path(url), url)
        return None

    #def get_or_404(self, url):
    #    page = self.get(url)
    #    if page:
    #        return page
    #    abort(404)

    def get_bare(self, url):
        if self.exists(url):
            return False
        return Page(self.default_processor, self.path(url), url, new=True)

    def move(self, url, newurl):
        os.rename(
            os.path.join(self.root, url) + '.md',
            os.path.join(self.root, newurl) + '.md'
        )

    def delete(self, url):
        path = self.path(url)
        if not self.exists(url):
            return False
        print path
        os.remove(path)
        return True

    #def index(self, attr=None):
    #    def _walk(directory, path_prefix=()):
    #        for name in os.listdir(directory):
    #            fullname = os.path.join(directory, name)
    #            if os.path.isdir(fullname):
    #                _walk(fullname, path_prefix + (name,))
    #            elif name.endswith('.md'):
    #                if not path_prefix:
    #                    url = name[:-3]
    #                else:
    #                    url = os.path.join(path_prefix[0], name[:-3])
    #                if attr:
    #                    pages[getattr(page, attr)] = page
    #                else:
    #                    pages.append(Page(fullname, url.replace('\\', '/')))
    #    if attr:
    #        pages = {}
    #    else:
    #        pages = []
    #    _walk(self.root)
    #    if not attr:
    #        return sorted(pages, key=lambda x: x.title.lower())
    #    return pages

    #def get_by_title(self, title):
    #    pages = self.index(attr='title')
    #    return pages.get(title)

    #def get_tags(self):
    #    pages = self.index()
    #    tags = {}
    #    for page in pages:
    #        pagetags = page.tags.split(',')
    #        for tag in pagetags:
    #            tag = tag.strip()
    #            if tag == '':
    #                continue
    #            elif tags.get(tag):
    #                tags[tag].append(page)
    #            else:
    #                tags[tag] = [page]
    #    return tags

    #def index_by_tag(self, tag):
    #    pages = self.index()
    #    tagged = []
    #    for page in pages:
    #        if tag in page.tags:
    #            tagged.append(page)
    #    return sorted(tagged, key=lambda x: x.title.lower())

    #def search(self, term, attrs=['title', 'tags', 'body']):
    #    pages = self.index()
    #    regex = re.compile(term)
    #    matched = []
    #    for page in pages:
    #        for attr in attrs:
    #            if regex.search(getattr(page, attr)):
    #                matched.append(page)
    #                break
    #    return matched
