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


async def agent_loop(server_address="localhost:5500", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        previous_grid = ""
        previous_key = ""
        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server

                #pprint(state)
                cursor = state.get("cursor")
                grid = state.get("grid")
                
                if previous_key == " ":
                    selected = state.get("selected")
                    print("Selected:", selected)
                    coords = m.piece_coordinates(selected)[-1]
                    print("Selected coords:", coords)
                    grid = grid.split(" ")[1]
                    i = coords.y * m.grid_size + coords.x + 1
                    limit = (coords.y + 1) * m.grid_size
                    line = grid[i:limit]
                    if line == "o" * len(line):
                        print("sim")
                        result = ["d"] * len(line)
                    key = "S"
                else:
                    if previous_key == "S":
                        key = ""
                        if result:
                            key = result.pop(0)
                            print(key)
                    elif previous_grid != grid:
                        print("calcula")
                        m = Map(grid)
                        coords = m.piece_coordinates("A")
                        p = SearchProblem(SearchDomain(m), cursor, coords)
                        t = SearchTree(p, "breadth")
                        result = t.search()
                        key = " "
                        if result:
                            key = result.pop(0)
                        print(key)

                previous_key = key
                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                )  # send key command to server - you must implement this send in the AI agent

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