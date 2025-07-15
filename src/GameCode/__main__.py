from .model import LuckyNineModel, Instruction
from .view import LuckyNineView
from .control import Control

model = LuckyNineModel()
view = LuckyNineView()

control = Control(model, view)

control.game_loop()