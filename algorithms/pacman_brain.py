import random
from algorithms.a_star import AStar
from algorithms.perception import Perception
from algorithms.q_iteration import QIteration
from algorithms.hunter_prey import HunterPrey
from utils.action import Action
from utils.direction import Direction
from utils.strategy import Strategy


class PacmanBrain():
    def __init__(self):
        pass

    def compute_action(self, strategy: Strategy, perception: Perception, id: str) -> Action:
        assert isinstance(strategy, Strategy)
        assert isinstance(perception, Perception)
        assert isinstance(id, str)

        if strategy == Strategy['RANDOM']:
            return Action(id, random.choice(list(Direction)))
        # si la strat = explo , alors a* pour aller au pacdot le plus proche
        # dans une autre branche
        # sur le master, une version qui amrche tjrs 
        # TODO
