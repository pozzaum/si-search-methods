import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
from spade.template import Template
from Utils.maze_generator import Maze
from Algorithms.dfs_algorithm import DepthFirstSearch

MAZE_DEPTH = 10
MAZE_WIDTH = 10

STATE_RCV_REQUEST = "STATE_RCV_REQUEST"
STATE_INFORM_ROUTE = "STATE_INFORM_ROUTE"

class FSMHandler(FSMBehaviour):
    async def on_start(self):
        print(f"FSM starting at initial state {self.current_state}")

    async def on_end(self):
        print(f"FSM finished at state {self.current_state}")
        if self.agent is not None:
            await self.agent.stop()


class RcvRequest(State):
    async def run(self):
        tolerance = 10.0 
        print(f"RcvRequest Running...")
        request = await self.receive(tolerance)
        if request:
            request.set_metadata("performative", "request")
            print(f"Request succesfully received {format(request.body)}")
            self.set_next_state(STATE_INFORM_ROUTE)
        else:
            print(f"No request received within {tolerance}s")


class InformRoute(State):
    async def run(self):
        print(f"InformRout Running...")

        ngbr = []
        if self.agent is not None:

            mazeClass = self.agent.mazeClass
            row, col = self.agent.index

            ngbr = [
                "C"
                if (mazeClass.maze[row - 1][col] - 1) >= 0 and
                row - 1 >= 0
                else None,

                "B"
                if (mazeClass.maze[row + 1][col] -1) >= 0 and
                row + 1 <= mazeClass.depth - 1
                else None,

                "E"
                if ((mazeClass.maze[row][col - 1] -1)  >= 0) and
                col - 1 >= 0
                else None,

                "D"
                if (mazeClass.maze[row][col + 1] -1)  >= 0 and
                col + 1 <= mazeClass.width - 1
                else None
            ]

            ngbr = [direction for direction in ngbr if direction is not None]

        msg = Message(to="pai@xmpp.lan")     # Instantiate the message
        msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
        msg.body = f"{ngbr}"
        await self.send(msg)
        print(f"Route sent: {ngbr}")                   # Set the message content


class MazeAgent(Agent):
    async def setup(self):
        print(f"Agent {format(str(self.jid))} started")
        self.mazeClass = Maze(MAZE_DEPTH, MAZE_WIDTH)
        self.index = self.mazeClass.entry_index

        fsm = FSMHandler()
        fsm.add_state(name=STATE_RCV_REQUEST, state=RcvRequest(), initial=True)
        fsm.add_state(name=STATE_INFORM_ROUTE, state=InformRoute())
        fsm.add_transition(source=STATE_RCV_REQUEST, dest=STATE_INFORM_ROUTE)
        self.add_behaviour(fsm)


async def main():
    mazeAgent = MazeAgent("labirinto@xmpp.lan", "labirinto")
    await mazeAgent.start(auto_register=True)

    await spade.wait_until_finished(mazeAgent)
    print("Maze agent finished")

if __name__ == "__main__":
    spade.run(main())

