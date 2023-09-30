from curses import wrapper
import os.path as os_path
import curses
import locale

from back.pacman_game import PacmanGame
from back.action import Action
from back.direction import Direction
from back.pacman import Pacman
from back.ghost import Ghost


class CliReplay():
    _path_board: str
    _history: list[list[Action]]

    def __init__(self, replay) -> None:
        assert isinstance(replay, tuple)
        assert len(replay) == 2
        assert isinstance(replay[0], str)
        assert os_path.exists(replay[0])
        assert isinstance(replay[1], list)
        assert len(replay[1]) > 0
        assert isinstance(replay[1][0], list)
        assert len(replay[1][0]) > 0
        assert isinstance(replay[1][0][0], Action)

        self._path_board = replay[0]
        self._history = replay[1]
        if input('Start curses replay ? (Y/n)') == 'n':
            return
        wrapper(self._start)

    def _start(self, stdscr) -> None:
        self._screen = stdscr
        self._screen.clear()
        self._screen.refresh()

        # game
        self._game = PacmanGame()
        self._game.load(self._path_board)

        # encoding
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        curses.curs_set(0)
        if not curses.has_colors():
            exit('Your terminal does not support curses colors')

        # constants
        self._ESCAPE = ['q']

        # colors
        curses.init_pair(1, curses.COLOR_BLUE, 0)  # wall
        curses.init_pair(2, curses.COLOR_YELLOW, 0)  # pacman

        # main loop
        self.main_loop()

        # exit
        self._screen.erase()
        self._screen.refresh()

    def main_loop(self) -> None:
        for step in self._history:
            self.display()

            # Input
            user_input = self._screen.get_wch()
            if user_input in self._ESCAPE:
                return

            self._game.step(step)

    def display(self) -> None:
        self._screen.erase()
        self._screen.border()
        self._screen.refresh()

        # board
        cells, agents = self._game.gather_cli_state()
        char_cell = [' ', '#', '+', '.', '0']
        color_cell = [0, 1, 0, 0, 0]
        char_pacman = ['v', '<', '^', '>']

        for x in range(len(cells)):
            for y in range(len(cells[0])):
                self._screen.addstr(y + 1,
                                    x + 1,
                                    char_cell[cells[x][y].value],
                                    curses.color_pair(color_cell[cells[x][y].value]))

        # agents
        for agent in agents:
            x, y = agent.get_position()
            if isinstance(agent, Pacman):
                self._screen.addstr(y + 1,
                                    x + 1,
                                    char_pacman[agent.get_last_direction().value],
                                    curses.color_pair(2))
