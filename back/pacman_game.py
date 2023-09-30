from back.board_manager import BoardManager
from back.agent_manager import AgentManager
from back.action import Action
from back.errors import PacErrInvalidAction, PacErrPacmanInWall
from back.cell import Cell
from back.pacman import Pacman

import os.path.exist as does_path_exist


class PacmanGame():
    _board_manager: BoardManager
    _agent_manager: AgentManager

    def __init__(self) -> None:
        self._board_manager = BoardManager()
        self._agent_manager = AgentManager()

    def load(self, path: str) -> None:
        assert isinstance(path, str)

        if not does_path_exist(path):
            return FileNotFoundError()

        if err := self._board_manager.load(path) is not None:
            return err

    def gather_qlearning_state(self) -> None:
        return None  # TODO

    def gather_cli_state(self) -> None:
        return None  # TODO

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
        collisions = self._board_manager.get_collisions(self._agent_manager(get_all_agents()))

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
                    elif col[1] == Cell['PAC_GUM']:
                        continue  # TODO

            # collision with agent
            else:
                other = self._agent_manager.get_agent(col[1])
                # TODO

    def _can_apply(self, action: Action) -> bool:
        assert isinstance(action, Action)

        agent = self._agent_manager.get_agent(action.id)
        cell = self._board_manager.get_cell(agent.try_move(action.direction))

        out = false
        if isinstance(agent, Pacman):
            if cell not in (Cell['WALL'], Cell['DOOR']):
                out = true
        else:
            if cell != Cell['WALL']:
                out = true

        agent.reverse(action.direction)
        return out

    def _apply(self, action) -> None:
        assert isinstance(action, Action)

        agent = self._agent_manager.get_agent(action.id)
        agent.move(action.direction)
