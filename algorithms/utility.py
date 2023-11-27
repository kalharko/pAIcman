

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
        board = team.get_perception().get_board()
        board_width, board_height = board.get_size()
        last_pacman_seen = team.get_perception().get_pacman_sightings()
        last_ghost_seen = team.get_perception().get_ghost_sightings()
        team_ids = list(team.get_ids())
        all_ids = list(last_pacman_seen.keys()) + list(last_ghost_seen.keys())
        other_ids = copy.copy(all_ids)
        for id in team_ids:
            other_ids.remove(id)
        astar = AStar(board)

        # decisional agent's team agents positions and probability
        for agent in team.get_agents():
            positions = []
            for direction in self.directions:
                new_pos = agent.try_move(direction)
                if board.get_cell(new_pos[0], new_pos[1]) in (Cell['WALL'], Cell['DOOR']):
                    continue
                positions.append(copy.copy(new_pos))
            possible_positions[agent.get_id()] = copy.deepcopy(positions)

        # other team agents positions and probability
        # TODO bake probability in possible positions and optimize position count of ennemies not seen for a while
        for agent_id, value in last_seen.items():
            if agent_id in team_ids:
                continue
            how_long_ago, position = value
            og_x, og_y = position
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
                    if board.get_cell(x, y) in (Cell['WALL'], Cell['DOOR']):
                        continue
                    # second, more precise check of distance
                    if astar.distance((x, y), (og_x, og_y)) > how_long_ago:
                        continue
                    # finaly position is valid, so we keep it
                    if not (x, y) in positions:
                        positions.append((og_x + dx, og_y + dy))
            possible_positions[agent_id] = positions

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
        board = team.get_perception().get_board()
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
        # TODO

        # other team's agent danger level
        # TODO

        return 1 / (1 + min_dist_to_score) + len(min_dist_to_unknown) / sum(min_dist_to_unknown)
