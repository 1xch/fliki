import os
import re
from flask import abort, current_app
from markdown import Markdown
from .util import config_value


class Processors(object):
    def __init__(self, content=""):
        self.content = self.pre(content)

    def wikilink(self, html):
        """Processes Wikilink syntax "[[Link]]" within content body.  This is
        intended to be run after the content has been processed by Markdown.

        Accepts Wikilink syntax in the form of [[WikiLink]] or [[url/location|LinkName]].
        Everything is referenced from the base location "/", therefore sub-pages
        need to use the [[page/subpage|Subpage]].

        :param html: string of Post-processed HTML output from Markdown
        """
        link = r"((?<!\<code\>)\[\[([^<].+?) \s*([|] \s* (.+?) \s*)?]])"
        compLink = re.compile(link, re.X | re.U)
        for i in compLink.findall(html):
            title = [i[-1] if i[-1] else i[1]][0]
            url = self.clean_url(i[1])
            formattedLink = u"<a href='{2}{0}'>{1}</a>".format(url, title, '/')
            html = re.sub(compLink, formattedLink, html, count=1)
        return html

    def clean_url(self, url):
        """Cleans the url and corrects various errors.  Removes multiple spaces
        and all leading and trailing spaces.  Changes spaces to underscores and
        makes all characters lowercase.  Also takes care of Windows style
        folders use.

        :param url: URL link string
        """
        pageStub = re.sub('[ ]{2,}', ' ', url).strip()
        pageStub = pageStub.lower().replace(' ', '_')
        pageStub = pageStub.replace('\\\\', '/').replace('\\', '/')
        return pageStub

    def pre(self, content):
        """Content preprocessor.

        :param content: Preprocessed content directly from the file or textarea.
        """
        return content

    def post(self, html):
        """Content post-processor.

        :param html: string of Post-processed HTML output from Markdown
        """
        return self.wikilink(html)

    def out(self):
        """Final content output.  Processes the Markdown, post-processes, and
        Meta data.
        """
        md = Markdown(['codehilite', 'fenced_code', 'meta'])
        html = md.convert(self.content)
        phtml = self.post(html)
        body = self.content.split('\n\n', 1)[1]
        meta = md.Meta
        return phtml, body, meta


class Page(object):
    def __init__(self, path, url, new=False):
        self.path = path
        self.url = url
        self._meta = {}
        if not new:
            self.load()
            self.render()

    def load(self):
        with open(self.path, 'rU') as f:
            self.content = f.read().decode('utf-8')

    def render(self):
        processed = Processors(self.content)
        self._html, self.body, self._meta = processed.out()

    def save(self, update=True):
        folder = os.path.dirname(self.path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(self.path, 'w') as f:
            for key, value in self._meta.items():
                line = u'%s: %s\n' % (key, value)
                f.write(line.encode('utf-8'))
            f.write('\n'.encode('utf-8'))
            f.write(self.body.replace('\r\n', '\n').encode('utf-8'))
        if update:
            self.load()
            self.render()

    @property
    def meta(self):
        return self._meta

    def __getitem__(self, name):
        item = self._meta[name]
        if len(item) == 1:
            return item[0]
        print item
        return item

    def __setitem__(self, name, value):
        self._meta[name] = value

    @property
    def html(self):
        return self._html

    def __html__(self):
        return self.html

    #@property
    #def title(self):
    #    return self['title']

    #@title.setter
    #def title(self, value):
    #    self['title'] = value

    @property
    def tags(self):
        return self['tags']

    @tags.setter
    def tags(self, value):
        self['tags'] = value


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
            return Page(self.path(url), url)
        return None

    def get_or_404(self, url):
        page = self.get(url)
        if page:
            return page
        abort(404)

    def get_bare(self, url):
        if self.exists(url):
            return False
        return Page(self.path(url), url, new=True)

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
