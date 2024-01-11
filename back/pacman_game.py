from back.board_manager import BoardManager
from back.agent_manager import AgentManager
from back.agent import Agent
from back.team import Team
from utils.action import Action
from utils.direction import Direction
from back.errors import PacErrAgentInWall
from back.cell import Cell
from back.pacman import Pacman
from back.ghost import Ghost

import os.path as os_path

from utils.distance_matrix import DistanceMatrix


class PacmanGame():
    """Root class of this pacman game inplementation
    """
    _board_manager: BoardManager
    _agent_manager: AgentManager
    _path_board: str
    _is_game_over: bool
    winning_team: int

    def __init__(self) -> None:
        """PacmanGame's initialization
        """
        self._board_manager = BoardManager()
        self._agent_manager = AgentManager()
        self._path_board = None
        self._is_game_over = False
        self.winning_team = None

    def load_map(self, path: str) -> None:
        """Load a pacman map from a file path

        :param path: path to the map file to load
        :type path: str
        """
        assert isinstance(path, str)

        if not os_path.exists(path):
            return FileNotFoundError()
        self._path_board = path

        with open(path, 'r') as file:
            lines = file.readlines()

        # load board
        board_description = lines[lines.index('|\n') + 1:]
        self._board_manager.load(board_description, path)

        # load agents
        agents_description = lines[:lines.index('|\n')]
        self._agent_manager.load(agents_description, self._board_manager.get_board_size())

        # first perception
        self._agent_manager.update_perceptions(self._board_manager)

    def gather_state(self) -> tuple[Team]:
        """Get the game's state

        :return: game's state, wich is the teams informations with their perceptions
        :rtype: tuple[Team]
        """
        return self._agent_manager.get_teams()

    def gather_cli_state(self) -> tuple[list[list[Cell]], list[Agent]]:
        """Get the the board description necessary to represent it in the cli

        :return: board description for cli representation
        :rtype: tuple[list[list[Cell]], list[Agent]]
        """
        return (
            self._board_manager.get_all_cells(),
            self._agent_manager.get_all_agents()
        )

    def step(self, actions: list[Action]) -> None:
        """Step the pacman's game simulation by applying the agent's actions

        :param actions: list of all the agent's actions for this simulation step
        :type actions: list[Action]
        """
        assert isinstance(actions, list)
        assert len(actions) > 0
        assert isinstance(actions[0], Action)

        actionIterator = 0
        while (actionIterator < len(actions)):
            action = actions[actionIterator]
            if self._can_apply(action):
                self._apply(action)
                # See the repercussions of the action on the others and adding the modified actions
                actions = actions[:actions.index(action)] + self.repercuting_actions(action, actions[actions.index(action):])

                # Verify collisions with board
                agent = self._agent_manager.get_agent(action.id)
                collisions = self._board_manager.get_collisions(agent)
                # collision with cell
                for col in collisions:
                    if isinstance(col, Cell):
                        if isinstance(agent, Pacman):
                            if col == Cell['WALL']:
                                return PacErrAgentInWall(col)
                            elif col == Cell['PAC_DOT']:
                                agent.add_score(5)
                                self._board_manager.set_cell(agent.get_position(), Cell['EMPTY'])
                            elif col == Cell['PAC_GUM']:
                                agent.eat_pacgum()
                                agentList = self._agent_manager.get_all_agents()
                                for agentIterator in agentList:
                                    if (isinstance(agentIterator, Ghost) and agentIterator.get_team() != agent.get_team()):
                                        agentIterator.set_vulnerability(True)
                                self._board_manager.set_cell(agent.get_position(), Cell['EMPTY'])
            else:
                # if action is invalid, will try to redo last action
                # agent = self._agent_manager.get_agent(action.id)
                # last_action = Action(action.id, agent.get_last_direction())
                # if self._can_apply(last_action):
                #    self._apply(last_action)
                # else:
                #    continue  # TODO: Change behavior be cause redo the previous can cause issues

                # If action is invalid, does nothing, may be the best action to avoid breaking the game
                pass

            actionIterator += 1

        # update team's perception
        self._agent_manager.update_perceptions(self._board_manager)

        # check collision
        # collisions = self._board_manager.get_collisions(self._agent_manager.get_all_agents())
        # for col in collisions:
        #    agent = self._agent_manager.get_agent(col[0])
        #    # collision with cell
        #    if isinstance(col[1], Cell):
        #        if isinstance(agent, Pacman):
        #            if col[1] == Cell['WALL']:
        #                return PacErrAgentInWall(col)
        #            elif col[1] == Cell['PAC_DOT']:
        #                agent.add_score(5)
        #                self._board_manager.set_cell(agent.get_position(), Cell['EMPTY'])
        #            elif col[1] == Cell['PAC_GUM']:
        #                agent.eat_pacgum()
        #    # collision with agent
        #    else:
        #        pass

    def repercuting_actions(self, currentAction: Action, allActions: list[Action]) -> list[Action]:
        """See which other actions have a repercussion on the on the agent making the action (like a ghost eating a pacman) and modify the necessary parameters

        :param currentAction: Action for which we want to see the impact
        :type currentAction: Action

        param allActions: list of all the agent's actions for this simulation step
        :type allActions: list[Action]

        return list[Action]
        """
        # Get the current action's agent (currentAgent)
        currentAgent = self.get_agent_manager().get_agent(currentAction.id)
        actionsToRemove = []
        actionsToAdd = []

        # Verify if another action is bothering the current action
        for action in allActions:
            # Get the verified action's agent (actionAgent)
            actionAgent = self._agent_manager.get_agent(action.id)

            # See if the action we want to verify is legal and not the current action we are viewing
            if ((action != currentAction) and (actionAgent._alive) and (self._can_apply(action))):

                # See if the actionAgent is next to currentAgent(orthogonally) and can have a repercussion on the agent
                distanceAgents = (currentAgent.get_position()[0] - actionAgent.get_position()[0], currentAgent.get_position()[1] - actionAgent.get_position()[1])
                if ((distanceAgents[0] == 0) or (distanceAgents[1] == 0)):
                    # Verify if actions make the agents pass each other or puts them on the same space
                    futureAgentPosition = (actionAgent.get_position()[0] + action.direction.value[0], actionAgent.get_position()[1] + action.direction.value[1])
                    if ((currentAgent.get_position() == futureAgentPosition) or (distanceAgents == (0, 0))):
                        # The current agent is a pacman
                        if (isinstance(currentAgent, Pacman)):
                            # He is interacting with a pacman
                            if (isinstance(actionAgent, Pacman)):
                                # Apply an opposing action to undo the movement
                                oppositeCurrentAction = Action(currentAction.id, currentAction.direction.opposite())
                                if (self._can_apply(oppositeCurrentAction)):
                                    self._apply(oppositeCurrentAction)
                                # Remove the bothering action to block
                                actionsToRemove.append(action)
                            # He is interacting with a ghost
                            elif (isinstance(actionAgent, Ghost)):
                                if currentAgent.is_invicible():
                                    actionAgent.die()
                                    actionsToAdd.append(Action(actionAgent.get_id(), Direction.RESPAWN))
                                else:
                                    currentAgent.die()
                                    actionsToAdd.append(Action(currentAgent.get_id(), Direction.RESPAWN))
                            # WTF is he interacting with ?
                            else:
                                print("Error ! Not authorized object making a movement !" + actionAgent.get_id())
                        # The current agent is a Ghost
                        elif (isinstance(currentAgent, Ghost)):
                            # He is interacting with a pacman
                            if (isinstance(actionAgent, Pacman)):
                                if actionAgent.is_invicible():
                                    currentAgent.die()
                                    actionsToAdd.append(Action(currentAgent.get_id(), Direction.RESPAWN))
                                else:
                                    actionAgent.die()
                                    actionsToAdd.append(Action(actionAgent.get_id(), Direction.RESPAWN))
                            # He is interacting with a ghost
                            elif (isinstance(actionAgent, Ghost)):
                                # Apply an opposing action to undo the movement
                                oppositeCurrentAction = Action(currentAction.id, currentAction.direction.opposite())
                                if (self._can_apply(oppositeCurrentAction)):
                                    self._apply(oppositeCurrentAction)
                                # Remove the bothering action to block
                                actionsToRemove.append(action)
                            # WTF is he interacting with ?
                            else:
                                print("Error ! Not authorized object making a movement !" + actionAgent.get_id())
                        # WTF is the current agent ?
                        else:
                            print("Error ! Not authordized object making a movement !" + currentAction.get_id())

        # Verify the positions of the other agents bother the current action
        agentList = self.get_agent_manager().get_all_agents()
        for agent in agentList:
            if agent != currentAgent:
                if currentAgent.get_position() == agent.get_position():
                    # Apply an opposing action that can be assimilated to a bounce
                    oppositeCurrentAction = Action(currentAction.id, currentAction.direction.opposite())
                    if (self._can_apply(oppositeCurrentAction)):
                        self._apply(oppositeCurrentAction)

        # Remove all actions unneeded
        for action in actionsToRemove:
            allActions.remove(action)
        allActions += actionsToAdd
        return allActions

    def _can_apply(self, action: Action) -> bool:
        """Check if an agent's action can be applied

        :param action: action to test
        :type action: Action
        :return: True if the action is legal, False if not
        :rtype: bool
        """
        assert isinstance(action, Action)

        agent = self._agent_manager.get_agent(action.id)
        cell = self._board_manager.get_cell(agent.try_move(action.direction))

        if isinstance(agent, Pacman):
            if cell != Cell['WALL']:
                return True
        else:
            if cell != Cell['WALL']:
                return True
        return False

    def _apply(self, action: Action) -> None:
        """Apply an action

        :param action: action to apply
        :type action: Action
        """
        assert isinstance(action, Action)

        agent = self._agent_manager.get_agent(action.id)
        # See i f the resoawn is direct or not
        # if action.direction == Direction.NONE:
        #    pass
        if action.direction == Direction.RESPAWN:
            agent.respawn()
        else:
            if (isinstance(agent, Pacman) and agent.is_invicible()):
                if not agent.invicibility_left():

                    agentList = self._agent_manager.get_all_agents()
                    for agentIterator in agentList:
                        if (isinstance(agentIterator, Ghost) and agentIterator.get_team() != agent.get_team()):
                            agentIterator.set_vulnerability(False)

                    agent.vulnerable()
                else:
                    agent.reduce_invicibility()
            agent.move(action.direction)

    def get_board_size(self) -> tuple[int, int]:
        """Get the game's board size

        :return: the game's board size (width, height)
        :rtype: tuple[int, int]
        """
        return self._board_manager.get_board_size()

    def reset(self) -> None:
        """Reset of the game
        """
        self._agent_manager.reset()
        self._board_manager.reset()
        self._is_game_over = False

    def get_teams(self) -> None:
        """Get the game's teams
        """
        return self._agent_manager.get_teams()

    def get_agent_manager(self) -> AgentManager:
        """
        Get the agent manager of the game
        :return: the agent manager
        :rtype : AgentManager
        """
        return self._agent_manager

    def get_board_distances(self) -> DistanceMatrix:
        return self._board_manager.get_board_distances()

    def is_game_over(self) -> bool:
        """Check if the game is over

        :return: True if the game is over, False if not
        :rtype: bool
        """
        if self._is_game_over is True:
            return True

        # check if the game is over
        if self._board_manager.is_game_over() is True:
            self._is_game_over = True
            t1, t2 = self._agent_manager.get_teams()
            self.winning_team = 0 if t1.get_score() > t2.get_score() else 1
        if self._agent_manager.is_game_over() is True:
            self._is_game_over = True
            t1, t2 = self._agent_manager.get_teams()
            self.winning_team = 0 if t1.get_pacman().is_alive() else 1

        return self._is_game_over
