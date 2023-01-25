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
from game.common import *
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
        immut_cursor = "" # used to be able to constantly sensor changes between states
        old_cursor = "" # used to be able to constantly sensor changes between states
        last_selected = "" # used to be able to constantly sensor changes between states
        last_command = ""   # used to detect 
        old_search_time = 0 # init old_search_time variable
        crazy = 0   # init crazy variable
        stuck = 0   # init stuck variable

        while True:
            try:
                state = json.loads(await websocket.recv())  # receive game update
                
                grid = state.get("grid") # retrieves grid from state
                selected = state.get("selected") # retrieves selected piece, if any, from state
                speed = state.get("game_speed") # retrieves speed from state
                dimensions = state.get("dimensions") # retrieves dimensions from state
                cursor = state.get("cursor") # retrives cursor coords from state
                immut_cursor = cursor # copy of cursor coords received from state, since the cursor variable will be manipulated in the next few lines
                rate = 1/speed # calculate rate by which the game engines consumes sent messages (commands)
                
                crazy = detectCrazy(grid, old_grid, selected, cursor, dimensions, last_command, old_cursor) # invoke function to detect crazy cars
                stuck = detectStuck(last_command, grid, old_grid, selected, last_selected) # invoke function to make sure last sent command was executed succesfully.
                
                # when stuck or when crazy occured and we take less than 1 seconds to search for solution or when all commands were consumed, find new solution
                if stuck or (crazy and old_search_time < 1) or commands == []:
                    last_command = "" # reset last_command sent
                    
                    # use greedy strategy for bigger grids
                    if dimensions[0] > 6:
                        m = MatrixForGreedy(grid)
                        t = SearchTree(m, "greedy")
                    # use uniform strategy for smaller grids
                    else:
                        m = Matrix(grid)                    
                        t = SearchTree(m, "uniform")
                    
                    # start timer to track time spent on finding a solution and translating it to cursor moves
                    start = time()
                    if m.n > 6:
                        solution = t.search2()
                    else:
                        solution = t.search3()
                    
                    commands = []

                    # process each action in solution and translate it to cursor moves
                    while solution != []:
                        action = solution.pop(0)
                        piece = action[0]   # get piece char
                        piece_bounds = m.pieces[piece] # get piece bounds
                        command = action[1] # get command char

                        # we need to make sure that the piece we want to move is selected
                        if selected != piece:
                            cursor_moves, cursor_x, cursor_y = moveCursor(cursor, piece_bounds, selected) # invoke function which simulates cursor behaviour of selecting desired piece
                            commands += list(cursor_moves)
                            selected = piece
                        commands += command
                        # simulate cursor executing given command and update cursor and selected piece coordinates
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
                        cursor = [cursor_x, cursor_y] # update cursor coordinates to the simulated situation
                    
                    # stop timer
                    search_time = time() - start
                    
                    # check if while finding solution and translating the agent got out of sync with the server and the game
                    if search_time >= rate:
                        # calculate and insert the necessary empty commands to re-establish sync with the server and the game
                        for i in range(int(search_time // rate)):
                            commands.insert(0, '')

                else: 
                    c = commands.pop(0)
                    last_command = c # variable used for sensoring between states
                    last_selected = selected # variable used for sensoring between states
                    old_search_time -= rate # decrease rate to old_search_time, it will be important when the search time to find solution is bigger than 1 second which can cause infinite loop of crazy car occurances and solution recalculation
                    await websocket.send(json.dumps({"cmd": "key", "key": c})) # send key command to server

                old_grid = grid # used to be able to constantly sensor changes between states
                old_cursor = immut_cursor # used to be able to constantly sensor changes between states
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