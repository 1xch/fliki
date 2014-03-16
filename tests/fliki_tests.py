from tests import *

class FlikiBase(FlikiTest):

    def test_base(self):
        self.assertIsNotNone(self.app.extensions['fliki'])
        self.assertEqual(self.fliki, self.app.extensions['fliki'])

    def test_has_index(self):
        r = self._get('/test/')
        self.assertNotIn("Title: index\nSummary: base page for wiki", r.data)
        self.assertIn("Welcome to your flask-wiki", r.data)

    def test_new_page(self):
        r = self._get('/test/test_page/')
        self.assertIn("Edit Page Content", r.data)

    def test_edit_page(self):
        r = self._post('/test/save', data=dict(pagekey='test_page', edit_content='a test_page'))
        self.assertIn("a test_page", r.data)

    def test_display_page(self):
        r = self._get('/test/random_page/')
        self.assertIn("A random page", r.data)

    def test_move_page(self):
        r = self._post('/test/move', data=dict(oldkey='random_page', newkey='a/new/random/page'))
        self.assertIn("A random page", r.data)

    def test_delete_page(self):
        r = self._post('/test/delete', data=dict(delete='random_page'))
        self.assertIn("index", r.data)
