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
async def moveCursor(cursor, piece_bounds, piece_char, selected):
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
    return path


async def agent_loop(server_address="localhost:5500", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        previous_grid = ""
        previous_level = ""
        cou = 0
        commands = []

        while True:
            try:
                state = json.loads(await websocket.recv())  # receive game update, this must be called timely or your game will get out of sync with the server

                grid = state.get("grid")
                level = state.get("level")
                if previous_grid != grid:
                    previous_grid = grid
                    if level != previous_level:
                        previous_level = level
                        cou = 0
                    print("re-calcula " + str(cou) + " " + str(state.get("level")))
                    cou += 1
                    cursor = state.get("cursor")

                    selected = state.get("selected")
                    
                    m = Matrix(grid)
                    t = SearchTree(m, "breadth")
                    result = await t.search()
                    commands = []
                    print("Solução encontrada: " + str(result))
                    if result:
                        key = result.pop(0)
                        if selected != key[0]:
                            print("Piece to be selected: " + str(key[0]) + " with coords: " + str(m.pieces[key[0]]))
                            key_bounds = m.pieces[key[0]]
                            commands += list(await moveCursor(cursor, key_bounds, key[0], selected))
                        commands += key[1]
                    print("Comandos: " + str(commands))
                    print("Cursor: " + str(cursor))
                    print("Selected Piece: " + str(selected))
                     
                if commands != []:     
                    command = commands.pop(0)
                    print("Next command to send '" + str(command) + "'")
                    await websocket.send(json.dumps({"cmd": "key", "key": command})) # send key command to server - you must implement this send in the AI agent
            
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "5500")
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