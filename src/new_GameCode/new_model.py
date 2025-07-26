from __future__ import annotations
from enum import Enum, auto
from random import randint
from typing import Dict, List, Protocol

class EmptyHandBettingError(Exception):
    pass

class Instruction(Enum):
    DRAW_CARD = auto()
    BET = auto()

class LuckyNineModel:
    def __init__(self, 
                 deck: List[CardTemplate], totals: Dict[Player, int], 
                 directed_adjacency_graph: Dict[Player, Player], max_hand: int,
                 first_player: Player) -> None:
        self._deck: List[CardTemplate] = deck
        self._totals: Dict[Player, int] = totals
        self._graph: Dict[Player, Player] = directed_adjacency_graph
        self._max_hand: int = max_hand
        self._status: Status = Status.IN_PLAY
        self._current: Player = first_player
        self._winner: Player | None = None
        
        self._players_len = len(totals)
        
    def end_of_game(self) -> None:
        self._winner = None
        self._status = Status.IN_PLAY
        self._players_len = len(self._totals)
        for player in self._totals:
            player.is_in_play = True
            self._totals[player] = 0
            player.turns_taken = 0
            self._deck.extend(player.hand)
            player.clear_hand()
        
    def next_active_player(self) -> None:
        sentinel: Player = self._current
        self._current = self._graph[self._current]
        while self._current is not sentinel and not self._current.is_in_play:
            self._current = self._graph[self._current]
        
    def current_turn(self, user_input: Instruction) -> None:
        match user_input:
            case Instruction.DRAW_CARD:
                if not self._current.is_in_play:
                    return None
                try:
                    self._current.draw_card(self._deck)
                except ValueError:
                    self._current.is_in_play = False
                    return None
                if self._current.turns_taken == self._max_hand:
                    print("too bad max turns, youre betting")
                    self.current_turn(Instruction.BET)
                self._current.turns_taken += 1
            case Instruction.BET:
                if len(self._current.hand) == 0:
                    raise EmptyHandBettingError
                self._current.is_in_play = False
                self._players_len -= 1
                temp_calculation: int = sum((card.value for card in self._current.hand))
                self._totals[self._current] = temp_calculation
                
        if not self._players_len:
            self._decide_winner()
            
    def _decide_winner(self) -> None:
        # get a max
        # invert the dict list to int player
        # if there are other players, theres a tie
        temp: Dict[int, List[Player]] = {}
        temp_max: Player = max(self._totals, key=lambda x: self._totals[x])
        for player in self._totals:
            if self._totals[player] in temp:
                temp[self._totals[player]].append(player)
            else:
                temp[self._totals[player]] = [player]
        if len(temp[self._totals[temp_max]]) == 1:
            self._status = Status.HAS_WINNER
            self._winner = temp_max
        else:
            self._status = Status.EQUAL
        
    @property
    def deck_len(self) -> int:
        return len(self._deck)
        
    @property
    def status(self) -> Status:
        return self._status
    
    @property
    def winner(self) -> Player | None:
        return self._winner
    
    @property
    def current(self) -> Player:
        return self._current


class Player:
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._hand: List[CardTemplate] = []
        self._is_in_play: bool = True
        self._turns_taken: int = 0
        
    def draw_card(self, deck: List[CardTemplate], is_normal_game_cycle:bool=True) -> None:
        if is_normal_game_cycle:
            self._hand.append(deck.pop(randint(0, len(deck) - 1)))
            return None

        self.hand.append(deck.pop())
        
    def play_hand(self) -> None:
        self._is_in_play = False
        
    def clear_hand(self) -> None:
        self._hand.clear()
        
    @property
    def hand(self) -> List[CardTemplate]:
        return [card for card in self._hand]
    
    @property
    def is_in_play(self) -> bool:
        return self._is_in_play
    
    @is_in_play.setter
    def is_in_play(self, value: bool) -> None:
        self._is_in_play = value
        
    @property
    def turns_taken(self) -> int:
        return self._turns_taken
    
    @turns_taken.setter
    def turns_taken(self, value: int) -> None:
        self._turns_taken = value
        
    @property
    def name(self) -> str:
        return self._name


class CardTemplate(Protocol):
    _suit: Suit
    _rank: Rank
    _value: int
    
    @property
    def suit(self) -> Suit:
        ...
    @property
    def rank(self) -> Rank:
        ...
    @property
    def value(self) -> int:
        ...

class Card:
    def __init__(self, suit: Suit, rank: Rank) -> None:
        self._suit: Suit = suit
        self._rank: Rank = rank
        self._value = self.card_value()
        
    def card_value(self) -> int:
        match self._rank:
            case Rank.ACE:
                return 1
            case Rank.TWO:
                return 2
            case Rank.THREE:
                return 3
            case Rank.FOUR:
                return 4
            case Rank.FIVE:
                return 5
            case Rank.SIX:
                return 6
            case Rank.SEVEN:
                return 7
            case Rank.EIGHT:
                return 8
            case Rank.NINE:
                return 9
            case Rank.TEN:
                return 0
            case Rank.JACK:
                return 0
            case Rank.QUEEN:
                return 0
            case Rank.KING:
                return 0
            
    @property
    def suit(self) -> Suit:
        return self._suit
    @property
    def rank(self) -> Rank:
        return self._rank
    @property
    def value(self) -> int:
        return self._value

class Status(Enum):
    IN_PLAY = auto()
    EQUAL = auto()
    HAS_WINNER = auto()

class Suit(Enum):
    CLUB = auto()
    DIAMOND = auto()
    HEART = auto()
    SPADE = auto()
    
class Rank(Enum):
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
