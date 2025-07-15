from .model import LuckyNineModel, Instruction
from .view import LuckyNineView

class Control:
    def __init__(self, model: LuckyNineModel, view: LuckyNineView) -> None:
        self._model: LuckyNineModel = model
        self._view: LuckyNineView = view
        
    def game_loop(self) -> None:
        message_below = ''
        while not self._model._is_game_over:#type: ignore
            self._view.display_stats(self._model, message_below)
            user_input = self.user_input()
            while user_input is None:
                user_input = self.user_input()
            
            try:
                self._model.turn_cycle(Instruction(user_input))
            except ValueError:
                message_below = "empty hand is forced to draw\n"
                continue

            message_below = ''            
            self._model.next_active_player()
        
        self._view.display_stats(self._model, message_below)
        self._model.decide_winner()
        self._view.display_winner(self._model)
        
            
    def user_input(self) -> bool | None:
        temp = input("will you draw a card? y/n ").lower()
        match temp:
            case "y":
                return True
            case "n":
                return False
            case _:
                return None