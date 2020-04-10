from a2 import Tile
import unittest

class Test_Tile_methods(unittest.TestCase):

	def setUp(self):
		#a_tile_instance
		self.a_tile_name = '#'
		self.a_tile_can_select = True
		self.a_tile = Tile(self.a_tile_name, self.a_tile_can_select)


	def test_repr_str(self):
		"""Test that __repr__ and __str__ are working"""
	
		self.assertEqual(repr(self.a_tile), f"Tile('{self.a_tile_name}', {self.a_tile_can_select})")
		self.assertEqual(str(self.a_tile), f"Tile('{self.a_tile_name}', {self.a_tile_can_select})")


	def test_get_name(self):
		self.assertEqual(self.a_tile.get_name(), self.a_tile_name)


if __name__ == '__main__':
	unittest.main()