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

### add code here ###

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
        board_layout = [[Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Tile('tile', True)], [StartPipe(1), Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Pipe('junction-t', 0, False), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), \
        Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('locked', False), Tile('tile', True)], \
        [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), EndPipe(3), \
        Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
        Tile('tile', True), Tile('tile', True)]]

        playable_pipes = {'straight': 1, 'corner': 1, 'cross': 1, 'junction-t': 1, 'diagonals': 1, 'over-under': 1}
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################

        ### add code here ###

    # #########################UNCOMMENT THIS FUNCTION WHEN READY#######################
    # def check_win(self):
    #     """
    #     (bool) Returns True  if the player has won the game False otherwise.
    #     """
    #     position = self.get_starting_position()
    #     pipe = self.pipe_in_position(position)
    #     queue = [(pipe, None, position)]
    #     discovered = [(pipe, None)]
    #     while queue:
    #         pipe, direction, position = queue.pop()
    #         for direction in pipe.get_connected(direction):
                
    #             if self.position_in_direction(direction, position) is None:
    #                 new_direction = None 
    #                 new_position = None
    #             else:
    #                 new_direction, new_position = self.position_in_direction(direction, position)
    #             if new_position == self.get_ending_posit(ion() and direction == self.pipe_in_position(
        #                     new_position).get_connected()[0]:
        #                 return True
    
        #             pipe = self.pipe_in_position(new_position)
        #             if pipe is None or (pipe, new_direction) in discovered:
        #                 continue
        #             discovered.append((pipe, new_direction))
        #             queue.append((pipe, new_direction, new_position))
        #     return False
        # #########################UNCOMMENT THIS FUNCTION WHEN READY#######################
    
    
class Tile:
    ID = "tile" # Needs to be dynamically assigned depending on subclass

    def __init__(self, name, selectable = True):
        """ Instantiates a Tile

                Parameters:
                    self (Tile obj): The variable name to store the instance in.
                    selectabe (bool): Whether the tile can be selected by the user.
                    name (str): The name of the tile.

                Returns:
                    Void
        """
        self.__name = name
        self.__selectable = selectable

    def get_name(self):
        """ Returns the name of the tile instance

                Parameters:
                    Tile (obj): an instance of the Tile class

                Returns:
                    str: The name of the tile instance
        """
        return self.__name

    def get_id(self):
        """ Returns the ID of the given Tile instance 

                Parameters:
                    Tile(obj): An instance of the tile class

                Returns:
                    str: The ID of the given Tile instance
        """
        return ID

    def set_select(self, select):
        """ Updated the "selected" status of the given Tile instance

                Parameters:
                    Tile(obj): An instance of the tile class
                    select (bool): The selected status to update the tile instance to.

                Returns:
                    Void             
        """
        self.__selectable = select


    def can_select(self):
        """ Returns whether the given Tile instance can be selected or not.

                Parameters:
                    Tile(obj): An instance of the tile class
                
                Returns:
                    bool: Whether the tile instance is selectable or not.
        """
        return self.__selectable

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
        return self.__str__()


class Pipe(Tile):

    def __init__(self):
        super().__init__()
        self.__orientation = 0

    def get_connected(self, side):
        """ Returns a list containing all of the sides that connect to the given side.

                Parameters:
                    side (str): The side of the pipe 
                    'N', 'S', 'E' or 'W' that is being checked
                    self (Pipe obj): An instance of the pipe (or a child) class.

                Returns:
                    list<str>: a list of characters corresponding to sides of the tile.
        """
        pass

    def rotate(self, direction):
        """ Rotates the given pipe by 90 degrees in the specified direction.

                Parameters: 
                    direction (int): -ve, +ve or zero indicating counter-clockwise,
                    clockwise rotation or no rotation respectively.
                    self (Pipe obj): An instance of the Pipe (or a child) class.

                Returns:
                    Void.
        """
        pass

    def get_orientation(self):
        """ Getter method for the orientation of the pipe 

                Parameters:
                    self (Pipe obj): An instance of the Pipe (or a child) class.

                Returns:
                    int: orientation [0, 1, 2, 3]
        """
        pass

    def __str__(self):
        """Returns the string representation of the Pipe.

                Parameters:
                    self(Pipe obj): An instance of the Pipe class or a child class

                Returns:
                    str: String representing the given instance
        """
        pass

    def __repr__(self):
        """ Same functionality as Pipe.str()"""
        pass




class SpecialPipe(Pipe):

    def __str__(self):
        """Returns the string representation of the Pipe.

                Parameters:
                    self(Pipe obj): An instance of SpecialPipe subclass

                Returns:
                    str: String representing the given instance
        """
        pass

    def __repr__(self):
        """ Same functionality as str(self)"""
        pass



class StartPipe(SpecialPipe):

    def __init__():
        pass


class EndPipe(SpecialPipe):

    def __init__():
        pass


if __name__ == "__main__":
    print("Please run gui.py instead")

