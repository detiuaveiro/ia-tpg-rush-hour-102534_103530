from common import *

""" Auxiliary functions for Rush Hour Agent"""


def moveCursor(cursor, piece_bounds, selected):
    """
    moveCursor simulates the cursor behavior of grabbing the the intended piece from its closest bound.

    moveCursor receives as parameters: 
        - cursor - tuple of cursor coordinates
        - piece_bounds - tuple of piece coordinate bounds
        - selected - string with the selected piece, if any.
    
    It returns the tuple (path, cursorx, cursory):
        - path - a string with the moves the cursor needs to make;
        - cursorx - x coordinate of the cursor after path is executed;
        - cursory - the y coordinate of the cursor after path is executed;
    """
    cursorx, cursory = cursor
    piecemin_x, piecemax_x, piecemin_y, piecemax_y = piece_bounds

    # euclidean distance between the cursor's coordinates and the piece coordinates
    if math.dist((cursorx, cursory), (piecemax_x, piecemax_y)) < math.dist((cursorx, cursory), (piecemin_x, piecemin_y)):
        # the closest point is (max_x, max_y)
        closestx = piecemax_x
        closesty = piecemax_y
    else:
        # the closest point is (min_x, min_y)
        closestx = piecemin_x
        closesty = piecemin_y
        
    # init path variable
    path = ""

    # if a car is selected, we must release it before moving the cursor
    if selected != "":
        path += " "

    # while cursor doesn't reach closest piece bound
    while (cursorx != closestx or cursory != closesty):
        if cursorx > closestx:
            # needs to move left
            path += "a"
            cursorx -= 1
        elif cursorx < closestx:
            # needs to move right
            path += "d"
            cursorx += 1
        
        if cursory > closesty:
            # needs to move up
            path += "w"
            cursory -= 1
        elif cursory < closesty:
            # needs to move down
            path += "s"
            cursory += 1
    # final step: select the piece
    path += " "

    return path, cursorx, cursory


def detectStuck(last_command, grid, old_grid, selected):
    """
    Simple function to detect if the command which the agent performed on the selected piece was executed or not.
    """
    if old_grid == "":
        return 0
    if selected != "" and last_command in ['a', 'd', 's', "w"] and grid == old_grid:
        return 1
    return 0

# function to detect crazy car
def detectCrazy(grid, old_grid, selected, cursor, dimensions, last_command):
    dimension = dimensions[0]
    # initial iteration, no crazy car can happen
    if old_grid == "":
        return 0
    
    for i, char in enumerate(grid):
        # check each square and compare with old registed state
        if (char !=  old_grid[i] and char != "o"):
            if char != selected:
                # crazy car occured
                return 1
            else:
                # this means it detected a change in the map and the selected piece is the same
                cursor_x, cursor_y = cursor
                if (grid[i%dimension + 1] == selected and cursor_x != i%dimension + 1): # crazy that horizontally shifted while selected
                    print("HORIZONTALLY SHIFTED")
                    return 1
                
                elif (grid[i // dimension + 1] == selected and cursor_y != i // dimension + 1): # crazy that vertically shifted while selected
                    print("VERTICALLY SHIFTED")
                    return 1
    return 0