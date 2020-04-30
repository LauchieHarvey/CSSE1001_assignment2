# A game of pipes :)

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
        self._playable_pipes = {'straight': 0, 'corner': 0, 'cross': 0, 'junction-t': 0, 'diagonals': 0, 'over-under': 0}
        
        self._board_layout = self.load_file(game_file)
        
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
                if new_position == self.get_ending_position() and \
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
        return self._board_layout

    def get_playable_pipes(self):
        """ Getter method for the playable pipes dictionary of the game instance."""
        return self._playable_pipes

    def change_playable_amount(self, pipe_name: str, number: int):
        """ Increments the amount of playable pipes for the specified pipe type by number
            
                Parameters:
                    pipe_name (str): The type of pipe (one of those outlined in PIPES dictionary)
                    number (int): The amount to increment the playable amount of the specified pipe by.
                
                Returns:
                    Void.
        """
        self._playable_pipes[pipe_name] = self._playable_pipes.get(pipe_name, 0) + number


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
        return self._board_layout[position[0]][position[1]]

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
        self._playable_pipes[pipe.get_name()] -= 1
        self._board_layout[position[0]][position[1]] = pipe

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

        obj_at_position = self._board_layout[position[0]][position[1]]

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
        old_pipe = self._board_layout[position[0]][position[1]]
        self._playable_pipes[old_pipe.get_name()] += 1
        self._board_layout[position[0]][position[1]] = Tile("tile")



    def position_in_direction(self, direction, position):
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
        if direction not in "NESW":
            return None

        # Relative position hash table
        pos_update_dict = {'N': (-1, 0), 'S': (1, 0) , 'E': (0, 1), 'W': (0, -1)}
        relative_position = pos_update_dict.get(direction)

        # Add the relative position to the old position.
        position = (position[0] + relative_position[0], position[1] + relative_position[1])

        # Use static method from Pipe class to flip the direction.
        direction = Pipe.convert_orientation(direction, 0, 2)

        board_size = len(self._board_layout)

        # Filter for invalid position
        if (
            (position[0] < 0 or position[0] >= board_size) or
            (position[1] < 0 or position[1] >= board_size)
         ):
            return None

        return (direction, position)


    def load_file(self, game_file):
        """ Takes a .csv file and converts it into the board_layout list.
            Also sets the initial playable pipes dictionary

                Parameters:
                    game_file (.csv): A .csv containing a structure overview
                    of an initial game state

                Returns:
                    list(tile): A list of tile (and relevant subclass) instances 
                    reflecting the structure given in the .csv file.
        """
        board_layout = []

        # Context manager for the game file.
        with open(game_file, 'r') as csv_file:
            # Read rows from the game file into a 3D list split by commas. 
            # Each minimal list represents a tile (tile description).
            file_rows = [row.split(',') for row in csv_file.readlines()]
            # File has been read into a variable so there is no need to keep it open.
        # Skip the last row because the last row contains playable_pipe information
        for row in file_rows[:-1]:
            board_layout.append([])

            for tile_description in row:
                tile_description = tile_description.replace("\n", '')
                # the tile_code is it's key in the PIPES dict or the SPECIAL_TILES dict.
                tile_code = ''.join(char for char in tile_description if not char.isdigit())
                tile_orientation = tile_description.replace(tile_code, '')
                tile_orientation = int(tile_orientation) if tile_orientation else 0

                if tile_code == '#':
                    current_tile = Tile(EMPTY_TILE, True)

                elif SPECIAL_TILES.get(tile_code) is not None:

                    if tile_code == 'S':
                        current_tile = StartPipe(tile_orientation)
                    elif tile_code == 'E':
                        current_tile = EndPipe(tile_orientation)
                    elif tile_code == 'L':
                        current_tile = Tile(LOCKED_TILE, False)

                elif PIPES.get(tile_code) is not None:
                    current_tile_type = PIPES.get(tile_code)
                    current_tile = Pipe(current_tile_type, tile_orientation, False)

                # Add the tile to the board_layout
                board_layout[-1].append(current_tile)

        # Iterate over the playable pipes dictionary and set the 
        # value to corresponding integer given in the last line of the .csv file.
        for pipe_num, pipe in enumerate(self._playable_pipes):
            self.change_playable_amount(pipe, int(file_rows[-1][pipe_num]))

        return board_layout

    # time: O(n) worst case despite two for loops.
    def end_pipe_positions(self):
        """ Finds and saves the positions of special pipes on the game board.

                Parameters:
                    self (PipeGame obj): An instance of the PipeGame class.

                Returns:
                    (tuple<int, int>): A tuple in form (row, col) corresponding 
                    to the location of the old tile/pipe in the 2D game list.
        """
        self._starting_position = None
        self._ending_position = None
        for row_num, row in enumerate(self._board_layout):
            for col_num, tile in enumerate(row):
                # Below if checks if the instance is a special_pipe and that at least one of 
                # the start_pipe/end_pipe hasn't been found yet
                if (tile.get_id() == "special_pipe" and
                    (self._starting_position is None or self._ending_position is None)
                    ):

                    if tile._name == "end":
                        self._ending_position = (row_num, col_num)
                    elif tile._name == "start":
                        self._starting_position = (row_num, col_num)


    def get_starting_position(self):
        """ Getter method for the positon of the starting pipe in the board_layout. """
        return self._starting_position


    def get_ending_position(self):
        """ Getter method for the positon of the end pipe in the board_layout. """
        return self._ending_position

    
    
class Tile:
    """ 
    Class definining Tile objects. Every grid on the board is a instance of the tile object.
    """

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
        return f"Tile('{self.get_name()}', {str(self.can_select())})"

    def __repr__(self):
        """ Equivalent functionality as __str__ above."""
        return str(self)



class Pipe(Tile):
    """ Class defining the Pipe object. Corresponds to a pipe in game."""

    def __init__(self, name, orientation = 0, selectable = True):
        """ Constructor method for Pipe instances"""
        super().__init__(name, selectable)
        self._orientation = orientation
        self._ID = "pipe"

        # Only works in orientation of 0. Static variable.
        Pipe.CONNECTIONS = {
            "straight": {'N': ['S'], 'S': ['N']},
            "corner": {'N': ['E'], 'E': ['N']},

            "cross" : {'N': ['S', 'E', 'W'], 'E': ['N', 'S', 'W'],
                        'S': ['N', 'E', 'W'], "W": ['N', 'S', 'E']},

            "junction-t": {'S': ['E', 'W'], 'E': ['S', 'W'], 'W': ['S', 'E']},
            "diagonals": {'N': ['E'], 'E': ['W'], 'S': ['W'], 'W': ['S']},
            "over-under": {'N': ['S'], 'E': ['W'], 'S': ['N'], 'W': ['E']}
        }

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
        # Convert side to the side it corresponds to if the orientation was 0
        standard_side = Pipe.convert_orientation(side, self._orientation, 0)

        # Find the connections dictionary that is relevant to the pipe.
        standard_connections_dict = Pipe.CONNECTIONS.get(self._name, None)
        if standard_connections_dict is None or standard_side is None:
            return []
        # Get the list of sides that are connected to the standard side.
        standard_connections = standard_connections_dict.get(standard_side)
        if standard_connections is not None:
            # For every standard side in the standard connection list 
            # convert it back to the original orientation and return it
            return [Pipe.convert_orientation(i, 0, self._orientation) for i in standard_connections]
        else:
            return []


    @staticmethod
    def convert_orientation(current_side, current_orientation, new_orientation = 0):
        """ Static method converts a side to a side in a different orientation.
        
                Parameters:
                    current_side (char): in "NSEW", the side at the given orientation.
                    current_orientation (int): The orientation that the side is relative to.
                    new_orientation (int): The orientation that the side is to be 
                    converted to be relative to.

                Returns:
                    (char): The standardised side to an orientation of 0.

            e.g. convert_orientation('E', 1, 0) --> 'N'
                Because at the orientation of 1, east is the top most side.
        """
        if current_side not in "NSEW":
            return None
        elif current_orientation == new_orientation:
            return current_side

        directions = ["NESW", "ESWN", "SWNE", "WNES"]
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
        if direction > 0:
            self._orientation += 1 if self._orientation != 3 else -3
        elif direction < 0:
            self._orientation -= 1 if self._orientation != 0 else -3

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
    """ Abstract class for the two child classes EndPipe and StartPipe.
    """

    def __init__(self, name, orientation = 0):
        """ Constructor method for Special Pipe instances"""
        super().__init__(name, orientation, selectable = False)
        self._ID = "special_pipe"


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
    """ 
    Class defining the attributes of the pipe from which the game starts.
    """

    def __init__(self, orientation = 0):
        """ Constructor method for StartPipe instances"""
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
        return ["NESW"[self._orientation]]


class EndPipe(SpecialPipe):
    """
        Child class of Pipe and SpecialPipe. Defines methods unique for end pipes in the game.
    """

    def __init__(self, orientation = 0):
        """ Constructor method for End Pipe instances"""
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
        return ["SWNE"[self._orientation]]


if __name__ == "__main__":
    print("Please run gui.py instead")

