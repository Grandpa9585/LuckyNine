from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from random import randint
from typing import Dict, List

@dataclass
class Instruction:
    IS_DRAW_CARD: bool
    
@dataclass
class Status(Enum):
    IN_PLAY = auto()
    EQUAL = auto()
    HAS_WINNER = auto()

class LuckyNineModel():
    def __init__(self) -> None:
        self._is_game_over: bool = False
        self._player_1: Player = Player()
        self._player_2: Player = Player()
        self._directed_adjacency_graph: Dict[Player, Player] = {
            self._player_1: self._player_2,
            self._player_2: self._player_1,
        }
        self._current: Player = self._player_1
        self._totals: Dict[Player, int] = {
            self._player_1: 0,
            self._player_2: 0,
        }
        self._deck = [LuckyNineCard(suit, rank) 
                      for suit in list(Suits)
                      for rank in list(Ranks)]
        self._status: Status = Status.IN_PLAY
        self._winner: Player | None = None
        
    def active_players(self) -> int:
        return sum(1 for item in self._directed_adjacency_graph if item.is_in_play)
        
    def next_active_player(self) -> None:
        sentinel: Player = self._current
        self._current = self._directed_adjacency_graph[self._current]
        while not self._current is sentinel and not self._current.is_in_play:
            self._current = self._directed_adjacency_graph[self._current]
        
    def turn_cycle(self, instruction: Instruction) -> None:
        if instruction.IS_DRAW_CARD:
            self._current.draw_card(self._deck)
            if self._current.turns_taken == 2:
                self._current._is_in_play = False
        else:
            if self._current.turns_taken == 0:
                raise ValueError("Must take a card when hand is empty")
            self._totals[self._current] = self._current.halt()
            
        if not self.active_players():
            self._is_game_over = True
            
    def decide_winner(self) -> None:
        if self._totals[self._player_1] == self._totals[self._player_2]:
            self._status = Status.EQUAL
            return None
        else:
            self._status = Status.HAS_WINNER
            
        if self._totals[self._player_1] < self._totals[self._player_2]:
            self._winner = self._player_1
        else:
            self._winner = self._player_2

class Player():
    def __init__(self) -> None:
        self._hand: List[LuckyNineCard] = []
        self._total: int = 0
        self._is_in_play: bool = True
        self._turns_taken: int = 0
    
    def draw_card(self, deck: List[LuckyNineCard]) -> None:
        if not self._is_in_play:
            return None
        
        card: LuckyNineCard = deck.pop(randint(0, len(deck)))
        self._turns_taken += 1
        self._total += card.value
        self._total %= 10
        self._hand.append(card)
        
    def halt(self) -> int:
        self._is_in_play = False
        return self._total
    
    @property
    def total(self) -> int:
        return self._total
    
    @property
    def is_in_play(self) -> bool:
        return self._is_in_play
    
    @property
    def turns_taken(self) -> int:
        return self._turns_taken
        

class LuckyNineCard():
    def __init__(self, suit: Suits, rank: Ranks) -> None:
        self._suit: Suits = suit
        self._rank: Ranks = rank
        self._value: int = self._card_value()
        
    def _card_value(self) -> int:
        if self._rank is Ranks.ACE:
            return 1
        elif self._rank is Ranks.TWO:
            return 2
        elif self._rank is Ranks.THREE:
            return 3
        elif self._rank is Ranks.FOUR:
            return 4
        elif self._rank is Ranks.FIVE:
            return 5
        elif self._rank is Ranks.SIX:
            return 6
        elif self._rank is Ranks.SEVEN:
            return 7
        elif self._rank is Ranks.EIGHT:
            return 8
        elif self._rank is Ranks.NINE:
            return 9
        elif self._rank is Ranks.TEN:
            return 0
        elif self._rank is Ranks.JACK:
            return 0
        elif self._rank is Ranks.QUEEN:
            return 0
        elif self._rank is Ranks.KING:
            return 0
    
    @property
    def suit(self) -> Suits:
        return self._suit
    
    @property
    def rank(self) -> Ranks:
        return self._rank
    
    @property
    def value(self) -> int:
        return self._value

@dataclass
class Ranks(Enum):
    ACE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    JACK = auto()
    QUEEN = auto()
    KING = auto()
    
@dataclass
class Suits(Enum):
    CLUBS = auto()
    DIAMONDS = auto()
    HEARTS = auto()
    SPADES = auto()
    
model = LuckyNineModel()