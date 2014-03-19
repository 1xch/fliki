from tests import *

class FlikiBase(FlikiTest):

    def test_base(self):
        self.assertIsNotNone(self.app.extensions['fliki'])
        self.assertEqual(self.fliki, self.app.extensions['fliki'])

    def test_has_index(self):
        r = self._get('/test/')
        self.assertNotIn(b"Title: index\nSummary: base page for wiki", r.data)
        self.assertIn(b"Welcome to your flask-wiki", r.data)

    def test_new_page(self):
        r = self._get('/test/test_page/')
        self.assertIn(b"Edit Page Content", r.data)

    def test_edit_page(self):
        r = self._post('/test/save', data=dict(pagekey='test_page', edit_content='a test_page'))
        self.assertIn(b"a test_page", r.data)

    def test_display_page(self):
        r = self._get('/test/random_page/')
        self.assertIn(b"A random page", r.data)

    def test_move_page(self):
        r1 = self._post('/test/move', data=dict(oldkey='random_page', newkey='new/random_page'))
        r2 = self._get('/test/new/random_page')
        r3 = self._get('/test/random_page')
        self.assertIn(b"A random page", r1.data)
        self.assertEqual(r1.data, r2.data)
        self.assertNotIn(b"A random page", r3.data)


    def test_delete_page(self):
        r = self._post('/test/delete', data=dict(delete='random_page'))
        self.assertIn(b"index", r.data)
