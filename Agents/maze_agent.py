import spade
import asyncio
from spade.agent import Agent
from spade.template import Template
from spade.behaviour import FSMBehaviour, CyclicBehaviour
from spade.message import Message
from Utils.maze_generator import Maze

MAZE_DEPTH = 10
MAZE_WIDTH = 10


class RcvRequest(CyclicBehaviour):
    async def run(self):
        await asyncio.sleep(5.1)
        tolerance = 10.0 
        #print(f"RcvRequest Running...")
        request = await self.receive(tolerance)
        if request is not None:
            print(f"Request succesfully received {format(request.body)}")
        else:
            print(f"No request received within {tolerance}s")


class InformRoute(CyclicBehaviour):
    async def run(self):
        await asyncio.sleep(5.2)
        #print(f"InformRoute Running...")

        ngbr = []
        if self.agent is not None:

            mazeClass = self.agent.mazeClass
            row, col = self.agent.user_index

            ngbr = [
                "E"
                if (col - 1 >= 0) and ((mazeClass.maze[row][col - 1] -1)  >= 0)
                else None,

                "D"
                if (col + 1 <= mazeClass.width - 1) and ((mazeClass.maze[row][col + 1] -1)  >= 0)
                else None,

                "C"
                if (row - 1 >= 0) and ((mazeClass.maze[row - 1][col] - 1) >= 0)
                else None,

                "B"
                if (row + 1 <= mazeClass.depth - 1) and ((mazeClass.maze[row + 1][col] -1) >= 0)
                else None
            ]

            ngbr = [direction for direction in ngbr if direction is not None]

        msg = Message(to="pai@xmpp.lan")     # Instantiate the message
        msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
        msg.body = f"{ngbr}"
        await self.send(msg)
        print(f"Route sent: {ngbr}")                   # Set the message content


class RcvRoute(CyclicBehaviour):
    async def run(self):
        await asyncio.sleep(5.3)
        tolerance = 10.0 
        #print(f"RcvRoute Running...")
        route = await self.receive(tolerance)
        if route is not None:
            print(f"Route succesfully received {format(route.body)}")
            if self.agent is not None:
                self.agent.choosen_route = route.body
        else:
            print(f"No request received within {tolerance}s")


class AckRoute(CyclicBehaviour):
   async def run(self):
        await asyncio.sleep(5.4)
        #print(f"AckRoute Running...")

        ack = None
        if self.agent is not None:
            choosen_route = self.agent.choosen_route
            mazeClass = self.agent.mazeClass

            row, col = self.agent.user_index
            index = self.agent.user_index

            print(f"Current index: {row}, {col}")
            print(f"Choosen route: {choosen_route}")

            match choosen_route:
                case 'E':
                    if (mazeClass.maze[row][col - 1] -1) >= 0 and (col - 1 >= 0):
                        ack = "ok"
                        index = (row, col - 1)
                    else: ack = "nok"

                case 'D':
                    if (mazeClass.maze[row][col + 1] -1) >= 0 and (row + 1 <= mazeClass.width - 1):
                        ack = "ok"
                        index = (row, col + 1)
                    else: ack = "nok"

                case 'C':
                    if (mazeClass.maze[row - 1][col] -1) >= 0 and (row - 1 >= 0):
                        ack = "ok"
                        index = (row - 1, col)
                    else: ack = "nok"

                case 'B':
                    if (mazeClass.maze[row + 1][col] -1) >= 0 and (row + 1 <= mazeClass.depth - 1):
                        ack = "ok"
                        index = (row + 1, col)
                    else: ack = "nok"

            self.agent.user_index = index

        msg = Message(to="pai@xmpp.lan")     # Instantiate the message
        msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
        msg.body = f"{ack}"
        await self.send(msg)
        print(f"Acknowledged sent: {ack}")                   # Set the message content


class RcvQuery(CyclicBehaviour):
    async def run(self):
        await asyncio.sleep(5.5)
        tolerance = 10.0 
        #print(f"RcvQuery Running...")
        obj_chk = await self.receive(tolerance)
        if obj_chk is not None:
            print(f"Obj Query succesfully received {format(obj_chk.body)}")
            if self.agent is not None:
                self.agent.choosen_route = obj_chk.body
        else:
            print(f"No request received within {tolerance}s")


class ChkObj(CyclicBehaviour):
   async def run(self):
        await asyncio.sleep(5.6)
        #print(f"ChkObj Running...")
        chk = "Uninitialized"
        if self.agent is not None:
            mazeClass = self.agent.mazeClass
            row, col = self.agent.user_index

            if (mazeClass.maze[row][col] == 3): 
                chk = "Done"
                self.agent.user_obj = True
            else: 
                chk = "Failure"

        msg = Message(to="pai@xmpp.lan")     # Instantiate the message
        msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
        msg.body = f"{chk}"
        await self.send(msg)
        print(f"Route sent: {chk}")                   # Set the message content


class MazeAgent(Agent):
    async def setup(self):
        print(f"Agent {format(str(self.jid))} started")
        self.mazeClass = Maze(MAZE_DEPTH, MAZE_WIDTH)
        self.user_index = self.mazeClass.entry_index
        self.user_obj = False
        self.choosen_route = None

        template_rcvrqt = Template()
        template_rcvrqt.set_metadata("performative", "request")
        template_rcvrt = Template()
        template_rcvrt.set_metadata("performative", "subscribe")
        template_rcvqr = Template()
        template_rcvqr.set_metadata("performative", "query-if")


        self.add_behaviour(RcvRequest(), template_rcvrqt)
        self.add_behaviour(InformRoute())
        self.add_behaviour(RcvRoute(), template_rcvrt)
        self.add_behaviour(AckRoute())
        self.add_behaviour(RcvQuery(), template_rcvqr)
        self.add_behaviour(ChkObj())


async def main():
    mazeAgent = MazeAgent("labirinto@xmpp.lan", "labirinto")
    await mazeAgent.start(auto_register=True)

    await spade.wait_until_finished(mazeAgent)
    print("Maze agent finished")

if __name__ == "__main__":
    spade.run(main())

