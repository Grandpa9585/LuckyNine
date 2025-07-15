from os import system

from .model import LuckyNineModel, Status, Suits, Ranks, LuckyNineCard

class LuckyNineView:
    def display_stats(self, model: LuckyNineModel, message_below: str) -> None:
        system("clear") # tied deeply to linux lmfao
        print("> " if model._current == model.player_1 else "", 
              "Player 1: ", 
              *[self._card_to_str(card) for card in model.player_1._hand],
              "\nsum: ", model.player_1.total)
        print("> " if model._current == model.player_2 else "", 
              "Player 2: ", 
              *[self._card_to_str(card) for card in model.player_2._hand],
              "\nsum: ", model.player_2.total)
        print(message_below, end='')
        
    def display_winner(self, model: LuckyNineModel) -> None:
        if model._status == Status.EQUAL:
            print("There is a Tie!")
        elif model._status == Status.HAS_WINNER:
            print(f"The winner is {\
                "player 1" if model._winner == model.player_1 else "player 2"}!")
            
    def _card_to_str(self, card: LuckyNineCard) -> str:
        return f"{self._enum_suit_to_str(card.suit)}{self._enum_ranks_to_str(card.rank)}"
            
    def _enum_suit_to_str(self, suit: Suits) -> str:
        match suit:
            case Suits.CLUBS:
                return 'C'
            case Suits.DIAMONDS:
                return 'D'
            case Suits.HEARTS:
                return 'H'
            case Suits.SPADES:
                return 'S'
            
    def _enum_ranks_to_str(self, rank: Ranks) -> str:
        match rank:
            case Ranks.ACE:
                return 'A'
            case Ranks.TWO:
                return '2'
            case Ranks.THREE:
                return '3'
            case Ranks.FOUR:
                return '4'
            case Ranks.FIVE:
                return '5'
            case Ranks.SIX:
                return '6'
            case Ranks.SEVEN:
                return '7'
            case Ranks.EIGHT:
                return '8'
            case Ranks.NINE:
                return '9'
            case Ranks.TEN:
                return '10'
            case Ranks.JACK:
                return 'J'
            case Ranks.QUEEN:
                return 'Q'
            case Ranks.KING:
                return 'K'
