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

	def test_set_select(self):
		# Case 1. Set a selectable tile to not selectable
		Tile.set_select(self.a_tile, False)
		self.assertEqual(self.a_tile.can_select(), False)

		# Case 2. Set a non-selectable tile to selectable
		non_selectable_tile = Tile('Not selectable', False)
		Tile.set_select(non_selectable_tile, True)
		self.assertEqual(non_selectable_tile.can_select(), True)

		# Case 3. Set a non-selectable tile to non-selectable
		non_selectable_tile2 = Tile('Not selectable', False)
		Tile.set_select(non_selectable_tile2, False)
		self.assertEqual(non_selectable_tile2.can_select(), False)

if __name__ == '__main__':
	unittest.main()