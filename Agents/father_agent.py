
import spade

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message


PAI_JID = "pai@xmpp.lan"
PAI_PASSWORD = "pai"
LABIRINTO_JID = "labirinto@xmpp.lan"

SEND_REQUEST = "SEND_REQUEST"
WAIT_PATHS = "WAIT_PATHS"
SEND_SUBSCRIBE = "SEND_SUBSCRIBE"
WAIT_MOVEMENT = "WAIT_MOVEMENT"
SEND_QUERY = "SEND_QUERY"
WAIT_OBJECTIVE = "WAIT_OBJECTIVE"


# Estado 1: Enviar request(caminhos)
class SendRequest(State):

    async def run(self):
        msg = Message(to=LABIRINTO_JID)
        msg.set_metadata("performative", "request")
        msg.body = "caminhos"

        await self.send(msg)

        print("[PAI] request(caminhos) enviado")

        self.set_next_state(WAIT_PATHS)


# Estado 2: Aguardar inform(direções)
class WaitPaths(State):

    async def run(self):

        reply = await self.receive(timeout=15)

        if reply is None:
            print("[PAI] Nenhuma resposta recebida")
            return

        print(f"[PAI] Direções recebidas: {reply.body}")

        if self.agent is not None:
            self.agent.available_paths = reply.body

        self.set_next_state(SEND_SUBSCRIBE)


# Estado 3: Enviar subscribe(direção)
class SendSubscribe(State):

    async def run(self):
        msg = Message(to=LABIRINTO_JID)
        msg.set_metadata("performative", "subscribe")
        if self.agent is not None:
            msg.body = self.agent.available_paths

        await self.send(msg)

        print("[PAI] subscribe(direção) enviado")

        self.set_next_state(WAIT_MOVEMENT)


# Estado 4: Aguardar inform(ok/nok)
class WaitMovement(State):

    async def run(self):
        pass
        self.set_next_state(SEND_QUERY)


# Estado 5: Enviar query-if(objetivo)
class SendQuery(State):

    async def run(self):
        pass
        self.set_next_state(WAIT_OBJECTIVE)


# Estado 6: Aguardar resultado do objetivo
class WaitObjective(State):

    async def run(self):
        pass


class FatherAgent(Agent):

    async def setup(self):
        print(f"[PAI] Conectado: {self.jid}")

        self.fsm = FSMBehaviour()

        #registro dos estados
        self.fsm.add_state(
            SEND_REQUEST, SendRequest(), initial=True
        )
        self.fsm.add_state(WAIT_PATHS, WaitPaths())
        self.fsm.add_state(SEND_SUBSCRIBE, SendSubscribe())
        self.fsm.add_state(WAIT_MOVEMENT, WaitMovement())
        self.fsm.add_state(SEND_QUERY, SendQuery())
        self.fsm.add_state(WAIT_OBJECTIVE, WaitObjective())

        #registro das transições
        self.fsm.add_transition(SEND_REQUEST, WAIT_PATHS)
        self.fsm.add_transition(WAIT_PATHS, SEND_SUBSCRIBE)
        self.fsm.add_transition(SEND_SUBSCRIBE, WAIT_MOVEMENT)
        self.fsm.add_transition(WAIT_MOVEMENT, SEND_QUERY)
        self.fsm.add_transition(SEND_QUERY, WAIT_OBJECTIVE)
        self.fsm.add_transition(WAIT_OBJECTIVE, SEND_REQUEST)

        self.add_behaviour(self.fsm)


async def main():
    father = FatherAgent(PAI_JID, PAI_PASSWORD, port=5222)

    try:
        await father.start(auto_register=False)
        await father.fsm.join()
    finally:
        await father.stop()


if __name__ == "__main__":
    spade.run(main())
