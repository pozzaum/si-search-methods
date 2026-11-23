import spade
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
from Utils.maze_generator import Maze

MAZE_DEPTH = 10
MAZE_WIDTH = 10

STATE_RCV_REQUEST = "STATE_RCV_REQUEST"
STATE_INFORM_ROUTE = "STATE_INFORM_ROUTE"
STATE_RCV_ROUTE = "STATE_RCV_ROUTE"
STATE_ACK_ROUTE = "STATE_ACK_ROUTE"
STATE_RCV_QUERY = "STATE_RCV_QUERY"
STATE_INFORM_OBJ = "STATE_INFORM_OBJ"
STATE_CHK_OBJ = "STATE_CHK_OBJ"


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
        print(f"InformRoute Running...")

        ngbr = []
        if self.agent is not None:

            mazeClass = self.agent.mazeClass
            if self.agent.father_next:
                row, col = self.agent.father_index

            else:
                row, col = self.agent.son_index

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
        self.set_next_state(STATE_RCV_ROUTE)


class RcvRoute(State):
    async def run(self):
        tolerance = 10.0 
        print(f"RcvRoute Running...")
        route = await self.receive(tolerance)
        if route:
            route.set_metadata("performative", "subscribe")
            print(f"Route succesfully received {format(route.body)}")
            if self.agent is not None:
                self.agent.choosen_route = route.body
            self.set_next_state(STATE_ACK_ROUTE)
        else:
            print(f"No request received within {tolerance}s")


class AckRoute(State):
   async def run(self):
        print(f"AckRoute Running...")

        ack = None
        if self.agent is not None:
            choosen_route = self.agent.choosen_route
            mazeClass = self.agent.mazeClass

            if self.agent.father_next:
                row, col = self.agent.father_index
                index = self.agent.father_index
            else:
                row, col = self.agent.son_index
                index = self.agent.son_index

            print(f"Current index: {row}, {col}")
            print(f"Choosen route: {choosen_route}")

            match choosen_route:
                case "['E']":
                    if (mazeClass.maze[row][col - 1] -1) >= 0 and (col - 1 >= 0):
                        ack = "ok"
                        index = (row, col - 1)
                    else: ack = "nok"

                case "['D']":
                    if (mazeClass.maze[row][col + 1] -1) >= 0 and (row + 1 <= mazeClass.width - 1):
                        ack = "ok"
                        index = (row, col + 1)
                    else: ack = "nok"

                case "['C']":
                    if (mazeClass.maze[row - 1][col] -1) >= 0 and (row - 1 >= 0):
                        ack = "ok"
                        index = (row - 1, col)
                    else: ack = "nok"

                case "['B']":
                    if (mazeClass.maze[row + 1][col] -1) >= 0 and (row + 1 <= mazeClass.depth - 1):
                        ack = "ok"
                        index = (row + 1, col)
                    else: ack = "nok"

            if self.agent.father_next:
                self.agent.father_index = index
                self.agent.father_next = False
            else:
                self.agent.son_index = index
                self.agent.father_next = True

        msg = Message(to="pai@xmpp.lan")     # Instantiate the message
        msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
        msg.body = f"{ack}"
        await self.send(msg)
        print(f"Acknowledged sent: {ack}")                   # Set the message content
        self.set_next_state(STATE_RCV_QUERY)


class RcvQuery(State):
    async def run(self):
        tolerance = 10.0 
        print(f"RcvQuery Running...")
        obj_chk = await self.receive(tolerance)
        if obj_chk:
            obj_chk.set_metadata("performative", "query-if")
            print(f"Obj Query succesfully received {format(obj_chk.body)}")
            if self.agent is not None:
                self.agent.choosen_route = obj_chk.body
            self.set_next_state(STATE_CHK_OBJ)
        else:
            print(f"No request received within {tolerance}s")


class ChkObj(State):
   async def run(self):
        print(f"ChkObj Running...")
        chk = "Uninitialized"
        chk_flag = None
        if self.agent is not None:
            mazeClass = self.agent.mazeClass
            row, col = self.agent.father_index

            if (mazeClass.maze[row][col] == 3): 
                chk = "Done"
                chk_flag = True
                self.agent.father_obj = True
            else: 
                chk = "Failure"
                chk_flag = False

        msg = Message(to="pai@xmpp.lan")     # Instantiate the message
        msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
        msg.body = f"{chk}"
        await self.send(msg)
        print(f"Route sent: {chk}")                   # Set the message content
        if self.agent is not None:
            if chk_flag and not self.agent.father_next: 
                self.set_next_state(STATE_RCV_ROUTE)    #Father accomplished the objective. Son must continue to move.

            if chk_flag and self.agent.father_next:
                pass                                    #Son accomplished the objective. Agent is finished. No more states to be executed.        

            else: self.set_next_state(STATE_RCV_REQUEST)


class MazeAgent(Agent):
    async def setup(self):
        print(f"Agent {format(str(self.jid))} started")
        self.mazeClass = Maze(MAZE_DEPTH, MAZE_WIDTH)
        self.father_index = self.mazeClass.entry_index
        self.father_obj = False
        self.son_index = self.mazeClass.entry_index
        self.son_obj = False
        self.choosen_route = None
        self.father_next = True

        fsm = FSMHandler()
        fsm.add_state(name=STATE_RCV_REQUEST, state=RcvRequest(), initial=True)
        fsm.add_state(name=STATE_INFORM_ROUTE, state=InformRoute())
        fsm.add_state(name=STATE_RCV_ROUTE, state=RcvRoute())
        fsm.add_state(name=STATE_ACK_ROUTE, state=AckRoute())
        fsm.add_state(name=STATE_RCV_QUERY, state=RcvQuery())
        fsm.add_state(name=STATE_INFORM_OBJ, state=ChkObj())
        fsm.add_transition(source=STATE_RCV_REQUEST, dest=STATE_INFORM_ROUTE)
        fsm.add_transition(source=STATE_INFORM_ROUTE, dest=STATE_RCV_ROUTE)
        fsm.add_transition(source=STATE_RCV_ROUTE, dest=STATE_ACK_ROUTE)
        fsm.add_transition(source=STATE_ACK_ROUTE, dest=STATE_RCV_QUERY)
        fsm.add_transition(source=STATE_RCV_QUERY, dest=STATE_INFORM_OBJ)
        fsm.add_transition(source=STATE_INFORM_OBJ, dest=STATE_ACK_ROUTE)
        self.add_behaviour(fsm)


async def main():
    mazeAgent = MazeAgent("labirinto@xmpp.lan", "labirinto")
    await mazeAgent.start(auto_register=True)

    await spade.wait_until_finished(mazeAgent)
    print("Maze agent finished")

if __name__ == "__main__":
    spade.run(main())

