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
from tree_search import *

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        previous_grid = ""
        previous_level = ""
        while True:
            try:
                state = json.loads(await websocket.recv())  # receive game update, this must be called timely or your game will get out of sync with the server
                grid = state.get("grid")
                level = state.get("level")
                if grid != previous_grid or level != previous_level:
                    m = Matrix(grid)
                    t = SearchTree(m, "breadth")
                    solution = t.search()
                    print(solution)
                    action = solution.pop(0)
                    piece = action[0]
                    minx, maxx, miny, maxy = m.pieces[piece]
                selected = state.get("selected")
                if selected == piece:
                    key = action[1]
                    if solution:
                        action = solution.pop(0) #for next iteration
                elif selected == "":
                    cursor_x, cursor_y = state.get("cursor")
                    if cursor_x > maxx:
                        key = "a"
                    elif cursor_x < minx:
                        key = "d"
                    elif cursor_y > maxy:
                        key = "w"
                    elif cursor_y < miny:
                        key = "s"
                    else:
                        key = " "
                else:
                    key = " "
                # async.sleep(0)
                await websocket.send(json.dumps({"cmd": "key", "key": key}))
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