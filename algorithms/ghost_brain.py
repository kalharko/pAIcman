import random
from algorithms.brain import Brain
from back.perception import Perception
from utils.direction import Direction
from utils.strategy import Strategy
from utils.action import Action


class GhostBrain(Brain):
    def __init__(self):
        pass

    def compute_action(self, strategy: Strategy, perception: Perception, id: str) -> Action:
        assert isinstance(strategy, Strategy)
        assert isinstance(perception, Perception)
        assert isinstance(id, str)

        if strategy == Strategy['RANDOM']:
            return Action(id, random.choice(list(Direction)))

        # TODO
