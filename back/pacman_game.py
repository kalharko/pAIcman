from back.board_manager import BoardManager
from back.agent_manager import AgentManager
from back.agent import Agent
from back.action import Action
from back.errors import PacErrInvalidAction, PacErrPacmanInWall
from back.cell import Cell
from back.pacman import Pacman

import os.path as os_path


class PacmanGame():
    _board_manager: BoardManager
    _agent_manager: AgentManager
    _path_board: str
    _history: list[list[Action]]

    def __init__(self) -> None:
        self._board_manager = BoardManager()
        self._agent_manager = AgentManager()
        self._path_board = None
        self._history = []

    def load(self, path: str) -> None:
        assert isinstance(path, str)

        if not os_path.exists(path):
            return FileNotFoundError()

        with open(path, 'r') as file:
            lines = file.readlines()

        i = 0
        agents = {}
        while lines[i] != '|\n':
            line = lines[i].rstrip('\n').split(', ')
            if line[0] == 'Pacman':
                agents[line[1]] = Pacman(line[1], int(line[2]), int(line[3]))
            else:
                agents[line[1]] = Ghost(line[1], int(line[2]), int(line[3]))
            i += 1
        self._agent_manager.set_agents(agents)

        if err := self._board_manager.load(lines[i + 1:]) is not None:
            return err

        self._path_board = path

    def gather_qlearning_state(self) -> None:
        return None  # TODO

    def gather_cli_state(self) -> tuple[list[list[Cell]], list[Agent]]:
        return (
            self._board_manager.get_all_cells(),
            self._agent_manager.get_all_agents()
        )

    def get_replay(self) -> tuple[str, list[list[Action]]]:
        return (self._path_board, self._history)

    def step(self, actions: list[Action]) -> None:
        assert isinstance(actions, list)
        assert len(actions) > 0
        assert isinstance(actions[0], Action)

        for action in actions:
            if self._can_apply(action):
                self._apply(action)
            else:
                # if action is invalid, will try to redo last action
                agent = self._agent_manager.get_agent(action.id)
                last_action = Action(action.id, agent.get_last_direction())
                if self._can_apply(last_action):
                    self._apply(last_action)
                else:
                    continue  # correct behavior ?

        # check collision
        collisions = self._board_manager.get_collisions(self._agent_manager.get_all_agents())

        for col in collisions:
            agent = self._agent_manager.get_agent(col[0])

            # collision with cell
            if isinstance(col[1], Cell):
                if isinstance(agent, Pacman):
                    if col[1] == Cell['WALL']:
                        return PacErrPacmanInWall(col)
                    elif col[1] == Cell['DOOR']:
                        return PacErrPacmanInWall(col)
                    elif col[1] == Cell['PAC_DOT']:
                        agent.add_score(5)
                        self._board_manager.set_cell(agent.get_position(), Cell['EMPTY'])
                    elif col[1] == Cell['PAC_GUM']:
                        continue  # TODO

            # collision with agent
            else:
                # other = self._agent_manager.get_agent(col[1])
                pass
                # TODO

        self._history.append(actions)

    def _can_apply(self, action: Action) -> bool:
        assert isinstance(action, Action)

        agent = self._agent_manager.get_agent(action.id)
        cell = self._board_manager.get_cell(agent.try_move(action.direction))

        out = False
        if isinstance(agent, Pacman):
            if cell not in (Cell['WALL'], Cell['DOOR']):
                out = True
        else:
            if cell != Cell['WALL']:
                out = True

        return out

    def _apply(self, action) -> None:
        assert isinstance(action, Action)

        agent = self._agent_manager.get_agent(action.id)
        agent.move(action.direction)
