import curses


class ThemeData():
    def __init__(self) -> None:
        pass

    def set_dark_theme(self):
        # set custom colors
        curses.init_color(250, 150, 150, 150)  # define gray

        # define pairs
        # init_pair(color_id, foreground_color, background_color)
        curses.init_pair(1, curses.COLOR_BLUE, 0)  # wall
        curses.init_pair(2, 250, 0)  # dots
        curses.init_pair(3, curses.COLOR_BLUE, 250)  # wall in perception team 1
        curses.init_pair(4, curses.COLOR_CYAN, 0)  # dots in perception team 1
        curses.init_pair(5, curses.COLOR_YELLOW, 0)  # pacman team 1
        curses.init_pair(6, curses.COLOR_MAGENTA, 0)  # ghost team 1
        curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_RED)  # pacman team 2
        curses.init_pair(8, curses.COLOR_RED, 0)  # ghost team 2
        curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_BLACK)  # text color

    def set_light_theme(self):
        # set custom colors
        curses.init_color(250, 150, 150, 150)  # define gray

        # define pairs
        # init_pair(color_id, foreground_color, background_color)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # wall
        curses.init_pair(2, 250, curses.COLOR_WHITE)  # dots
        curses.init_pair(3, curses.COLOR_BLUE, 250)  # wall in perception team 1
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_WHITE)  # dots in perception team 1
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_WHITE)  # pacman team 1
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_WHITE)  # ghost team 1
        curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_RED)  # pacman team 2
        curses.init_pair(8, curses.COLOR_RED, curses.COLOR_WHITE)  # ghost team 2
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_WHITE)  # text color
