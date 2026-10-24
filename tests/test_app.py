import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
class TestApp(unittest.TestCase):
    def test_demo_and_priority_filter(self):
        app=AppTest.from_file(str(Path(__file__).parents[1]/'app.py'),default_timeout=30).run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(len(app.tabs),3)
        app.multiselect[0].set_value(['High']).run()
        self.assertEqual(len(app.exception),0)
