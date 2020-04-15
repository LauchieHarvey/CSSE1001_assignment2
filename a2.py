EMPTY_TILE = "tile"
START_PIPE = "start"
END_PIPE = "end"
LOCKED_TILE = "locked"

SPECIAL_TILES = {
    "S": START_PIPE,
    "E": END_PIPE,
    "L": LOCKED_TILE
}

PIPES = {
    "ST": "straight",
    "CO": "corner",
    "CR": "cross",
    "JT": "junction-t",
    "DI": "diagonals",
    "OU": "over-under"
}

# Only works in orientation of 0.
PIPE_CONNECTIONS_AS_LISTS = {
    "straight": {'N': ['S'], 'S': ['N']},
    "corner": {'N': ['E'], 'E': ['N']},

    "cross" : {'N': ['S', 'E', 'W'], "S": ['N', 'E', 'W'],
                'S': ['N', 'E', 'W'], "W": ['N', 'S', 'E']},

    "junction-t": {'N': ['E', 'W'], 'E': ['N', 'S'], 'S': ['S', 'E', 'W']},
    "diagonals": {'N': ['E'], 'E': ['W'], 'S': ['W'], 'W': ['S']},
    "over-under": {'N': ['S'], 'E': ['W'], 'S': ['N'], 'W': ['E']}
}

### add code here ###

BOARD_SIZE = 6

class PipeGame:
    """
    A game of Pipes.
    """
    def __init__(self, game_file='game_1.csv'):
        """
        Construct a game of Pipes from a file name.

        Parameters:
            game_file (str): name of the game file.
        """
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
        self.board_layout = [[Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Tile('tile', True)], [StartPipe(1), Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Pipe('junction-t', 0, False), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), \
        Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('locked', False), Tile('tile', True)], \
        [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), EndPipe(3), \
        Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Tile('tile', True)]]

        self.playable_pipes = {'straight': 1, 'corner': 1, 'cross': 1, 'junction-t': 1, 'diagonals': 1, 'over-under': 1}
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################

        ### add code here ###

        # Function call also sets the starting and ending position variables.
        self.end_pipe_positions() 
        

    def check_win(self):
        """
            (bool) Returns True  if the player has won the game False otherwise.
        """
        position = self.get_starting_position()
        pipe = self.pipe_in_position(position)
        queue = [(pipe, None, position)]
        discovered = [(pipe, None)]
        while queue:
            pipe, direction, position = queue.pop()
            for direction in pipe.get_connected(direction):
                    
                if self.position_in_direction(direction, position) is None:
                    new_direction = None 
                    new_position = None
                else:
                    new_direction, new_position = self.position_in_direction(direction, position)
                if new_position == self.get_ending_posit(ion()) and \
                 direction == self.pipe_in_position(new_position).get_connected()[0]:
                    return True

                pipe = self.pipe_in_position(new_position)
                if pipe is None or (pipe, new_direction) in discovered:
                    continue
                discovered.append((pipe, new_direction))
                queue.append((pipe, new_direction, new_position))
        return False


    def get_board_layout(self):
        """ Getter method for the 2D board layout of the game."""
        return self.board_layout

    def get_playable_pipes(self):
        """ Getter method for the playable pipes dictionary of the game instance."""
        return self.playable_pipes

    def change_playable_amount(self, pipe_name: str, number: int):
        """ Increments the amount of playable pipes for the specified pipe type by number
            
                Parameters:
                    pipe_name (str): The type of pipe (one of those outlined in PIPES dictionary)
                    number (int): The amount to increment the playable amount of the specified pipe by.
                
                Returns:
                    Void.
        """
        playable_pipes[pipe_name] = playable_pipes.get(pipe_name, 0) + number


    def get_pipe(self, position):
        """ Getter method for pipe/tile object at a given position on the game board.

                Parameters:
                    self (PipeGame Obj): An instance of the PipeGame class.
                    position (tuple<int, int>): A tuple in form (row, col) corresponding 
                    to the locations of the tile/pipe in the 2D game list.

                Returns:
                    (Pipe | Tile) obj: If the tile has no Pipe then a tile instance is returned.
                    Otherwise the most specialised instance of the pipe is returned.
        """
        return self.board_layout[position[0]][position[1]]

    def set_pipe(self, pipe, position):
        """ Setter method, sets the tile at the given position to the given pipe. Updates available pipes.

                Parameters:
                    self (PipeGame obj): An instance of the PipeGame class.
                    position (tuple<int, int>): A tuple in form (row, col) corresponding 
                    to the locations of the tile/pipe in the 2D game list.
                    pipe (Pipe obj): An instance of the Pipe class (or a subclass of the pipe class)
    
                Returns:
                    Void.
        """
        self.playable_pipes[pipe.get_name()] -= 1
        self.board_layout[position[0]][position[1]] = pipe

    def pipe_in_position(self, position):
        """ Returns the Pipe instance of the pipe in the given position of the game board if it exists.

                Parameters: 
                    self (PipeGame obj): An instance of the PipeGame class.
                    position (tuple<int, int>): A tuple in form (row, col) corresponding 
                    to the locations of the tile/pipe in the 2D game list.

                Returns:
                    Pipe (obj): The instance of the pipe in the given position
                    None: If the tile doesn't contain a pipe or the position is invalid.
        """
        if position is None:
            return None

        obj_at_position = self.board_layout[position[0]][position[1]]

        if obj_at_position.get_id() in ["pipe", "special_pipe"]:
            return obj_at_position

    def remove_pipe(self, position):
        """ Replaces the pipe with a tile at the given position from the game board.
            
                Parameters:
                    self (PipeGame obj): An instance of the PipeGame class.
                    position (tuple<int, int>): A tuple in form (row, col) corresponding 
                    to the locations of the tile/pipe in the 2D game list.

                Returns:
                    Void.
        """
        old_pipe = self.board_layout[position[0]][position[1]]
        self.playable_pipes[old_pipe.get_name()] += 1
        self.board_layout[position[0]][position[1]] = Tile("tile")



    def position_in_direction(self, direction, position): #  -> tuple<str, tuple<int, int>>
        """ Returns the opposite direciton and the position corresponding to that 
        direction from the given position.

                Parameters:
                    self (PipeGame obj): An instance of the PipeGame class.
                    position (tuple<int, int>): A tuple in form (row, col) corresponding 
                    to the location of the old tile/pipe in the 2D game list.

                Returns:
                    tuple<char, tuple<int, int>>: A tuple with the opposite direction as a char
                    at index 0 and a tulpe containing the new position (row, col) at index 1
                    None: If the position is invalid.
        """
        board_height = len(self.board_layout)

        if direction not in "NESW":
            return None

        # Using a relative position hashing to convert old pos to new pos given direction.
        pos_update_dict = {'N': (1, 0), 'S': (-1, 0) , 'E': (0, 1), 'W': (0, -1)}
        position = sum(i for i in zip(position, pos_update_dict.get(direction)))

        # Use static method from Pipe class to flip the direction.
        direction = Pipe.convert_orientation(direction, 0, 2)

        # Filter for invalid position
        if (BOARD_SIZE - 1 < position[0] < 0) or (BOARD_SIZE - 1 < position[1] < 0):
            return None

        return tuple(direction, position)



    # time: O(n) worst case despite two for loops.
    def end_pipe_positions(self):
        self._starting_position = None
        self._ending_position = None
        for row_num, row in enumerate(self.board_layout):
            for col_num, tile in enumerate(row):
                # Below if checks if the instance is a special_pipe and that at least one of 
                # the start_pipe/end_pipe hasn't been found yet
                if (tile.get_id() == "special_pipe" and
                    (self._starting_position is None or self._ending_position is None)
                    ):
                    print("\n\nWE GOT THIS FAR.\n\n")
                    if tile._name == "end":
                        self._ending_position = (row_num, col_num)
                    elif tile._name == "start":
                        self._starting_position = (row_num, col_num)


    def get_starting_position(self):
        """ Getter method for the positon of the starting pipe in the board_layout. """
        print("get_starting_position", self._starting_position)
        return self._starting_position


    def get_ending_position(self):
        """ Getter method for the positon of the end pipe in the board_layout. """
        print("get_ending_position", self._ending_position)
        return self._ending_position

    
    
class Tile:

    def __init__(self, name, selectable = True):
        """ Instantiates a Tile

                Parameters:
                    self (Tile obj): The variable name to store the instance in.
                    selectabe (bool): Whether the tile can be selected by the user.
                    name (str): The name of the tile.

                Returns:
                    Void
        """
        self._name = name
        self._selectable = selectable
        self._ID = "tile"

    def get_name(self):
        """ Returns the name of the tile instance

                Parameters:
                    Tile (obj): an instance of the Tile class

                Returns:
                    str: The name of the tile instance
        """
        return self._name

    def get_id(self):
        """ Returns the ID of the given Tile instance 

                Parameters:
                    Tile(obj): An instance of the tile class

                Returns:
                    str: The ID of the given Tile instance
        """
        return self._ID

    def set_select(self, select):
        """ Updated the "selected" status of the given Tile instance

                Parameters:
                    Tile(obj): An instance of the tile class
                    select (bool): The selected status to update the tile instance to.

                Returns:
                    Void             
        """
        self._selectable = select


    def can_select(self):
        """ Returns whether the given Tile instance can be selected or not.

                Parameters:
                    Tile(obj): An instance of the tile class
                
                Returns:
                    bool: Whether the tile instance is selectable or not.
        """
        return self._selectable

    def __str__(self):
        """ Returns the string representation of the given Tile instance

                Parameters:
                    Tile(obj): An instance of the tile class

                Returns:
                    str: String representing the given instance
        """
        return f"Tile('{self.get_name()}', {self.can_select()})"

    def __repr__(self):
        """ Equivalent functionality as __str__ above."""
        return str(self)



class Pipe(Tile):

    def __init__(self, name, orientation = 0, selectable = True):
        super().__init__(name, selectable)
        self._orientation = orientation
        self._ID = "pipe"


    def get_connected(self, side):
        """ Returns a list containing all of the sides that connect to the given side.

                Parameters:
                    side (str): The side of the pipe 
                    'N', 'S', 'E' or 'W' that is being checked
                    self (Pipe obj): An instance of the pipe (or a child) class.

                Returns:
                    list<str>: a list of characters corresponding to sides of the tile.
                    empty list if input is invalid or no sides connect.
        """
        standard_side = Pipe.convert_orientation(side, self._orientation, 0)
        standard_connections_dict = PIPE_CONNECTIONS_AS_LISTS.get(self._name, None)
        if standard_connections_dict is None or standard_side is None:
            return []

        standard_connections = standard_connections_dict.get(standard_side)
        if standard_connections is not None:
            return [Pipe.convert_orientation(i, 0, self._orientation) for i in standard_connections]
        else:
            return []


    @staticmethod
    def convert_orientation(current_side, current_orientation, new_orientation = 0):
        """ Static method converts a side to a side in a different orientation."""
        if current_side not in "NSEW":
            return None
        elif current_orientation == new_orientation:
            return current_side

        directions = ["NESW", "WNES", "SWNE", "ESWN"]
        side_index = directions[current_orientation].find(current_side)
        converted_side = directions[new_orientation][side_index]
        return converted_side


    def rotate(self, direction):
        """ Rotates the given pipe by 90 degrees in the specified direction.

                Parameters: 
                    direction (int): -ve, +ve or zero indicating counter-clockwise,
                    clockwise rotation or no rotation respectively.
                    self (Pipe obj): An instance of the Pipe (or a child) class.

                Returns:
                    Void.
        """
        self._orientation += 1 if self._orientation != 3 else -3

    def get_orientation(self):
        """ Getter method for the orientation of the pipe 

                Parameters:
                    self (Pipe obj): An instance of the Pipe (or a child) class.

                Returns:
                    int: orientation [0, 1, 2, 3]
        """
        return self._orientation

    def __str__(self):
        """Returns the string representation of the Pipe.

                Parameters:
                    self(Pipe obj): An instance of the Pipe class or a child class

                Returns:
                    str: String representing the given instance
        """
        return f"Pipe('{self._name}', {self._orientation})"

    def __repr__(self):
        """ Same functionality as Pipe.str()"""
        return str(self)




class SpecialPipe(Pipe):

    def __init__(self, name, orientation = 0):
        super().__init__(name, selectable = False)
        self._ID = "special_pipe"
        self._orientation = orientation


    def __str__(self):
        """Returns the string representation of the Pipe.

                Parameters:
                    self(Pipe obj): An instance of SpecialPipe subclass

                Returns:
                    str: String representing the given instance
        """
        return f"{self.__class__.__name__}({self._orientation})"

    def __repr__(self):
        """ Same functionality as str(self)"""
        return str(self)



class StartPipe(SpecialPipe):

    def __init__(self, orientation = 0):
        super().__init__("start", orientation)

    def get_connected(self, side = None):
        """ Overwritten method from Pipe Superclass. Returns direction of the StartPipe instance.

                Parameters:
                    self (StartPipe obj): An instance of the StartPipe class
                    side (None): Irrelevant in determining the facing direction. 
                    It is only a parameter to avoid extra parameter error.

                Returns:
                    char: The direction that the start pipe is facing (N, S, E or W)
        """
        return "NESW"[self._orientation]


class EndPipe(SpecialPipe):

    def __init__(self, orientation = 0):
        super().__init__("end", orientation)



    def get_connected(self, side = None):
        """ Overwritten method from Pipe Superclass. Returns direction of the EndPipe instance.

                Parameters:
                    self (StartPipe obj): An instance of the StartPipe class
                    side (None): Irrelevant in determining the facing direction. 
                    It is only a parameter to avoid extra parameter error.

                Returns:
                    char: The direction that the start pipe is facing (N, S, E or W)
        """
        return "SWNE"[self._orientation]


if __name__ == "__main__":
    print("Please run gui.py instead")

