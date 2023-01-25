from game.common import *

""" Auxiliary functions for Rush Hour Agent"""


def moveCursor(cursor, piece_bounds, selected=None):
    """
    moveCursor simulates the cursor behavior of grabbing the intended piece from its closest bound.

    moveCursor receives as parameters: 
        - cursor - list of cursor coordinates;
        - piece_bounds - tuple of piece coordinate bounds;
        - selected - string with the selected piece, if any;
    
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
    if selected is not None and selected != "":
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


def detectStuck(last_command, grid, old_grid, selected, last_selected):
    """
    Simple function to detect if the command which the agent performed on the selected piece was executed sucessfully or not.

    It takes as parameters:
    * last_command - string with the last recorded command which was sent to the game;
    * grid - string which reflects current state of the game ;
    * old_grid - string which reflects last recorded state of the game;
    * selected - string with currently selected piece, if any;
    * last_selected - string with the last recorded selected piece, if any.

    It returns the boolean value "1" if it is stuck or "0" if it is not stuck.
    """
    if old_grid == "":
        return 0
    if selected != "" and last_command in ['a', 'd', 's', "w"] and grid == old_grid:
        return 1
    if selected == last_selected and last_command == " ":
        return 1
    return 0


def detectCrazy(grid, old_grid, selected, cursor, dimensions, last_command, old_cursor):
    """
    Function to detect if a crazy car has occured.

    It takes as parameters:
    * grid - string which reflects current state of the game;
    * old_grid - string which reflects last recorded state of the game;
    * selected - string with selected piece, if any;
    * cursor - array with the current cursor coordinates;
    * dimensions - array with the dimensions of the grid;
    * last_command - string with the last recorded command which was sent to the game;
    * old_cursor - array with the last recorded state of the cursor coordinates;

    It returns a boolean value "1" when crazy occured and "0" when crazy did not occured.
    """
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
                # so we must check if it occurred an anomaly on the cursor coordinates
                old_cursor_x, old_cursor_y = cursor
                if last_command == "a":
                    old_cursor_x += 1
                elif last_command == "d":
                    old_cursor_x -= 1
                elif last_command == "w":
                    old_cursor_y += 1
                elif last_command == "s":
                    old_cursor_y -= 1

                if old_cursor_x != old_cursor[0] or old_cursor_y != old_cursor[1]:
                    return 1
    
    return 0