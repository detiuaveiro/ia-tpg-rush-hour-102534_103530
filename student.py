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

        previous_level = ""
        cou = 0
        commands = []
        solution = 0
        old_grid = ""
        last_command = ""
        old_search_time = 0
        crazy = 0
        stuck = 0
        while True:
            try:
                state = json.loads(await websocket.recv())  # receive game update, this must be called timely or your game will get out of sync with the server
                
                grid = state.get("grid")
                selected = state.get("selected")
                crazy = detectCrazy(grid, old_grid, selected, state.get("cursor"), state.get("dimensions"), last_command)
                stuck = detectStuck(last_command, grid, old_grid, selected)

                level = state.get("level")
                if crazy:
                    print("Crazy occured at level: " + str(level) + " !")
                if stuck:
                    print("Agent is stuck.")

                if stuck or (crazy and old_search_time < 1) or commands == []:
                    last_command = ""
                    previous_grid = grid
                    if level != previous_level:
                        previous_level = level
                        cou = 0
                    #print("re-calcula " + str(cou) + " " + str(state.get("level")))
                    cou += 1
                    
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
                            cursor_moves, cursor_x, cursor_y = moveCursor(cursor, piece_bounds, selected)
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
                    last_command = c
                    old_search_time -= 0.1
                    await websocket.send(json.dumps({"cmd": "key", "key": c})) # send key command to server - you must implement this send in the AI agent
                    #print("Command sent '" + str(c) + "'")
                old_grid = grid
                old_search_time = search_time
                #print("Last command:" + str(last_command))
            
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