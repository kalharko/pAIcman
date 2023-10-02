from curses import wrapper
import os.path as os_path
import curses
import locale
from back.cell import Cell

from back.pacman_game import PacmanGame
from back.action import Action
from back.pacman import Pacman


class CliReplay():
    _path_board: str
    _history: list[list[Action]]
    _fancy_walls: list[list[str]]

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
        self._fancy_walls = [[]]
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

        # load fancy walls
        self._fancy_walls = self._load_fancy_walls()

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
        curses.init_color(700, 150, 150, 150)  # define gray
        curses.init_pair(3, 700, 0)  # dots

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
        char_cell = [' ', '#', '_', '·', 'Ø']
        color_cell = [0, 1, 3, 3, 3]
        char_pacman = ['v', '<', '^', '>']

        for x in range(len(cells)):
            for y in range(len(cells[0])):
                if cells[x][y] == Cell['WALL']:
                    char = self._fancy_walls[x][y]
                else:
                    char = char_cell[cells[x][y].value]
                self._screen.addstr(y + 1,
                                    x + 1,
                                    char,
                                    curses.color_pair(color_cell[cells[x][y].value]))

        # agents
        for agent in agents:
            x, y = agent.get_position()
            if isinstance(agent, Pacman):
                self._screen.addstr(y + 1,
                                    x + 1,
                                    char_pacman[agent.get_last_direction().value],
                                    curses.color_pair(2))

        # score
        i = 0
        self._screen.addstr(2, len(cells) + 2, 'Scores', curses.color_pair(3))
        for agent in agents:
            if isinstance(agent, Pacman):
                self._screen.addstr(3 + i, len(cells) + 2, f'{agent.get_id()} : {agent.get_score()}', curses.color_pair(3))
                i += 1

    def _load_fancy_walls(self) -> list[list[str]]:
        cells, agents = self._game.gather_cli_state()
        out = [[' ' for y in range(len(cells[0]))] for x in range(len(cells))]
        wall_map = {str((0, 0, 0, 0, 0, 0, 0, 0)): '█',
                    str((1, 1, 1, 1, 1, 1, 1, 1)): ' ',
                    str((0, 0, 0, 1, 0, 1, 0, 0)): '╔',
                    str((0, 0, 0, 1, 0, 0, 0, 1)): '═',
                    str((0, 1, 0, 0, 0, 1, 0, 0)): '║',
                    str((0, 0, 0, 0, 0, 1, 0, 1)): '╗',
                    str((0, 1, 0, 0, 0, 0, 0, 1)): '╝',
                    str((0, 1, 0, 1, 0, 0, 0, 0)): '╚',
                    str((0, 0, 0, 1, 0, 0, 1, 1)): '═',
                    str((0, 1, 1, 0, 0, 1, 0, 0)): '║',
                    str((0, 0, 0, 1, 1, 0, 0, 1)): '═',
                    str((1, 0, 0, 1, 0, 0, 0, 1)): '═',
                    str((0, 0, 1, 1, 0, 0, 0, 1)): '═',
                    str((0, 0, 0, 1, 0, 0, 0, 0)): '═',
                    str((0, 0, 0, 0, 0, 0, 0, 1)): '═',
                    str((0, 1, 0, 0, 1, 1, 0, 0)): '║',
                    str((1, 1, 0, 0, 0, 1, 0, 0)): '║',
                    str((0, 1, 0, 0, 0, 1, 1, 0)): '║',
                    str((0, 0, 0, 1, 1, 1, 0, 1)): '┐',
                    str((0, 0, 0, 0, 0, 1, 1, 1)): '┐',
                    str((1, 1, 1, 1, 1, 1, 0, 1)): '┐',
                    str((0, 1, 1, 1, 0, 1, 0, 0)): '┐',
                    str((1, 1, 0, 1, 0, 0, 0, 1)): '└',
                    str((0, 1, 1, 1, 0, 0, 0, 0)): '└',
                    str((0, 1, 0, 1, 1, 1, 0, 0)): '└',
                    str((1, 1, 0, 1, 1, 1, 1, 1)): '└',
                    str((0, 1, 1, 1, 0, 0, 0, 1)): '┘',
                    str((1, 1, 0, 0, 0, 0, 0, 1)): '┘',
                    str((0, 1, 1, 1, 1, 1, 1, 1)): '┘',
                    str((0, 0, 0, 1, 0, 1, 1, 1)): '┌',
                    str((0, 0, 0, 1, 1, 1, 0, 0)): '┌',
                    str((1, 1, 1, 1, 0, 1, 1, 1)): '┌',
                    str((1, 1, 1, 0, 0, 1, 1, 1)): '│',
                    str((1, 1, 1, 1, 1, 1, 0, 0)): '│',
                    str((0, 1, 1, 1, 1, 1, 0, 0)): '│',
                    str((1, 1, 0, 0, 0, 1, 1, 1)): '│',
                    str((1, 1, 0, 0, 1, 1, 1, 1)): '│',
                    str((0, 1, 1, 1, 1, 1, 1, 0)): '│',
                    str((0, 0, 0, 1, 1, 1, 1, 1)): '─',
                    str((1, 1, 1, 1, 0, 0, 0, 1)): '─',
                    str((1, 1, 1, 1, 0, 0, 1, 1)): '─',
                    str((1, 1, 1, 1, 1, 0, 0, 1)): '─',
                    str((1, 0, 0, 1, 1, 1, 1, 1)): '─',
                    str((0, 0, 1, 1, 1, 1, 1, 1)): '─',
                    }
        for x in range(len(cells)):
            for y in range(len(cells[0])):
                if cells[x][y] != Cell['WALL']:
                    continue
                mat = [[cells[x][y] == Cell['WALL'] if 0 <= x < len(cells) and 0 <= y < len(cells[0]) else False for y in range(y - 1, y + 2)] for x in range(x - 1, x + 2)]
                neighbors = str((int(mat[0][0]),
                                 int(mat[1][0]),
                                 int(mat[2][0]),
                                 int(mat[2][1]),
                                 int(mat[2][2]),
                                 int(mat[1][2]),
                                 int(mat[0][2]),
                                 int(mat[0][1])))
                if not str(neighbors) in wall_map.keys():
                    out[x][y] = "#"
                else:
                    out[x][y] = wall_map[str(neighbors)]
        return out
