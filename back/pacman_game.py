from back.board_manager import BoardManager
from back.agent_manager import AgentManager
from back.agent import Agent
from back.team import Team
from utils.action import Action
from back.errors import PacErrAgentInWall
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

    def load_map(self, path: str) -> None:
        assert isinstance(path, str)

        if not os_path.exists(path):
            return FileNotFoundError()
        self._path_board = path

        with open(path, 'r') as file:
            lines = file.readlines()

        # load board
        board_description = lines[lines.index('|\n') + 1:]
        self._board_manager.load(board_description)

        # load agents
        agents_description = lines[:lines.index('|\n')]
        self._agent_manager.load(agents_description, self._board_manager.get_board_size())

        # first perception
        self._agent_manager.update_perceptions(self._board_manager)

    def gather_state(self) -> tuple[Team]:
        return self._agent_manager.get_teams()

    def gather_cli_state(self) -> tuple[list[list[Cell]], list[Agent]]:
        return (
            self._board_manager.get_all_cells(),
            self._agent_manager.get_all_agents()
        )

    def step(self, actions: list[Action]) -> None:
        assert isinstance(actions, list)
        assert len(actions) > 0
        assert isinstance(actions[0], Action)

        # apply actions
        self._history.append(actions)
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

        # update team's perception
        self._agent_manager.update_perceptions(self._board_manager)

        # check collision
        collisions = self._board_manager.get_collisions(self._agent_manager.get_all_agents())

        for col in collisions:
            agent = self._agent_manager.get_agent(col[0])

            # collision with cell
            if isinstance(col[1], Cell):
                if isinstance(agent, Pacman):
                    if col[1] == Cell['WALL']:
                        return PacErrAgentInWall(col)
                    elif col[1] == Cell['DOOR']:
                        return PacErrAgentInWall(col)
                    elif col[1] == Cell['PAC_DOT']:
                        agent.add_score(5)
                        self._board_manager.set_cell(agent.get_position(), Cell['EMPTY'])
                    elif col[1] == Cell['PAC_GUM']:
                        continue  # TODO

            # collision with agent
            else:
                pass

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

    def get_board_size(self) -> tuple[int, int]:
        return self._board_manager.get_board_size()

    def reset(self) -> None:
        self._agent_manager.reset()
        self._board_manager.reset()

    def get_history(self) -> None:
        return self._history
