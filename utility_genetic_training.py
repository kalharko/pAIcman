from argparse import ArgumentParser
import copy
import random
from main import Main
from os import listdir
import time
import pickle
from math import inf


if __name__ != '__main__':
    exit(0)

parser = ArgumentParser(prog='Utility Genetic Training for Paicman',
                        description='Use genetic algorithm to find the best parameters for the utility algorithm',
                        epilog='epilog')
parser.add_argument('-m', '--map_path',
                    help='path to the map to use',
                    default='maps/6x9.txt')
parser.add_argument('-b', '--include_best',
                    help='include the best individual in the initial population',
                    default=False,)
args = parser.parse_args()


# Constants
NB_GENES = 12
POP_SIZE = 15
TOURNAMENT_SIZE = 4
SELECTION_PRESSURE = 0.99
NB_PARENTS = 5
NB_CHILDREN = 5
MUTATION_RATE = 0.1
BREADING_RATE = 0.9
NB_ITERATIONS = 40
CROSS_ALPHA = [1.5]
CROSS_BETA = [-0.5]

main = Main(args.map_path, 'utility', 'utility', verbose=True)
print(f'Training on map {args.map_path}')


def display_individual(individual) -> None:
    out = '('
    for gene in individual:
        out += str(gene)[:4] + ', '
    out = out[:-2] + ')'
    print(out)


def select_parent_indexes(population, nb_parents=NB_PARENTS, pressure=SELECTION_PRESSURE, tournament_size=TOURNAMENT_SIZE, include_results: bool = False) -> tuple[list[int], set[int]]:
    print(f'Selecting {nb_parents} parents')
    # parent selection through tournament
    parents = []
    game_lengths = [[] for i in population]
    while len(parents) < nb_parents:
        print('\nlen(parents)', len(parents))
        # participants selection
        participants = []
        while len(participants) < tournament_size:
            rd = random.randint(0, POP_SIZE - 1)
            if rd not in participants:
                participants.append(rd)

        print('starting tournament with', len(participants), 'participants')

        # tournament TODO include length of games to advantage fast wins
        results = [[0 for i in range(tournament_size)] for j in range(tournament_size)]
        debug_i = 0
        for p1 in participants:
            for p2 in participants:
                if p1 == p2:
                    continue
                print('\r|  ', debug_i, end='')
                debug_i += 1
                # setup match
                main.reset()
                main.set_teams_utility_parameters(population[p1], population[p2])
                i = 0
                while main.cycle() and not main.is_repeating() and i < 50:
                    i += 1
                if main.environment.is_game_over():
                    if main.get_winning_team_number() == 0:
                        results[participants.index(p1)][participants.index(p2)] += 1
                        results[participants.index(p2)][participants.index(p1)] -= 1
                    else:
                        results[participants.index(p1)][participants.index(p2)] -= 1
                        results[participants.index(p2)][participants.index(p1)] += 1
                if main.is_repeating():
                    game_lengths[p1].append(250)
                    game_lengths[p1].append(250)
                game_lengths[p1].append(i)
                game_lengths[p2].append(i)
        print()

        # best selection
        scores = [sum(line) for line in results]
        for i in range(tournament_size):
            max_index = scores.index(max(scores))
            if random.random() < pressure * ((1 - pressure) ** i):
                parents.append(max_index)
                print('max_index', max_index)
            scores[max_index] = -tournament_size

    for line in game_lengths:
        print(line)

    if len(parents) > NB_PARENTS:
        parents = parents[:NB_PARENTS]
    if include_results:
        return parents, game_lengths, results
    return parents, game_lengths


def cross_breading(population, parent_indexes) -> list[tuple[int]]:
    print(f'Crossing {NB_CHILDREN} children')
    children = []
    i = 0
    while len(children) < NB_CHILDREN:
        rd = random.randint(0, NB_PARENTS - 1)
        if rd > BREADING_RATE:  # probability for sterility
            continue
        parent1 = parent_indexes[i % len(parent_indexes)]
        parent2 = parent_indexes[(i + 1) % len(parent_indexes)]
        for j in range(len(CROSS_ALPHA)):
            k = random.randrange(NB_GENES)  # random gene index
            gene = CROSS_ALPHA[j] * population[parent1][k] + CROSS_BETA[j] * population[parent2][k]
            child = tuple((parent_gene if gene_index != k else gene for gene_index, parent_gene in enumerate(population[parent1])))
            children.append(child)
        i += 1

    if len(children) > NB_CHILDREN:
        children = children[:NB_CHILDREN]
    return children


def mutations(children) -> list[tuple[int]]:
    print(f'Mutation {len(children)} children')
    mutants = []
    for child in children:
        rd = random.random()
        if rd > MUTATION_RATE:
            continue
        # random gene multiplication
        random_gene = random.randrange(NB_GENES)
        gene = child[random_gene] * random.uniform(-2, 2)
        mutants.append(tuple((child_gene if gene_index != random_gene else gene for gene_index, child_gene in enumerate(child))))
    return mutants


# initial population
population = []
if args.include_best:
    best_paths = listdir('data/genetic/best_individuals/')
    print('Including best individuals')
    i = 0
    while i < min(NB_PARENTS // 2, len(best_paths)):
        population.append(tuple(pickle.load(open(best_paths[i], 'rb'))))
        i += 1
    population.append(tuple(pickle.load(open(best_paths[-1], 'rb'))))
while len(population) < POP_SIZE:
    population.append(tuple((random.random() for i in range(NB_GENES))))

for iter in range(NB_ITERATIONS):
    print('\nIteration', iter)
    # select parents
    parent_indexes, game_lengths = select_parent_indexes(population)
    # crossover
    children = cross_breading(population, parent_indexes)
    # mutation
    mutants = mutations(children)
    # compile next population
    new_population = []
    new_population += children
    new_population += mutants
    # add untested individuals
    for i in range(POP_SIZE):
        if game_lengths[i] == []:
            new_population.append(population[i])
    print('new pop is :')
    print(f'\t{len(children)} children')
    print(f'\t{len(mutants)} mutants')
    print(f'\t{len(new_population) - len(children) - len(mutants)} untested individuals')
    print(f'\t{POP_SIZE - len(new_population)} from the best tested individuals')
    print()
    # add best tested individuals
    average_length_of_games = []
    for i in range(POP_SIZE):
        if game_lengths[i] == []:
            average_length_of_games.append(inf)
        else:
            average_length_of_games.append(sum(game_lengths[i]) / len(game_lengths[i]))
    while len(new_population) < POP_SIZE:
        min_index = average_length_of_games.index(min(average_length_of_games))
        new_population.append(population[min_index])
        average_length_of_games[min_index] = inf
    # set new population
    population = copy.deepcopy(new_population)


# tournament to find best individual
parents, tested_indexes, results = select_parent_indexes(population, nb_parents=1, tournament_size=POP_SIZE, pressure=1, include_results=True)
best = population[parents[0]]

print()
for line in results:
    for char in line:
        print(str(char) + ' ' * (4 - len(str(char))), end=' ')
    print()
print()

# save best individual
print(best)
pickle.dump(best, open('data/genetic/best_individuals/' + time.strftime("%Y%m%d-%H%M%S") + '.pkl', 'wb'))
