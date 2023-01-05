import spade
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State, CyclicBehaviour, PeriodicBehaviour
from spade.message import Message
import random

start_state = "StartState"
sign_number_state = "SignNumberState"
j_state = "JState"
seven_state = "SevenState"
eight_state = "EightState"
stop_state = "StopState"

sign_dict = {"\u2663":"\u2663", "\u2660":"\u2660", "\u2666":"\u2666", "\u2665":"\u2665"}
number_dict = {"A": 1, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13}

class MauMau(Agent):
    deck = []
    class MauMauBehav(FSMBehaviour):
        async def on_start(self):
            print("\nAgent " + self.agent.agent_name)
            if self.agent.agent_name=="Marta":
                print(" zapocinje s kartama " +  str(first_agent_cards))
            if self.agent.agent_name=="Ivan":
                print(" zapocinje s kartama " +  str(second_agent_cards))

        async def on_end(self):
            print("\nAgent " + self.agent.agent_name + " zavrsava")

    class StartState(State):
        async def run(self):
            self.set_next_state(sign_number_state)

    class SignNumberState(State):
        async def run(self):
            msg = await self.receive(timeout=10)
            print("\n------------------------------------------------")
            print(self.agent.agent_name + " je na potezu: ")
            if self.agent.agent_name=="Marta":
                print("Ruka agenta: " +  str(first_agent_cards))
            if self.agent.agent_name=="Ivan":
                print("Ruka agenta: " +  str(second_agent_cards))
            if msg:
                if msg.thread == "start":
                    card = random.choice(self.agent.cards)
                    self.agent.cards.remove(card)
                    message = Message(to=self.agent.env_jid,
                                    body=card,
                                    thread="card",
                                    metadata={"performative": "inform"})
                    if card[:-1] == "8":
                        message.body += "," + str(3)
                    await self.send(message)
                    self.set_next_state(sign_number_state)
                    print("\nIgra: " + card[:-1] + sign_dict[card[-1]])
                    self.agent.score -= number_dict[card[:-1]]
                else:
                    content = msg.body.split(",")
                    last_card_sign = content[0][-1]
                    last_card_number = content[0][:-1]
                    self.agent.last_card = content[0]
                    if last_card_number == "J":
                        self.set_next_state(j_state)
                    elif last_card_number == "7":
                        self.set_next_state(seven_state)
                    elif last_card_number == "8":
                        self.agent.cards_to_draw = int(content[1])
                        self.set_next_state(eight_state)

                    else:
                        is_card_found = False
                        for card in self.agent.cards:
                            card_sign = card[-1]
                            card_number = card[:-1]
                            if card_sign == last_card_sign or card_number == last_card_number:
                                message = Message(to=self.agent.env_jid,
                                                body=card,
                                                thread="card",
                                                metadata={"performative": "inform"})
                                if card_number == "8":
                                    message.body += "," + str(3)
                                await self.send(message)
                                self.agent.cards.remove(card)
                                self.set_next_state(sign_number_state)
                                is_card_found = True
                                print("Igra: " + card_number + sign_dict[card_sign])
                                self.agent.score -= number_dict[card_number]
                                break
                            elif card_number == "J":
                                message = Message(to=self.agent.env_jid,
                                                body=card,
                                                thread="card",
                                                metadata={"performative": "inform"})
                                await self.send(message)
                                self.agent.cards.remove(card)
                                self.set_next_state(sign_number_state)
                                is_card_found = True
                                print("Igra: " + card_number + sign_dict[card_sign])
                                self.agent.score -= number_dict[card_number]
                                break
                        while not is_card_found:
                            if len(self.agent.deck) == 0:
                                self.set_next_state(stop_state)
                                return
                            card = random.choice(self.agent.deck)
                            self.agent.deck.remove(card)
                            self.agent.cards.append(card)
                            card_sign = card[-1]
                            card_number = card[:-1]
                            print("\n------------------------------------------------")
                            print(self.agent.agent_name + " vuce " + card_number + sign_dict[card_sign] + " iz spila")
                            if self.agent.agent_name=="Marta":
                                print("Ruka agenta: " +  str(first_agent_cards))
                            if self.agent.agent_name=="Ivan":
                                print("Ruka agenta: " +  str(second_agent_cards))
                            self.agent.score += number_dict[card_number]
                            if card_sign == last_card_sign or card_number == last_card_number:
                                message = Message(to=self.agent.env_jid,
                                                body=card,
                                                thread="card",
                                                metadata={"performative": "inform"})
                                if card_number == "8":
                                    message.body += "," + str(3)
                                await self.send(message)
                                self.agent.cards.remove(card)
                                self.set_next_state(sign_number_state)
                                is_card_found = True
                                print("\n------------------------------------------------")
                                print("\nIgra: " + card_number + sign_dict[card_sign])
                                self.agent.score -= number_dict[card_number]
                                break

                if len(self.agent.cards) == 0:
                    self.set_next_state(stop_state)

    class JState(State):
        async def run(self):
            print("\n------------------------------------------------")
            print(self.agent.agent_name + " je na potezu: ")
            if self.agent.agent_name=="Marta":
                print("Ruka agenta: " +  str(first_agent_cards))
            if self.agent.agent_name=="Ivan":
                print("Ruka agenta: " +  str(second_agent_cards))
            is_card_found = False
            last_card_sign = self.agent.last_card[-1]
            for card in self.agent.cards:
                card_sign = card[-1]
                card_number = card[:-1]
                if card_number == "J":
                    message = Message(to=self.agent.env_jid,
                                    body=card,
                                    thread="card",
                                    metadata={"performative": "inform"})
                    await self.send(message)
                    self.agent.cards.remove(card)
                    self.set_next_state(sign_number_state)
                    is_card_found = True
                    print("\nIgra: " + card_number + sign_dict[card_sign])
                    self.agent.score -= number_dict[card_number]
                    break

            if not is_card_found:
                for card in self.agent.cards:
                    card_sign = card[-1]
                    card_number = card[:-1]
                    if card_sign == last_card_sign:
                        message = Message(to=self.agent.env_jid,
                                        body=card,
                                        thread="card",
                                        metadata={"performative": "inform"})
                        if card_number == "8":
                            message.body += "," + str(3)
                        await self.send(message)
                        self.agent.cards.remove(card)
                        self.set_next_state(sign_number_state)
                        is_card_found = True
                        print("\nIgra: " + card_number + sign_dict[card_sign])
                        self.agent.score -= number_dict[card_number]
                        break

            while not is_card_found:
                if len(self.agent.deck) == 0:
                    self.set_next_state(stop_state)
                    return
                card = random.choice(self.agent.deck)
                self.agent.deck.remove(card)
                self.agent.cards.append(card)
                card_sign = card[-1]
                card_number = card[:-1]
                print("\n------------------------------------------------")
                print(self.agent.agent_name + " vuce " + card_number + sign_dict[card_sign] + " iz spila")
                if self.agent.agent_name=="Marta":
                    print("Ruka agenta: " +  str(first_agent_cards))
                if self.agent.agent_name=="Ivan":
                    print("Ruka agenta: " +  str(second_agent_cards))
                self.agent.score += number_dict[card_number]
                if card_sign == last_card_sign:
                    message = Message(to=self.agent.env_jid,
                                    body=card,
                                    thread="card",
                                    metadata={"performative": "inform"})
                    if card_number == "8":
                        message.body += "," + str(3)
                    await self.send(message)
                    self.agent.cards.remove(card)
                    self.set_next_state(sign_number_state)
                    is_card_found = True
                    print("Igra: " + card_number + sign_dict[card_sign])
                    self.agent.score -= number_dict[card_number]
                    break
                elif card_number == "J":
                    message = Message(to=self.agent.env_jid,
                                    body=card,
                                    thread="card",
                                    metadata={"performative": "inform"})
                    await self.send(message)
                    self.agent.cards.remove(card)
                    self.set_next_state(sign_number_state)
                    is_card_found = True
                    print("Igra: " + card_number + sign_dict[card_sign])
                    self.agent.score -= number_dict[card_number]
                    break
            if len(self.agent.cards) == 0:
                self.set_next_state(stop_state)

    class SevenState(State):
        async def run(self):
            message = Message(to=self.agent.env_jid,
                            body=self.agent.last_card[-1],
                            thread="card",
                            metadata={"performative": "inform"})
            await self.send(message)
            self.set_next_state(sign_number_state)
            print(self.agent.agent_name + " preskace svoj red")

    class EightState(State):
        async def run(self):
            is_card_found = False
            for card in self.agent.cards:
                card_sign = card[-1]
                card_number = card[:-1]
                if card_number == "8":
                    cards_to_draw_temp = self.agent.cards_to_draw + 3
                    message = Message(to=self.agent.env_jid,
                                    body=card + "," + str(cards_to_draw_temp),
                                    thread="card",
                                    metadata={"performative": "inform"})
                    await self.send(message)
                    self.agent.cards.remove(card)
                    self.set_next_state(sign_number_state)
                    is_card_found = True
                    print("\n------------------------------------------------")
                    print(self.agent.agent_name + " je na potezu: \nIgra: " + card_number + sign_dict[card_sign])
                    self.agent.score -= number_dict[card_number]
                    break
            while not is_card_found:
                for i in range(self.agent.cards_to_draw):
                    if len(self.agent.deck) == 0:
                        self.set_next_state(stop_state)
                        return
                    card = random.choice(self.agent.deck)
                    self.agent.deck.remove(card)
                    self.agent.cards.append(card)
                    self.agent.score += number_dict[card[:-1]]
                self.set_next_state(sign_number_state)
                last_card_sign = self.agent.last_card[-1]
                message = Message(to=self.agent.env_jid,
                                body=last_card_sign,
                                thread="card",
                                metadata={"performative": "inform"})
                await self.send(message)
                is_card_found = True
                print("\n------------------------------------------------")
                print("Agent " + self.agent.agent_name + " vuce " + str(self.agent.cards_to_draw) + " karte")
                if self.agent.agent_name=="Marta":
                    print("Ruka agenta: " +  str(first_agent_cards))
                if self.agent.agent_name=="Ivan":
                    print("Ruka agenta: " +  str(second_agent_cards))
            if len(self.agent.cards) == 0:
                self.set_next_state(stop_state)

    class StopState(State):
        async def run(self):
            message = Message(to=self.agent.env_jid,
                            body=self.agent.agent_name,
                            thread="MauMau",
                            metadata={"performative": "inform"})
            if len(self.agent.deck) == 0:
                message.thread = "emptyDeck"
            await self.send(message)

    def __init__(self, jid, password, agent_name, cards, env_jid):
        super().__init__(jid, password)
        self.cards = cards
        self.agent_name = agent_name
        self.env_jid = env_jid
        self.score = 0

    async def setup(self):
        mau_mau_behav = self.MauMauBehav()

        mau_mau_behav.add_state(name=start_state, state=self.StartState(), initial=True)
        mau_mau_behav.add_state(name=sign_number_state, state=self.SignNumberState())
        mau_mau_behav.add_state(name=j_state, state=self.JState())
        mau_mau_behav.add_state(name=seven_state, state=self.SevenState())
        mau_mau_behav.add_state(name=eight_state, state=self.EightState())
        mau_mau_behav.add_state(name=stop_state, state=self.StopState())
        mau_mau_behav.add_transition(source=start_state, dest=sign_number_state)
        mau_mau_behav.add_transition(source=sign_number_state, dest=sign_number_state)
        mau_mau_behav.add_transition(source=sign_number_state, dest=j_state)
        mau_mau_behav.add_transition(source=j_state, dest=sign_number_state)
        mau_mau_behav.add_transition(source=sign_number_state, dest=seven_state)
        mau_mau_behav.add_transition(source=seven_state, dest=sign_number_state)
        mau_mau_behav.add_transition(source=sign_number_state, dest=eight_state)
        mau_mau_behav.add_transition(source=eight_state, dest=sign_number_state)
        mau_mau_behav.add_transition(source=sign_number_state, dest=stop_state)
        mau_mau_behav.add_transition(source=j_state, dest=stop_state)
        mau_mau_behav.add_transition(source=eight_state, dest=stop_state)

        self.add_behaviour(mau_mau_behav)
        for card in self.cards:
            self.score += number_dict[card[:-1]]

class Enviroment(Agent):
    class EnviromentBehav(PeriodicBehaviour):
        async def on_start(self):
            self.agent.is_first_agent_turn = True
            print("\nOkruzje zapocinje")

        async def on_end(self):
            print("\nOkruzje zavrsava")

        async def run(self):
            if not self.agent.is_first_message_sent:
                message = Message(to=self.agent.first_agent_jid,
                                body="",
                                thread="start",
                                metadata={"performative": "inform"})
                await self.send(message)
                self.agent.is_first_message_sent = True
            message = await self.receive(timeout=10)
            if message:
                if message.thread == "MauMau":
                    print("\n------------------------------------------------")
                    print("\nAgent " + message.body + " je pobjednik!")
                    print("\nAgent " + self.agent.first_agent.agent_name + " ima karte: " + str(first_agent_cards)+ "\n Ukupno ima bodova: " + str(self.agent.first_agent.score))
                    print("\nAgent " + self.agent.second_agent.agent_name + " ima karte: " + str(second_agent_cards)+  "\n Ukupno ima bodova: " + str(self.agent.second_agent.score))
                    await self.agent.first_agent.stop()
                    await self.agent.second_agent.stop()
                    await self.agent.stop()
                elif message.thread == "emptyDeck":
                    print("\n------------------------------------------------")
                    print("Spil je prazan!")
                    if self.agent.first_agent.score < self.agent.second_agent.score:
                        print("\nAgent " + self.agent.first_agent.agent_name + " je pobjednik!")
                    elif self.agent.first_agent.score > self.agent.second_agent.score:
                        print("\nAgent " + self.agent.second_agent.agent_name + " je pobjednik!")
                    else:
                        print("Vuci!")
                    print("\nAgent " + self.agent.first_agent.agent_name + " ima karte: " + str(first_agent_cards)+ "\n Ukupno ima bodova: " + str(self.agent.first_agent.score))
                    print("\nAgent " + self.agent.second_agent.agent_name + " ima karte: " + str(second_agent_cards)+  "\n Ukupno ima bodova: " + str(self.agent.second_agent.score))
                    await self.agent.first_agent.stop()
                    await self.agent.second_agent.stop()
                    await self.agent.stop()
                else:
                    if self.agent.is_first_agent_turn:
                        message.to = second_agent_jid
                        self.agent.is_first_agent_turn = False
                    else:
                        message.to = first_agent_jid
                        self.agent.is_first_agent_turn = True
                    await self.send(message)


    def __init__(self, jid, password, agent_name, first_agent_jid, second_agent_jid, first_agent, second_agent):
        super().__init__(jid, password)
        self.agent_name = agent_name
        self.first_agent_jid = first_agent_jid
        self.second_agent_jid = second_agent_jid
        self.first_agent = first_agent
        self.second_agent = second_agent
        self.is_first_agent_turn = True
        self.is_first_message_sent = False

    async def setup(self):
        env_behav = self.EnviromentBehav(period=2)
        self.add_behaviour(env_behav)
        await self.first_agent.start()
        await self.second_agent.start()

def createDeck():
    global playable_cards, playable_signs
    deck = []
    for i in range(len(playable_signs)):
        for j in range(len(playable_cards)):
            deck.append(playable_cards[j]+playable_signs[i])
    return deck


if __name__ == '__main__':
    first_agent_jid = "martaa@jabb.im"
    first_agent_password = "marta123"
    first_agent_name = "Marta"
    second_agent_jid = "ivann@jabb.im"
    second_agent_password = "ivan123"
    second_agent_name = "Ivan"
    env_jid = "okruzje@jabb.im"
    env_password = "okruzje123"
    env_name = "okruzje"

    playable_cards = ['K', 'Q', 'J', '10', '9', '8', '7', 'A']
    playable_signs = ['\u2663','\u2660', '\u2666', '\u2665']
    starting_card_count = 6
    print("\n-----Igra Mau-Mau zapocinje!-----")

    deck = createDeck()
    random.shuffle(deck)

    sample = random.sample(range(0, len(deck)), starting_card_count * 2)
    first_agent_cards = []
    second_agent_cards = []
    for i in range(len(sample)):
        if i < len(sample)//2:
            first_agent_cards.append(deck[sample[i] - i])
        else:
            second_agent_cards.append(deck[sample[i] - i])
        deck.pop(sample[i] - i)

    MauMau.deck = deck

    first_agent = MauMau(first_agent_jid, first_agent_password, first_agent_name, first_agent_cards, env_jid)
    second_agent = MauMau(second_agent_jid, second_agent_password, second_agent_name, second_agent_cards, env_jid)
    env = Enviroment(env_jid, env_password, env_name, first_agent_jid, second_agent_jid, first_agent, second_agent)
    future = env.start(auto_register=True)
    future.result()
    input("\n-----Pritisnite enter da zaustavite agente-----\n")
    spade.quit_spade()