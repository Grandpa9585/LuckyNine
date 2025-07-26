from typing import Dict, List

from .new_view import LuckyNineView
from .new_model import LuckyNineModel, Player, Card, Suit, Rank, CardTemplate
from .new_control import Control

view: LuckyNineView = LuckyNineView()

player_1 = Player(name="player 1")
player_2 = Player(name="player 2")
player_3 = Player(name="player 3")

directed_adjacency_graph: Dict[Player, Player] = {
    player_1: player_2,
    player_2: player_3,
    player_3: player_1,
}

totals: Dict[Player, int] = {
    player_1: 0,
    player_2: 0,
    player_3: 0,
}

first_player = player_1

deck: List[CardTemplate] = [Card(suit, rank) 
                    for suit in list(Suit)
                    for rank in list(Rank)]

max_hand_len = 3

model: LuckyNineModel = LuckyNineModel(deck, totals, directed_adjacency_graph, max_hand_len, first_player)

control: Control = Control(model, view)

control.main_game_loop()
