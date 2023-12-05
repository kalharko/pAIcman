import copy
from curses import wrapper
import curses
import locale
from back.cell import Cell

from back.pacman_game import PacmanGame
from utils.action import Action
from utils.replay_logger import ReplayLogger
from back.pacman import Pacman
from utils.direction import Direction


class CliReplay():
    _fancy_walls: list[list[str]]
    _step_count: int
    _map_path: str
    _steps: list[list[Action]]
    _comments: list[list[str]]

    def __init__(self) -> None:
        self._map_path, self._comments, self._steps = ReplayLogger().get_replay()
        self._game = PacmanGame()
        self._game.load_map(self._map_path)

        self._fancy_walls = [[]]
        self._step_count = 0
        for line in self._game.get_history():
            for a in line:
                print(a, end=' ')
            print()
        if input('Start curses replay ? (Y/n)') == 'n':
            return

        # start graphical interface
        wrapper(self._start)

    def _start(self, stdscr) -> None:
        self._screen = stdscr
        self._screenH, self._screenW = self._screen.getmaxyx()
        self._screen.clear()
        self._screen.refresh()

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
        curses.init_color(250, 150, 150, 150)  # define gray

        curses.init_pair(1, curses.COLOR_BLUE, 0)  # wall
        curses.init_pair(2, 250, 0)  # dots
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_RED)  # wall in perception team 1
        curses.init_pair(4, 250, curses.COLOR_RED)  # dots in perception team 1
        curses.init_pair(5, curses.COLOR_YELLOW, 0)  # pacman team 1
        curses.init_pair(6, curses.COLOR_MAGENTA, 0)  # ghost team 1
        curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_RED)  # pacman team 2
        curses.init_pair(8, curses.COLOR_MAGENTA, curses.COLOR_RED)  # ghost team 2
        curses.init_pair(9, curses.COLOR_MAGENTA, curses.COLOR_RED)  # pacman team 2 in perception team 1
        curses.init_pair(10, curses.COLOR_MAGENTA, curses.COLOR_RED)  # ghost team 2 in perception team 1

        # main loop
        self.main_loop()

        # exit
        self._screen.erase()
        self._screen.refresh()

    def main_loop(self) -> None:
        for comments, step in zip(self._comments, self._steps):
            self.display(comments)

            # Input
            user_input = self._screen.get_wch()
            if user_input in self._ESCAPE:
                return

            self._game.step(step)
            self._step_count += 1

    def display(self, comments: list[str]) -> None:
        self._screen.erase()
        self._screen.border()
        self._screen.refresh()

        # board
        teams = self._game._agent_manager.get_teams()
        team1, team2 = (teams[0], teams[1]) if teams[0]._team_number == 0 else (teams[1], teams[0])
        last_cells_seen_by_team1 = team1.get_perception().get_last_cells_seen()
        board = self._game._board_manager.get_all_cells()
        char_cell = [' ', '#', '·', 'Ø']
        color_cell = [1, 1, 2, 2]
        char_pacman = {Direction['UP']: 'ᗢ',
                       Direction['RIGHT']: 'ᗧ',
                       Direction['DOWN']: 'ᗣ',
                       Direction['LEFT']: 'ᗤ',
                       Direction['NONE']: 'X'}
        char_ghost = 'ᗝ'

        for x in range(len(board)):
            for y in range(len(board[0])):
                if board[x][y] == Cell['WALL']:
                    char = self._fancy_walls[x][y]
                else:
                    char = char_cell[board[x][y].value]
                color = curses.color_pair(color_cell[board[x][y].value])
                if (x, y) in last_cells_seen_by_team1:
                    color += 3
                self._screen.addstr(y + 1, x + 1, char, color)

        # agents team 1
        x, y = team1.get_pacman().get_position()
        self._screen.addstr(y + 1, x + 1, char_pacman[team1.get_pacman().get_last_direction()], curses.color_pair(5))
        for ghost in team1.get_ghosts():
            x, y = ghost.get_position()
            self._screen.addstr(y + 1, x + 1, char_ghost, curses.color_pair(6))

        # agents team 2
        x, y = team1.get_pacman().get_position()
        if (x, y) in last_cells_seen_by_team1:
            self._screen.addstr(y + 1, x + 1, char_pacman[team1.get_pacman().get_last_direction()], curses.color_pair(9))
        else:
            self._screen.addstr(y + 1, x + 1, char_pacman[team1.get_pacman().get_last_direction()], curses.color_pair(7))
        for ghost in team1.get_ghosts():
            x, y = ghost.get_position()
            if (x, y) in last_cells_seen_by_team1:
                self._screen.addstr(y + 1, x + 1, char_ghost, curses.color_pair(10))
            else:
                self._screen.addstr(y + 1, x + 1, char_ghost, curses.color_pair(8))

        # comments
        y = 1
        for comment in comments:
            self._screen.addstr(y, len(board), comment[:self._screenW - len(board)])

            y += 1
            if y + 1 >= self._screenH:
                break

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
                    str((1, 1, 0, 0, 0, 1, 0, 1)): '┐',
                    str((1, 1, 0, 1, 0, 0, 0, 1)): '└',
                    str((0, 1, 1, 1, 0, 0, 0, 0)): '└',
                    str((0, 1, 0, 1, 1, 1, 0, 0)): '└',
                    str((1, 1, 0, 1, 1, 1, 1, 1)): '└',
                    str((0, 1, 1, 1, 0, 0, 0, 1)): '┘',
                    str((1, 1, 0, 0, 0, 0, 0, 1)): '┘',
                    str((0, 1, 1, 1, 1, 1, 1, 1)): '┘',
                    str((0, 1, 0, 0, 0, 1, 1, 1)): '┘',
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
