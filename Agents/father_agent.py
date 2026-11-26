import ast
import spade

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message


PAI_JID = "pai@localhost"
PAI_PASSWORD = "pai"
LABIRINTO_JID = "labirinto@localhost"

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

        if (self.agent is not None) and (reply.body is not None):
            self.agent.available_paths = ast.literal_eval(reply.body)

        self.set_next_state(SEND_SUBSCRIBE)


# Estado 3: Enviar subscribe(direção)
class SendSubscribe(State):
    async def run(self):
        if self.agent is None:
            return

        direction = self.agent.choose_direction()

        if direction is None:
            print("[PAI] Não existem mais caminhos")
            return

        self.agent.chosen_direction = direction

        msg = Message(to=LABIRINTO_JID)
        msg.set_metadata("performative", "subscribe")
        msg.body = direction

        await self.send(msg)

        print(f"[PAI] subscribe({direction}) enviado")

        self.set_next_state(WAIT_MOVEMENT)


# Estado 4: Aguardar inform(ok/nok)
class WaitMovement(State):
    async def run(self):
        reply = await self.receive(timeout=15)

        if reply is None:
            print("[PAI] Nenhuma resposta de movimento")
            return

        if self.agent is None:
            return

        if reply.body == "ok":
            print("[PAI] Movimento confirmado")

            self.agent.confirm_movement()

            self.set_next_state(SEND_QUERY)

        elif reply.body == "nok":
            print("[PAI] Movimento recusado")
            # Por enquanto, encerra a FSM.


# Estado 5: Enviar query-if(objetivo)
class SendQuery(State):

    async def run(self):
        msg = Message(to=LABIRINTO_JID)
        msg.set_metadata("performative", "query-if")
        msg.body = "objetivo"

        await self.send(msg)

        print("[PAI] query-if(objetivo) enviado")

        self.set_next_state(WAIT_OBJECTIVE)


# Estado 6: Aguardar resultado do objetivo
class WaitObjective(State):

    async def run(self):
        reply = await self.receive(timeout=15)
        result = None

        if reply is None:
            print("[PAI] Nenhuma resposta sobre o objetivo")
            return

        if reply.body is not None:
            result = reply.body.strip().lower()

        print(f"[PAI] Resposta do objetivo: {result}")

        if result == "done":
            if self.agent is not None:
                print("[PAI] Objetivo encontrado!")
                print(f"[PAI] Caminho final: {self.agent.path}")
                await self.agent.stop()

        elif result == "failure":
            print("[PAI] Objetivo não encontrado. Continuando busca...")
            self.set_next_state(SEND_REQUEST)

        else:
            print(f"[PAI] Resposta inesperada: {repr(reply.body)}")


class FatherAgent(Agent):

     def choose_direction(self):
        movements = {
            "C": (-1, 0),
            "B": (1, 0),
            "E": (0, -1),
            "D": (0, 1)
        }

        row, col = self.current_position

        # Procura uma posição ainda não visitada
        for direction in self.available_paths:
            dr, dc = movements[direction]
            next_position = (row + dr, col + dc)

            if next_position not in self.visited:
                self.backtracking = False
                return direction

        # para onde volta caso não tenha novas posições
        if self.path:
            reverse = {
                "C": "B",
                "B": "C",
                "E": "D",
                "D": "E"
            }

            self.backtracking = True
            return reverse[self.path[-1]]

        return None

     def confirm_movement(self):
        movements = {
            "C": (-1, 0),
            "B": (1, 0),
            "E": (0, -1),
            "D": (0, 1)
        }

        if self.chosen_direction is not None:
            row, col = self.current_position
            dr, dc = movements[self.chosen_direction]

            # atualiza a posição atual
            self.current_position = (row + dr, col + dc)

        if self.backtracking:
            #remove o último da pilha
            self.path.pop()
        else:
            #registra a nova posição visitada
            self.visited.add(self.current_position)
            self.path.append(self.chosen_direction)

        print(f"[PAI] Posição atual: {self.current_position}")
        print(f"[PAI] Visitados: {self.visited}")
        print(f"[PAI] Caminho: {self.path}")

     async def setup(self):
        print(f"[PAI] Conectado: {self.jid}")

        self.current_position = (0, 0)
        self.visited = {(0, 0)}
        self.path = []
        self.available_paths = []
        self.chosen_direction = None
        self.backtracking = False

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
