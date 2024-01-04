# import pickle
import pickle
from utils.action import Action

from utils.singleton import SingletonMeta
from os import path


class ReplayLogger(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._log_path = 'maps/'
        self._log_name = 'log.txt'
        self._path = path.join(self._log_path, self._log_name)
        self.replay_path_map = ''
        self.replay_comments = []  # list of list of comments to display each steps
        self.replay_steps = []  # list of list of actions applied each steps

    def log_map(self, path: str) -> None:
        """Register the path to the map used for this replay

        :param path: path to the map used for this replay
        :type path: str
        """
        assert isinstance(path, str)

        self.replay_path_map = path

    def log_comment(self, comment: str) -> None:
        """Register a comment that will be shown during the next simulation step replay

        :param comment: comment to be registered
        :type comment: str
        """
        assert isinstance(comment, str)

        if len(self.replay_comments) == len(self.replay_steps):
            self.replay_comments.append([])
        for line in comment.split('\n'):
            self.replay_comments[-1].append(line)

    def log_step(self, actions: list[Action]) -> None:
        """Register a simulation step

        :param actions: list of actions making up a simulation step
        :type actions: list[Action]
        """
        assert isinstance(actions, list)
        assert len(actions) > 0
        assert isinstance(actions[0], Action)

        self.replay_steps.append(actions)
        while len(self.replay_comments) < len(self.replay_steps):
            self.replay_comments.append([])

    def get_replay(self) -> tuple[str, list[list[str]], list[list[Action]]]:
        """Returns the current replay, to be used in the class CliReplay

        :return: the current replay
        :rtype: tuple[str, list[list[str]], list[list[Action]]]
        """
        return (self.replay_path_map, self.replay_comments, self.replay_steps)

    def reset(self) -> None:
        self.replay_comments = []
        self.replay_steps = []

    def save_replay(self, path: str = 'last_replay.pkl') -> None:
        """Saves the current replay

        :param path: path to where the file should be saved
        :type path: str
        """

        pickle.dump(self.get_replay(), open(path, 'wb'))

    def is_repeating(self) -> bool:
        """Game analysis function, returns wether or not the game is repeating

        :return: wether or not the game is repeating
        :rtype: bool
        """

        if len(self.replay_steps) < 6:
            return False

        if self.replay_steps[-1] == self.replay_steps[-3] and self.replay_steps[-2] == self.replay_steps[-4]:
            return True

        return False
