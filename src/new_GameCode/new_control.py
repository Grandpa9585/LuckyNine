from typing import Protocol

from .new_model import Status, Instruction, EmptyHandBettingError, Player
# from new_view import

class LuckyModel(Protocol):
    def current_turn(self, user_input: Instruction) -> None:
        ...
    
    def next_active_player(self) -> None:
        ...
        
    def end_of_game(self) -> None:
        ...
    
    @property
    def deck_len(self) -> int:
        ...
        
    @property
    def status(self) -> Status:
        ...
        
    @property
    def winner(self) -> Player | None:
        ...
        
    @property
    def current(self) -> Player:
        ...        
    # might add more

class LuckyView(Protocol):
    def title_screen(self) -> None:
        ...
        
    def play_screen(self, model: LuckyModel) -> None:
        ...
        
    def info_screen(self, s: str) -> None:
        ...
        
    def user_input(self) -> Instruction:
        ...
        
    def display_result(self, model: LuckyModel) -> None:
        ...
        
    def empty_hand_error(self) -> None:
        ...
        
    def clear_screen(self) -> None:
        ...

class Control:
    def __init__(self, model: LuckyModel, view: LuckyView) -> None:
        self._model: LuckyModel = model
        self._view: LuckyView = view        
        
    def main_game_loop(self) -> None:
        self._view.clear_screen()
        self._view.title_screen()
        input() # press any key to continue
        self._view.clear_screen()
        while self._model.deck_len:
            self._main_game_loop_individual_round()
           
            self._view.info_screen("play again? y/n ")
            if not self._boolean_input_handler():
               break
            
            self._model.end_of_game()           
                   
    def _main_game_loop_individual_round(self) -> None:
        while self._model.status == Status.IN_PLAY:
            self._view.play_screen(self._model)
            user_input: Instruction = self._view.user_input()
            try:
                self._model.current_turn(user_input)
            except EmptyHandBettingError:
                self._view.empty_hand_error()
                continue
            self._view.clear_screen()
            self._view.play_screen(self._model)
            input(f"you have chosen to {'bet' if user_input == Instruction.BET else 'draw'}\npress enter to continue")
            self._model.next_active_player() 
            self._view.clear_screen()
             
        self._view.display_result(self._model)    
            
    def _boolean_input_handler(self) -> bool | None:
        while True:
            match input().lower():
                case 'y':
                    return True
                case 'n':
                    return False
                case _:
                    pass