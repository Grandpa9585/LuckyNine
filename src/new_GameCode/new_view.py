# from enum import Enum, auto
from os import system

from .new_control import LuckyModel
from .new_model import Instruction, Status, Rank, Suit

# class Instruction(Enum):
#     DRAW_CARD = auto()
#     BET = auto()

class LuckyNineView:
    def title_screen(self) -> None: # trust the process
        print(\
"""  
     _      _    _  ____  _    _  _   _  _____ 
    | |    | |  | ||  __|| |  | || | | ||  _  |
    | |    | |  | || |   | |_/ /  \\\\ // | |_| |   
    | |    | |  | || |   |  _ |    | |  |___  |   
    | |___ | |__| || |__ | | \\ \\   | |   ___| | 
    |_____||______||____||_|  |_|  |_|  |_____|
    
    Press Enter to Continue
""")
        
    def play_screen(self, model: LuckyModel) -> None:
        print(f"{model.current.name}'s cards are: ")
        for card in model.current.hand:
            print(f"{self.rank_enum_to_string(card.rank)} of {self.suit_enum_to_string(card.suit)}")
            
    def rank_enum_to_string(self, enum: Rank):
        match enum:
            case Rank.ACE:
                return "Ace"
            case Rank.TWO:
                return "Two"
            case Rank.THREE:
                return "Three"
            case Rank.FOUR:
                return "Four"
            case Rank.FIVE:
                return "Five"
            case Rank.SIX:
                return "Six"
            case Rank.SEVEN:
                return "Seven"
            case Rank.EIGHT:
                return "Eight"
            case Rank.NINE:
                return "Nine"
            case Rank.TEN:
                return "Ten"
            case Rank.JACK:
                return "Jack"
            case Rank.QUEEN:
                return "Queen"
            case Rank.KING:
                return "King"
    
    def suit_enum_to_string(self, enum: Suit):
        match enum:
            case Suit.CLUB:
                return "Clubs"
            case Suit.DIAMOND:
                return "Diamonds"
            case Suit.HEART:
                return "Hearts"
            case Suit.SPADE:
                return "Spades"
        
    def info_screen(self, s: str, end:str="\n") -> None:
        print(s,end=end)
        
    def user_input(self) -> Instruction:
        while True:
            match input("draw or bet? type in you answer: ").lower():
                case "draw":
                    return Instruction.DRAW_CARD
                case "bet":
                    return Instruction.BET
                case _:
                    continue
        
    def display_result(self, model: LuckyModel) -> None:
        if model.status == Status.EQUAL:
            print("There are no winners in this game")
        elif model.status == Status.HAS_WINNER and model.winner is not None:
            print(f"The winner for this game is {model.winner.name}")
        else:
            print("something went wrong")
            
    def empty_hand_error(self) -> None:
        print("You are forced to draw a card when your hand is empty")
        
    def clear_screen(self) -> None:
        system("clear")
        
    