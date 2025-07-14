# run as python3 -m TestCode.test_model

from .model import LuckyNineModel, LuckyNineCard, Suits, Ranks, Player, Instruction, Status

import pytest

from typing import List

class TestLuckyNineModel:
    @pytest.fixture
    def ace_of_spades(self) -> List[LuckyNineCard]:
        return [LuckyNineCard(Suits.SPADES, Ranks.ACE)]
    
    @pytest.fixture
    def queen_of_hearts(self) -> List[LuckyNineCard]:
        return [LuckyNineCard(Suits.HEARTS, Ranks.QUEEN)]
    
    @pytest.fixture
    def nine_hearts(self) -> List[LuckyNineCard]:
        return [LuckyNineCard(Suits.HEARTS, Ranks.NINE)]
    
    def test_draw_card(self, ace_of_spades):
        # this tells me that different instances of a card even if theyre of the same value
        # are not even structurally equivallent for some fucking reason
        # makes sense now the more i think about it
        test_player = Player()
        card_sample = ace_of_spades[0]
        test_player.draw_card(ace_of_spades)
        
        assert test_player.is_in_play
        assert test_player.turns_taken == 1
        assert test_player.total == 1
        assert test_player._hand == [card_sample]
        
    def test_draw_face_cards_and_order(self, queen_of_hearts, nine_hearts):
        test_player = Player()
        card_sample_queen = queen_of_hearts[0]
        card_sample_hearts = nine_hearts[0]
        test_player.draw_card(queen_of_hearts)
        test_player.draw_card(nine_hearts)
        
        assert test_player.is_in_play
        assert test_player.turns_taken == 2
        assert test_player.total == 9
        assert test_player._hand == [card_sample_queen, card_sample_hearts]
    
    def test_draw_modulo(self, nine_hearts):
        test_player = Player()
        card_sample_hearts1 = nine_hearts[0]
        card_sample_hearts2 = nine_hearts[0]
        test_player.draw_card([card_sample_hearts1])
        test_player.draw_card(nine_hearts)
        
        assert test_player.is_in_play
        assert test_player.turns_taken == 2
        assert test_player.total == 8
        assert test_player._hand == [card_sample_hearts1, card_sample_hearts2]
        
    def test_halt(self, queen_of_hearts):
        test_player = Player()
        
        assert test_player.halt() == 0
        test_player.draw_card(queen_of_hearts)
        
        assert not test_player.is_in_play
        assert not test_player.turns_taken
        assert not test_player.total
        assert not test_player._hand
        
    
    def test_four_turn_game(self):
        model = LuckyNineModel()
        
        assert model.active_players() == 2
        
        assert model._current.is_in_play
        assert not model._current.turns_taken
        assert not model._current.total
        assert not model._current._hand
        
        model.turn_cycle(Instruction(IS_DRAW_CARD=True))
        
        assert model._current.is_in_play
        assert model._current.turns_taken == 1
        assert 0 <= model._current.total <= 9
        assert len(model._current._hand) == 1
        
        model.next_active_player()
        
        assert model._current.is_in_play
        assert not model._current.turns_taken
        assert not model._current.total
        assert not model._current._hand
        
        model.turn_cycle(Instruction(IS_DRAW_CARD=True))
        
        assert model._current.is_in_play
        assert model._current.turns_taken == 1
        assert 0 <= model._current.total <= 9
        assert len(model._current._hand) == 1
        
        model.next_active_player()
        
        assert model._current.is_in_play
        assert model._current.turns_taken == 1
        assert 0 <= model._current.total <= 9
        assert len(model._current._hand) == 1
        
        model.turn_cycle(Instruction(IS_DRAW_CARD=True))

        assert not model._current.is_in_play
        assert model._current.turns_taken == 2
        assert 0 <= model._current.total <= 9
        assert len(model._current._hand) == 2
        
        assert model.active_players() == 1
        
        model.next_active_player()
        
        assert model._current.is_in_play
        assert model._current.turns_taken == 1
        assert 0 <= model._current.total <= 9
        assert len(model._current._hand) == 1
        
        model.turn_cycle(Instruction(IS_DRAW_CARD=True))

        assert not model._current.is_in_play
        assert model._current.turns_taken == 2
        assert 0 <= model._current.total <= 9
        assert len(model._current._hand) == 2
        
        assert model.active_players() == 0
        
        model.turn_cycle(Instruction(IS_DRAW_CARD=True))

        assert not model._current.is_in_play
        assert model._current.turns_taken == 2
        assert 0 <= model._current.total <= 9
        assert len(model._current._hand) == 2
        
        assert model._status is not None
        assert model._is_game_over
        
    def test_halt_with_empty_hand(self):
        model = LuckyNineModel()
        
        with pytest.raises(ValueError):
            model.turn_cycle(Instruction(IS_DRAW_CARD=False))
            
        model.turn_cycle(Instruction(IS_DRAW_CARD=True))
        model.next_active_player()
        
        with pytest.raises(ValueError):
            model.turn_cycle(Instruction(IS_DRAW_CARD=False))
            
    def test_two_turn_game(self):
        model = LuckyNineModel()
        
        assert model.active_players() == 2
        
        model.turn_cycle(Instruction(IS_DRAW_CARD=True))
        model.next_active_player()

        model.turn_cycle(Instruction(IS_DRAW_CARD=True))
        model.next_active_player()
        
        model.turn_cycle(Instruction(IS_DRAW_CARD=False))
        
        assert model.active_players() == 1
        assert not model._is_game_over
        model.next_active_player()
        
        model.turn_cycle(Instruction(IS_DRAW_CARD=False))
        
        assert model.active_players() == 0
        assert model._is_game_over
        assert model._status is Status.IN_PLAY
        assert model._winner is None
        
        model.decide_winner()
        
        assert model._status is not Status.IN_PLAY
        
        

        
        
        
        