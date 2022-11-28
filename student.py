"""
Authors:
Rafael Gonçalves (102534)
André Butuc (103530)
"""

import asyncio
import getpass
import json
import os
from pprint import pprint
import websockets
from common import *
from tree_search import *


# for simplicity's sake let's assume the cursor will always select the piece from its maximum x and y coordinates.
async def moveCursor(cursor, piece_bounds, selected):
    cursorx, cursory = cursor
    piecemin_x, piecemax_x, piecemin_y, piecemax_y = piece_bounds
    path = ""
    if selected != "":
        path += " "
    while (cursorx != piecemax_x or cursory != piecemax_y):
        if cursorx > piecemax_x:
            path += "a"
            cursorx -= 1
        elif cursorx < piecemax_x:
            path += "d"
            cursorx += 1
        
        if cursory > piecemax_y:
            path += "w"
            cursory -= 1
        elif cursory < piecemax_y:
            path += "s"
            cursory += 1
    path += " "
    return path, cursorx, cursory


async def detectCrazy(grid, old_grid, selected, cursor, dimensions):
    dimension = dimensions[0]
    if old_grid == "":
        return 0
    
    for i, char in enumerate(grid):
        if (char !=  old_grid[i] and char != "o"):
            if char != selected:
                return 1
            else:
                cursor_x, cursor_y = cursor
                if (grid[i%dimension + 1] == selected and cursor_x != i%dimension + 1): # this means it is horizontal
                    print("shift while selected")
                    return 1
                
                elif (grid[i // dimension + 1] == selected and cursor_y != i // dimension + 1): #this means it is vertical
                    print("shift while selected")
                    return 1
    return 0
    
async def agent_loop(server_address="localhost:5500", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        previous_grid = ""
        previous_level = ""
        cou = 0
        commands = []
        solution = 0
        old_grid = ""
        old_search_time = 0
        crazy = 0
        while True:
            try:
                state = json.loads(await websocket.recv())  # receive game update, this must be called timely or your game will get out of sync with the server
                
                grid = state.get("grid")
                crazy = await detectCrazy(grid, old_grid, state.get("selected"), state.get("cursor"), state.get("dimensions"))
                level = state.get("level")
                if crazy:
                    print("Crazy occured at level: " + str(level) + " !")
                #break
                if (crazy and old_search_time < 1) or commands == []:
                    previous_grid = grid
                    if level != previous_level:
                        previous_level = level
                        cou = 0
                    #print("re-calcula " + str(cou) + " " + str(state.get("level")))
                    cou += 1
                    
                    m = Matrix(grid)
                    t = SearchTree(m, "breadth")
                    start = time()
                    solution = t.search()
                    commands = []
                    selected = state.get("selected")
                    cursor = state.get("cursor")
                    #print("Solution: " + str(solution))
                    #print("Cursor Initial State: " + str(cursor))
                    while solution != []:
                        action = solution.pop(0)
                        piece = action[0]
                        piece_bounds = m.pieces[piece]
                        command = action[1]
                        if selected != piece:
                            #print("Piece to be selected: " + str(piece) + " with bounds: " + str(piece_bounds))
                            cursor_moves, cursor_x, cursor_y = await moveCursor(cursor, piece_bounds, selected)
                            #print("Cursor Moves: " + str(cursor_moves))
                            commands += list(cursor_moves)
                            selected = piece
                        commands += command
                        if command == "w":
                            cursor_y -= 1
                            m.set_bounds(selected, tuple(map(sum, zip(piece_bounds,(0, 0, -1, -1)))))
                        elif command == "s":
                            cursor_y += 1
                            m.set_bounds(selected, tuple(map(sum, zip(piece_bounds,(0, 0, 1, 1)))))
                        elif command == "a":
                            cursor_x -= 1
                            m.set_bounds(selected, tuple(map(sum, zip(piece_bounds,(-1, -1, 0, 0)))))
                        elif command == "d":
                            cursor_x += 1
                            m.set_bounds(selected, tuple(map(sum, zip(piece_bounds,(1, 1, 0, 0)))))
                        cursor = (cursor_x, cursor_y)
                        #print("Fake Cursor: " + str(cursor))
                    search_time = time() - start
                    print("Time taken to reach solution and commands: " + str(search_time))
                    if search_time >= 0.1:
                        print("De-sync")
                        print("N Fake commands: " + str(int(search_time // 0.1)))
                        for i in range(int(search_time // 0.1)):
                            commands.insert(0, '')
                    #print("Cursor: " + str(state.get("cursor")))
                    print("Comandos: " + str(commands))

                    
                    #print("Selected Piece: " + str(selected))
                else: 
                    c = commands.pop(0)
                    old_search_time -= 0.1
                    await websocket.send(json.dumps({"cmd": "key", "key": c})) # send key command to server - you must implement this send in the AI agent
                    #print("Command sent '" + str(c) + "'")
                old_grid = grid
                old_search_time = search_time
            
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))

# def grid2dict(grid, cursor):
#     grid = grid.split(" ")[1]
#     n = int(len(grid)**(1/2))
#     d = {}
#     for y in range(n):
#         line = grid[y*n:(y+1)*n]
#         for x in range(n):
#             element = line[x]
#             if element != "o":
#                 if element in d:
#                     d[element].append((x,y))
#                 else:
#                     d[element] = [(x,y)]
#             if cursor == [x,y]:
#                 element = '@'
#             print("{:2s} ".format(element), end="")
#         print()
#     return d
