

import copy
from algorithms.flood_fill import FloodFill
from back.agent import Agent
from back.pacman import Pacman
from back.team import Team
from utils.action import Action
from utils.direction import Direction
from back.cell import Cell
from algorithms.a_star import AStar
from random import random
from utils.replay_logger import ReplayLogger


class Utility():

    def __init__(self) -> None:
        self.directions = (Direction['UP'],
                           Direction['RIGHT'],
                           Direction['DOWN'],
                           Direction['LEFT'])

    def run(self, team: Team) -> list[Action]:
        assert isinstance(team, Team)

        # important data
        possible_positions = {}  # contains agent_id: [(x, y), (x,y), ...]
        position_probability = {}  # contains agent_id: [probability, probability, ...]
        # used data
        perception = team.get_perception()
        board = perception.get_board()
        board_width, board_height = board.get_size()
        pacman_sighting = perception.get_pacman_sighting()
        ghost_sightings = perception.get_ghost_sightings()
        all_ids = list(team.get_ids()) + perception.get_ids()
        astar = AStar(board)

        # decisional agent's team agents positions and probability
        for agent in team.get_agents():
            positions = []
            for direction in self.directions:
                new_pos = agent.try_move(direction)
                if board.get_cell(new_pos) == Cell['WALL']:
                    continue
                positions.append(copy.copy(new_pos))
            possible_positions[agent.get_id()] = copy.deepcopy(positions)
            position_probability[agent.get_id()] = [1 / len(positions)] * len(positions)

        # other team agents positions and probability
        for value in pacman_sighting + ghost_sightings:
            how_long_ago, agent = value
            og_x, og_y = agent.get_position()
            positions = [(og_x, og_y)]
            nb_of_positions_probability_count_for = [1]
            nb_skipped = 0
            # iterate on positions of a square of size how_long_ago, centered on agent last seen position
            for dx in range(-how_long_ago - 1, how_long_ago + 2):
                for dy in range(-how_long_ago - 1, how_long_ago + 2):
                    # quit if distance is to great for the agent to have reached it
                    if abs(dx) + abs(dy) > how_long_ago + 1:
                        continue
                    x, y = og_x + dx, og_y + dy
                    # quit if outside of board
                    if not (0 <= x < board_width and 0 <= y < board_height):
                        continue
                    # quit if is an illegal position
                    if board.get_cell((x, y)) == Cell['WALL']:
                        continue
                    # second, more precise check of distance
                    if astar.distance((x, y), (og_x, og_y)) > how_long_ago + 2:
                        continue
                    # random chance to skip this position
                    if random() > 1 / (how_long_ago + 1 / 2 + nb_skipped):
                        nb_skipped += 1
                        continue
                    # finaly position is valid, so we keep it
                    if not (x, y) in positions:
                        positions.append((og_x + dx, og_y + dy))
                        nb_of_positions_probability_count_for.append(nb_skipped + 1)
                        nb_skipped = 0
            possible_positions[agent.get_id()] = positions
            position_probability[agent.get_id()] = [1 / len(positions) * nb_of_positions_probability_count_for[i] for i in range(len(positions))]

        # chose action
        out = []
        for decisional_agent in team.get_agents():
            # build state probability list
            states = [[[], 1]]  # list of [[[all agent positions], probability]] TODO change
            decisional_agent_id = decisional_agent.get_id()
            ReplayLogger().log_comment(f'{decisional_agent_id}')
            for id in all_ids:
                new_states = []
                # decisional agent's positions is filled with None for later replacement
                if id == decisional_agent_id:
                    for state in states:
                        new_states.append([state[0] + [None], state[1]])
                        states = copy.copy(new_states)
                    continue

                for state in states:
                    probability = 1 / len(possible_positions[id])
                    for position in possible_positions[id]:
                        new_states.append([state[0] + [position], state[1] * probability])
                states = copy.copy(new_states)

            # measure expected utilities
            expected_utilities = []
            for action in possible_positions[decisional_agent_id]:
                eu = 0
                for og_positions, probability in states:
                    positions = copy.deepcopy(og_positions)
                    positions[positions.index(None)] = action
                    eu += self.utility(positions, all_ids, team) * probability
                expected_utilities.append(eu)
                ReplayLogger().log_comment(f'{action} : {eu}')

            # choose max expected utility
            chosen_action = possible_positions[decisional_agent_id][expected_utilities.index(max(expected_utilities))]
            out.append((decisional_agent_id, chosen_action))
            possible_positions[decisional_agent_id] = [chosen_action]

        # translate out to Actions
        new_out = []
        for id, new_pos in out:
            pos = team.get_agent(id).get_position()
            dpos = (new_pos[0] - pos[0], new_pos[1] - pos[1])
            deltas = ((0, -1), (1, 0), (0, 1), (-1, 0))
            directions = (Direction['UP'], Direction['RIGHT'], Direction['DOWN'], Direction['LEFT'])
            if dpos == (0, 0):
                new_out.append(Action(id, team.get_agent(id).get_last_direction()))
            else:
                new_out.append(Action(id, directions[deltas.index(dpos)]))
        return new_out

    def utility(self, description: list[tuple[int, int]], all_ids: list[str], team: Team) -> float:
        # simple combination of the following metrics :
        # - distance to score gain
        # - distance to explored cell gain
        # - team's agent danger level
        # - other team's agent danger level

        # build positions: dict[(str, int, int): tuple[int, int]]
        perception = team.get_perception()
        positions = {}
        team_number = team.get_team_number()
        for p, id in zip(description, all_ids):
            if id in team.get_ids():
                if id == team.get_pacman().get_id():
                    positions[(id, team_number, 1)] = p
                else:
                    positions[(id, team_number, 0)] = p
            else:
                if id in perception.get_ghost_ids():
                    positions[(id, team_number + 1, 0)] = p
                else:
                    positions[(id, team_number + 1, 1)] = p

        # general data
        board = perception.get_board()
        flood_fill = FloodFill(board)
        a_star = AStar(board)
        enemy_ghosts = []
        enemy_pacman = None
        team_ghosts = []
        team_pacman = None
        for id, team_number, type in positions.keys():
            if team_number == team.get_team_number():
                if type == 1:  # is pacman
                    team_pacman = (id, team_number, type)
                else:  # is ghost
                    team_ghosts.append((id, team_number, type))
            else:
                if type == 1:  # is pacman
                    enemy_pacman = (id, team_number, type)
                else:  # is ghost
                    enemy_ghosts.append((id, team_number, type))

        # distance to score gain
        pacman_pos = positions[(team.get_pacman().get_id(), team.get_team_number(), 1)]
        min_dist_to_score = flood_fill.closest_cell(pacman_pos[0], pacman_pos[1], Cell['PAC_DOT'])

        # distance to unknown cell
        min_dist_to_unknown = []
        for agent in team_ghosts + [team_pacman]:
            x, y = positions[agent]
            min_dist_to_unknown.append(flood_fill.closest_cell(x, y, Cell['UNKNOWN']))

        # team's and other team's danger level
        danger = 0
        other_team_danger = 0
        # team's pacman
        if team.get_pacman().is_invicible():  # is not vulnerable
            for ghost in enemy_ghosts:
                other_team_danger += a_star.distance(positions[ghost], positions[team_pacman])
            for ghost in team_ghosts:
                danger += a_star.distance(positions[ghost], positions[team_pacman])
        else:  # is vulnerable
            for ghost in team_ghosts + enemy_ghosts:
                danger += a_star.distance(positions[ghost], positions[team_pacman])
        # enemy's pacman
        if enemy_pacman is not None:
            if team.get_ghosts()[0].is_vulnerable():  # is not vulnerable
                for ghost in enemy_ghosts:
                    other_team_danger += a_star.distance(positions[ghost], positions[enemy_pacman])
                for ghost in team_ghosts:
                    danger += a_star.distance(positions[ghost], positions[enemy_pacman])
            else:  # is vulnerable
                for ghost in enemy_ghosts + team_ghosts:
                    other_team_danger += a_star.distance(positions[ghost], positions[enemy_pacman])

        return -min_dist_to_score / 30 - min(min_dist_to_unknown) / 30 + danger / 20 - other_team_danger / 20
