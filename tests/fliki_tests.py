from tests import *

class FlikiBase(FlikiTest):

    def test_base(self):
        self.assertIsNotNone(self.app.extensions['fliki'])
        self.assertEqual(self.fliki, self.app.extensions['fliki'])

    def test_has_index(self):
        r = self._get('/wiki/')
        self.assertNotIn("Title: index\nSummary: base page for wiki", r.data)
        self.assertIn("Welcome to your flask-wiki", r.data)

    def test_new_page(self): pass

    def test_display_page(self): pass

    def test_move_page(self): pass

    def test_delete_page(self): pass
