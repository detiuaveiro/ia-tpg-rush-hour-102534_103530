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

async def moveCursor(websocket, cursor):
    await websocket.send(
        json.dumps({"cmd": "key", "key": "a"})
    ) 

async def agent_loop(server_address="localhost:5500", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        counter = 0
        while True:
            counter += 1
            if counter == 10:
                break
            try:
                print(counter)
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server

                #pprint(state)
                cursor = state.get("cursor")
                grid = state.get("grid")
                m = Map(grid)
                
                d = m.coordinates
                acoords = m.piece_coordinates("A")
                print(d)
                p = SearchProblem(SearchDomain(m), cursor, acoords[0])
                t = SearchTree(p, "breadth")
                print(await t.search())
                print()

                await websocket.send(
                    json.dumps({"cmd": "key", "key": "a"})
                )  # send key command to server - you must implement this send in the AI agent

                # # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                # key = ""
                # for event in pygame.event.get():
                #     if event.type == pygame.QUIT:
                #         pygame.quit()

                #     if event.type == pygame.KEYDOWN:
                #         if event.key == pygame.K_UP:
                #             key = "w"
                #         elif event.key == pygame.K_LEFT:
                #             key = "a"
                #         elif event.key == pygame.K_DOWN:
                #             key = "s"
                #         elif event.key == pygame.K_RIGHT:
                #             key = "d"
                #         elif event.key == pygame.K_SPACE:
                #             key = " "

                #         elif event.key == pygame.K_d:
                #             import pprint

                #             pprint.pprint(state)

                #         await websocket.send(
                #             json.dumps({"cmd": "key", "key": key})
                #         )  # send key command to server - you must implement this send in the AI agent
                #         break
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