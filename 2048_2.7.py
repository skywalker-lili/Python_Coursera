"""
Achen's version of 2048 game.
"""

import poc_2048_gui

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # create "bridge_list" that has the same length as "line"
    # but has non-zero tiles moved to beginning with same order 
    bridge_list = []
    for tiles in line:
        if tiles != 0:
            bridge_list.append(tiles)
    listofzeros = [0] * (len(line)-len(bridge_list))
    bridge_list = bridge_list + listofzeros
        
    # iterate tiles in "bridge_list" from starting to end postion to
    # merge values based on its next tiles
    for num in range(len(bridge_list)-1):
        if bridge_list[num] == bridge_list[num+1]:
            bridge_list[num] += bridge_list[num+1]
            bridge_list[num+1] = 0
    
    # repeat first step to shift non-zero tiles in "bridge_list" to its
    # beginning and fill the rest tiles with zeros
    merged_list = []
    for tiles in bridge_list:
        if tiles != 0:
            merged_list.append(tiles)
    listofzeros = [0] * (len(bridge_list)-len(merged_list))
    merged_list = merged_list + listofzeros
    
    return merged_list

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        #self._grid = []
        self._grid = [[0 for dummy_col in range(self._width)] for dummy_row in \
                range(self._height)]
        #self.reset()
        # create initial tiles for four directions
        initial_tiles_up = [] # UP
        for width in range(self._width):
            tile_cord = [0,width]
            initial_tiles_up.append(tile_cord)
        
        initial_tiles_down = [] # DOWN
        for width in range(self._width):
            tile_cord = [self._height-1,width]
            initial_tiles_down.append(tile_cord)
        
        initial_tiles_left = [] # LEFT
        for height in range(self._height):
            tile_cord = [height,0]
            initial_tiles_left.append(tile_cord)
        
        initial_tiles_right = [] # RIGHT
        for height in range(self._height):
            tile_cord = [height,self._width-1]
            initial_tiles_right.append(tile_cord)
        
        # record the initial tiles in a dictionary for future use    
        self._initial_tiles = {
            UP: initial_tiles_up,
            DOWN: initial_tiles_down,
            LEFT: initial_tiles_left,
            RIGHT: initial_tiles_right}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_col in range(self._width)] for dummy_row in \
                range(self._height)]
        self.new_tile()
        self.new_tile()         

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._grid)
    
    def grid_print(self):
        """
        Print the grid in a grid form in console. 
        """
        print
        for dummy_length in range(len(self._grid)):
            print str(self._grid[dummy_length])

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # find the corresponding initial tiles and offset (direction of each traverse step)
        #, given a direction
        if direction == UP:
            initial_tiles = self._initial_tiles[UP]
            offset = OFFSETS[UP]
        elif direction == DOWN:
            initial_tiles = self._initial_tiles[DOWN]
            offset = OFFSETS[DOWN]
        elif direction == LEFT:
            initial_tiles = self._initial_tiles[LEFT]
            offset = OFFSETS[LEFT]
        elif direction == RIGHT:
            initial_tiles = self._initial_tiles[RIGHT]
            offset = OFFSETS[RIGHT]
        else:
            print "Please input only numbers between 1 to 4."
        
        # iterate all corresponding initial tiles
        for initial_tile in initial_tiles:
            # using the OFFSET dict to form a temporary list to record
            # tile values from the grid
            temp_list = []
            temp_cord = [] # a list to record the coordinates of each tile
            if direction == 1 or direction == 2:
                for step in range(self._height):
                    row = initial_tile[0] + step*offset[0]
                    col = initial_tile[1] + step*offset[1]
                    temp_list.append(self._grid[row][col])
                    temp_cord.append([row,col])
            elif direction == 3 or direction == 4:
                for step in range(self._width):
                    row = initial_tile[0] + step*offset[0]
                    col = initial_tile[1] + step*offset[1]
                    temp_list.append(self._grid[row][col])
                    temp_cord.append([row,col])
            
            # merge the temporary list
            merged_list = merge(temp_list)
                
            # return the merged temporary list's values back to gird
            for length in range(len(temp_cord)):
                row = temp_cord[length][0]
                col = temp_cord[length][1]
                self._grid[row][col] = merged_list[length]
        
        # Call new tile to continue the game
        self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # find all zero tiles and record their coordinates in one list
        zeros_grid = []
        for dummy_col in range(self._width):
            for dummy_row in range(self._height):
                if self._grid[dummy_row][dummy_col] == 0:
                    cord_zero = [dummy_row, dummy_col]
                    zeros_grid.append(cord_zero)
        # if zeros_grid has at least one elelment, randomly select a tile to fill
        # in a 4 or 2; otherwise, print "End of the game" and break program
        if len(zeros_grid) == 0:
            print "End of game"
        else:
            import random
            selected_cord = random.randrange(0,len(zeros_grid))
            tile_chance = random.randrange(0,9)
            if tile_chance == 0:
                self._grid[zeros_grid[selected_cord][0]][zeros_grid[selected_cord][1]] = 4
            else:
                self._grid[zeros_grid[selected_cord][0]][zeros_grid[selected_cord][1]] = 2     

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
