from tests import *

class FlikiBase(FlikiTest):
    def test_base(self):
        self.assertIsNotNone(self.app.extensions['fliki'])
