from a2 import *
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


class Test_Pipe_methods(unittest.TestCase):

	def setUp(self):
		self.a_pipe_name = "straight"
		self.a_pipe = Pipe(self.a_pipe_name)

		self.b_pipe_name = "corner"
		self.b_pipe = Pipe(self.b_pipe_name)

		self.c_pipe_name = "corner"
		self.c_pipe = Pipe(self.c_pipe_name, 2)

	def test_inherited_methods(self):
		self.assertEqual(self.a_pipe.get_name(), self.a_pipe_name)
		self.assertEqual(self.a_pipe.get_id(), "pipe")

	def test_str_and_repr(self):
		self.assertEqual(str(self.a_pipe), f"Pipe('{self.a_pipe_name}', {self.a_pipe.get_orientation()})")

	def test_rotate_get_orientation(self):
		"""tests both rotate and get_orientation."""

		self.assertEqual(self.a_pipe.get_orientation(), 0)

		self.a_pipe.rotate(1)
		self.assertEqual(self.a_pipe.get_orientation(), 1)
		self.a_pipe.rotate(1)
		self.a_pipe.rotate(1)
		self.assertEqual(self.a_pipe.get_orientation(), 3)
		self.a_pipe.rotate(1)
		self.assertEqual(self.a_pipe.get_orientation(), 0)

	def test_get_connected(self):
		self.assertEqual(self.a_pipe.get_connected("N"), ['S'])
		self.assertEqual(self.a_pipe.get_connected("L"), [])

		self.assertEqual(self.b_pipe.get_connected("E"), ['N'])
		self.assertEqual(self.b_pipe.get_connected("J"), [])

		self.assertEqual(self.c_pipe.get_connected("N"), [])
		self.assertEqual(self.c_pipe.get_connected("J"), [])


class Test_Special_Pipe_subclass_methods(unittest.TestCase):

	def setUp(self):
		self.a_start_pipe = StartPipe()
		self.a_end_pipe = EndPipe()

	def test_str_repr(self):
		self.assertEqual(str(self.a_start_pipe), "StartPipe(0)")
		self.assertEqual(str(self.a_end_pipe), "EndPipe(0)")
	
	def test_inherited_methods(self):
		self.assertEqual(self.a_start_pipe.get_id(), "special_pipe")
		self.assertEqual(self.a_end_pipe.get_id(), "special_pipe")

	def test_get_connected(self):
		self.assertEqual(self.a_start_pipe.get_connected(), "N")
		self.assertEqual(self.a_end_pipe.get_connected(), "S")

		b_end_pipe = EndPipe(1)
		self.assertEqual(b_end_pipe._orientation, 1)
		self.assertEqual(b_end_pipe.get_connected(), "W")

if __name__ == '__main__':
	unittest.main()