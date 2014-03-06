import re
from markdown import Markdown

class FlikiProcessor(object):
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
