from common import *

# function which simulates moves the cursor needs to make in order to grab the intended piece
# it grabs the piece by the corner which he is closest to
def moveCursor(cursor, piece_bounds, selected):
    cursorx, cursory = cursor
    piecemin_x, piecemax_x, piecemin_y, piecemax_y = piece_bounds
    if math.dist((cursorx, cursory), (piecemax_x, piecemax_y)) < math.dist((cursorx, cursory), (piecemin_x, piecemin_y)):
        closestx = piecemax_x
        closesty = piecemax_y
    else:
        closestx = piecemin_x
        closesty = piecemin_y
        
    path = ""
    if selected != "":
        path += " "
    while (cursorx != closestx or cursory != closesty):
        if cursorx > closestx:
            path += "a"
            cursorx -= 1
        elif cursorx < closestx:
            path += "d"
            cursorx += 1
        
        if cursory > closesty:
            path += "w"
            cursory -= 1
        elif cursory < closesty:
            path += "s"
            cursory += 1
    path += " "
    return path, cursorx, cursory

# function to detect if agent is stuck
def detectStuck(last_command, grid, old_grid, selected):
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
                if (grid[i%dimension + 1] == selected and cursor_x != i%dimension + 1): # this means it is horizontal
                    return 1
                
                elif (grid[i // dimension + 1] == selected and cursor_y != i // dimension + 1): #this means it is vertical
                    return 1
    return 0