from .model import LuckyNineModel
from .view import LuckyNineView
from .control import Control

model = LuckyNineModel()
view = LuckyNineView()

control = Control(model, view)

control.game_loop()