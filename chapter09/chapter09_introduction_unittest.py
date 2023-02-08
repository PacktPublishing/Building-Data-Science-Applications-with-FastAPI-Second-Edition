import unittest

from chapter09.chapter09_introduction import add


class TestChapter09Introduction(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
