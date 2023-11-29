

import copy
from algorithms.flood_fill import FloodFill
from back.team import Team
from utils.action import Action
from utils.direction import Direction
from back.cell import Cell
from algorithms.a_star import AStar


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
                if board.get_cell(new_pos) in (Cell['WALL']):
                    continue
                positions.append(copy.copy(new_pos))
            possible_positions[agent.get_id()] = copy.deepcopy(positions)

        # other team agents positions and probability
        # TODO bake probability in possible positions and optimize position count of ennemies not seen for a while
        for value in pacman_sighting + ghost_sightings:
            how_long_ago, agent = value
            og_x, og_y = agent.get_position()
            positions = [(og_x, og_y)]
            # iterate on positions of a square of size how_long_ago, centered on agent last seen position
            for dx in range(-how_long_ago, how_long_ago + 1):
                for dy in range(-how_long_ago, how_long_ago + 1):
                    # quit if distance is to great for the agent to have reached it
                    if abs(dx) + abs(dy) > how_long_ago:
                        continue
                    x, y = og_x + dx, og_y + dy
                    # quit if outside of board
                    if not (0 <= x < board_width and 0 <= y < board_height):
                        continue
                    # quit if is an illegal position
                    if board.get_cell((x, y)) in (Cell['WALL']):
                        continue
                    # second, more precise check of distance
                    if astar.distance((x, y), (og_x, og_y)) > how_long_ago:
                        continue
                    # finaly position is valid, so we keep it
                    if not (x, y) in positions:
                        positions.append((og_x + dx, og_y + dy))
            possible_positions[agent.get_id()] = positions

        # chose action
        out = []
        for decisional_agent in team.get_agents():
            # build state probability list
            states = [[[], 1]]  # list of [[[all agent positions], probability]]
            decisional_agent_id = decisional_agent.get_id()
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
            print(decisional_agent_id)
            for action in possible_positions[decisional_agent_id]:
                eu = 0
                for og_positions, probability in states:
                    positions = copy.deepcopy(og_positions)
                    positions[positions.index(None)] = action
                    eu += self.utility(positions, all_ids, team) * probability
                expected_utilities.append(eu)

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

    def utility(self, positions, all_ids, team: Team) -> float:
        # simple combination of the following metrics :
        # - distance to score gain
        # - distance to explored cell gain
        # - team's agent danger level
        # - other team's agent danger level

        # general data
        perception = team.get_perception()
        board = perception.get_board()
        width, height = board.get_size()
        team_ids = list(team.get_ids())
        flood_fill = FloodFill(board)
        a_star = AStar(board)

        # distance to score gain
        pacman_pos = positions[all_ids.index(team.get_pacman().get_id())]
        min_dist_to_score = flood_fill.closest_cell(pacman_pos[0], pacman_pos[1], Cell['PAC_DOT'])

        # distance to unknown cell
        min_dist_to_unknown = []
        for id, position in zip(all_ids, positions):
            if id not in team_ids:
                continue
            min_dist_to_unknown.append(flood_fill.closest_cell(position[0], position[1], Cell['UNKNOWN']))

        # team's danger level
        danger = 0
        other_team_danger = 0
        for time, enemy_ghost in perception.get_ghost_sightings():
            if enemy_ghost.is_vulnerable():
                other_team_danger += a_star.distance(team.get_pacman().get_position(), enemy_ghost.get_position())
            else:
                danger += a_star.distance(team.get_pacman().get_position(), enemy_ghost.get_position())

        pacman_sighting = perception.get_pacman_sighting()
        if pacman_sighting != []:
            enemy_pacman = pacman_sighting[0][1]
            for ghost in team.get_ghosts():
                if ghost.is_vulnerable():
                    danger += a_star.distance(enemy_pacman.get_position(), ghost.get_position())
                else:
                    other_team_danger += a_star.distance(enemy_pacman.get_position(), ghost.get_position())

        print(min_dist_to_score, min(min_dist_to_unknown), danger, other_team_danger)
        return -min_dist_to_score / 30 - min(min_dist_to_unknown) / 30 - danger / 90 + other_team_danger / 90
