"""
Authors:
Rafael Gonçalves (102534)
André Butuc (103530)
"""

import asyncio
import getpass
import json
import os
import websockets
from common import *
from tree_search import *
from auxiliary_functions import moveCursor, detectStuck, detectCrazy

            
    
async def agent_loop(server_address="localhost:5500", agent_name="student"):
    """Rush Hour """
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        commands = [] # list to store commands to send to game engine
        solution = 0  # init solution variable
        old_grid = ""  # used to be able to constantly sensor changes between states
        last_command = ""   # used to detect 
        old_search_time = 0 # init old_search_time variable
        crazy = 0   # init crazy variable
        stuck = 0   # init stuck variable

        while True:
            try:
                state = json.loads(await websocket.recv())  # receive game update, this must be called timely or your game will get out of sync with the server
                
                grid = state.get("grid")
                selected = state.get("selected")
                speed = state.get("game_speed")
                dimensions = state.get("dimensions")
                cursor = state.get("cursor")
                rate = 1/speed
                
                crazy = detectCrazy(grid, old_grid, selected, cursor, dimensions, last_command)
                stuck = detectStuck(last_command, grid, old_grid, selected)


                if stuck or (crazy and old_search_time < 1) or commands == []:
                    last_command = ""
                    
                    m = Matrix(grid)
                    if m.n > 6:                      
                        t = SearchTree(m, "gulosa")
                    else:
                        t = SearchTree(m, "breadth")
                    
                    start = time()
                    if m.n > 6:
                        solution = t.search2()
                    else:
                        solution = t.search()
                    
                    commands = []
    
                    while solution != []:
                        action = solution.pop(0)
                        piece = action[0]
                        piece_bounds = m.pieces[piece]
                        command = action[1]
                        if selected != piece:
                            cursor_moves, cursor_x, cursor_y = moveCursor(cursor, piece_bounds, selected)
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
                    
                    search_time = time() - start

                    if search_time >= rate:
                        for i in range(int(search_time // rate)):
                            commands.insert(0, '')

                else: 
                    c = commands.pop(0)
                    last_command = c
                    old_search_time -= rate
                    await websocket.send(json.dumps({"cmd": "key", "key": c})) # send key command to server - you must implement this send in the AI agent

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