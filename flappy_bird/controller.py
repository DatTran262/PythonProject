# controller.py
from model import FlappyBirdModel

class FlappyBirdController:
    def __init__(self):
        self.model = FlappyBirdModel()

    def update(self):
        self.model.update()

    def jump(self):
        self.model.jump()

    def reset(self):
        self.model.reset()