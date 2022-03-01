from unittest import TestCase
from util.hasher import hasher

class TestHasher(TestCase):

    def test_hash(self):
        self.assertEqual(hasher('one'), '49e9fcfb5617aad332d56d58ffd0c7020d29ec1d0d0a03b7d7c47f268820acf3')
        self.assertEqual(hasher(2), 'd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35')
        self.assertEqual(hasher(['1', '2']), '8169cab3831aaa019f12f5b449b10e3dffa012a58703c1cb158fd64c235f7713')
        self.assertEqual(hasher('one', 2), '8b9a6564dfbb14a3790f774ebed314d2eb6b45d66d0c5de21e79d9b0c590fb1c')