# type: ignore
import ast
import spade

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message

FILHO_JID = "filho@localhost"
FILHO_PASSWORD = "filho"
LABIRINTO_JID = "labirinto@localhost"
PAI_JID = "pai@localhost"

IDLE_STATE = "IDLE_STATE"
SEND_SUBSCRIBE = "SEND_SUBSCRIBE"
WAIT_ACK = "WAIT_ACK"
SEND_FEEDBACK = "SEND_FEEDBACK"


class IdleState(State):
    async def run(self):
        print(f"[FILHO] Está em Idle")
        msg = await self.receive(timeout = 120.0)

        if (self.agent is not None) and (msg is not None):
            self.agent.route = msg.body
            print(f"[FILHO] Direções recebidas! {self.agent.route}")

        self.set_next_state(SEND_SUBSCRIBE)


class SendSubscribe(State):
    async def run (self):
        msg = Message(to=LABIRINTO_JID)
        msg.set_metadata("performative", "subscribe")

        if self.agent is not None:
            msg.body = self.agent.route
            await self.send(msg)
            print(f"[FILHO] subscribe({self.agent.route}) enviado")

        self.set_next_state(WAIT_ACK)


class WaitAck(State):
    async def run (self):
        ack = await self.receive(timeout=10)

        if ack is None:
            print("[FILHO] Mensagem não recebida")
            return

        else:
            if ack.body == "nok":
                print("[FILHO] Não cheguei")
                return

            if ack.body == "ok":
                self.set_next_state(SEND_FEEDBACK)


class SendFeedback(State):
    async def run (self):
        msg = Message(to=PAI_JID)
        msg.set_metadata("performative", "inform")

        msg.body = "Cheguei"
        await self.send(msg)
        print(f"[FILHO] {msg.body}")

        return


class SonAgent(Agent):

    async def setup(self):
        self.fsm = FSMBehaviour()

        self.fsm.add_state(IDLE_STATE, IdleState(), initial=True)
        self.fsm.add_state(SEND_SUBSCRIBE, SendSubscribe())
        self.fsm.add_state(WAIT_ACK, WaitAck())
        self.fsm.add_state(SEND_FEEDBACK, SendFeedback())

        self.fsm.add_transition(IDLE_STATE, SEND_SUBSCRIBE)
        self.fsm.add_transition(SEND_SUBSCRIBE, WAIT_ACK)
        self.fsm.add_transition(WAIT_ACK, IDLE_STATE)
        self.fsm.add_transition(WAIT_ACK, SEND_FEEDBACK)

        self.add_behaviour(self.fsm)


async def main():
    son = SonAgent(FILHO_JID, FILHO_PASSWORD, port=5222)

    try:
        await son.start(auto_register=True)
        await son.fsm.join()
    finally:
        await son.stop()


if __name__ == "__main__":
    spade.run(main())