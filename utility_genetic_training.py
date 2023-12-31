from argparse import ArgumentParser
import copy
import random
from front.cli.cli_replay import CliReplay
from main import Main
from os import listdir
import time
import pickle

if __name__ != '__main__':
    exit(0)

parser = ArgumentParser(prog='Utility Genetic Training for Paicman',
                        description='Use genetic algorithm to find the best parameters for the utility algorithm',
                        epilog='epilog')
parser.add_argument('-m', '--map_path',
                    help='path to the map to use',
                    default='maps/9x9.txt')
parser.add_argument('-b', '--include_best',
                    help='include the best individual in the initial population',
                    default=False,)
args = parser.parse_args()


# Constants
NB_GENES = 12
POP_SIZE = 30
TOURNAMENT_SIZE = 4
SELECTION_PRESSURE = 0.9
NB_PARENTS = 8
NB_CHILDREN = 20
MUTATION_RATE = 0.01
BREADING_RATE = 0.5
NB_ITERATIONS = 4
CROSS_ALPHA = [0.5, 1.5, -0.3]
CROSS_BETA = [0.5, -0.5, 1.5]

main = Main(args.map_path, 'utility', 'utility', verbose=True)
print(f'Training on map {args.map_path}')


def display_individual(individual) -> None:
    out = '('
    for gene in individual:
        out += str(gene)[:4] + ', '
    out = out[:-2] + ')'
    print(out)


def select_parent_indexes(population, nb_parents=NB_PARENTS, pressure=SELECTION_PRESSURE, tournament_size=TOURNAMENT_SIZE) -> tuple[list[int], set[int]]:
    print(f'Selecting {nb_parents} parents')
    # parent selection through tournament
    parents = []
    tested_indexes = set()
    while len(parents) < nb_parents:
        print('len(parents)', len(parents))
        # participants selection
        participants = []
        while len(participants) < tournament_size:
            rd = random.randint(0, POP_SIZE - 1)
            if rd not in participants:
                participants.append(rd)
                tested_indexes.add(rd)

        print('starting tournament with', len(participants), 'participants')

        # tournament TODO include length of games to advantage fast wins
        results = [[0 for i in range(tournament_size)] for j in range(tournament_size)]
        for p1 in participants:
            print('p1', display_individual(population[p1]))
            for p2 in participants:
                if p1 == p2:
                    continue
                print('p2', display_individual(population[p2]))
                # setup match
                main.reset()
                main.set_teams_utility_parameters(population[p1], population[p2])
                i = 0
                while main.cycle() and i < 15:
                    print('\r' + str(i), end='')
                    i += 1
                CliReplay()
                print()
                if main.get_winning_team_number() == 0:
                    results[participants.index(p1)][participants.index(p2)] += 1
                    results[participants.index(p2)][participants.index(p1)] -= 1
                else:
                    results[participants.index(p1)][participants.index(p2)] -= 1
                    results[participants.index(p2)][participants.index(p1)] += 1

        # best selection
        scores = [sum(line) for line in results]
        for i in range(tournament_size):
            max_index = scores.index(max(scores))
            if random.random() < pressure * ((1 - pressure) ** i):
                parents.append(max_index)
            scores[max_index] = -tournament_size

    if len(parents) > NB_PARENTS:
        parents = parents[:NB_PARENTS]
    return parents, tested_indexes


def cross_breading(population, parent_indexes) -> list[tuple[int]]:
    print(f'Crossing {NB_CHILDREN} children')
    children = []
    i = 0
    while len(children) < NB_CHILDREN:
        rd = random.randint(0, NB_PARENTS - 1)
        if rd > BREADING_RATE:  # probability for sterility
            continue
        parent1 = i % NB_PARENTS
        parent2 = (i + 1) % NB_PARENTS
        for j in range(len(CROSS_ALPHA)):
            k = random.ranrange(NB_GENES)  # random gene index
            gene = CROSS_ALPHA[j] * population[parent1][k] + CROSS_BETA[j] * population[parent2][k]
            child = population[parent1][:k] + (gene) + population[parent2][k:]
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
        mutants.append(child[:random_gene] + (gene) + child[random_gene:])
    return mutants


# initial population
population = []
if args.include_best:
    best_paths = listdir('data/genetic/best_individuals/')
    print('Including best individual', best_paths)[-1]
    population.append(tuple(pickle.load(open(best_paths[-1], 'rb'))))
while len(population) < POP_SIZE:
    population.append(tuple((random.random() for i in range(NB_GENES))))

for iter in range(NB_ITERATIONS):
    print('\nIteration', iter)
    # select parents
    parent_indexes, population_tested_indexes = select_parent_indexes(population)
    # crossover
    children = cross_breading(population, parent_indexes)
    # mutation
    mutants = mutations(children)
    # compile next population
    new_population = []
    new_population += children
    new_population += mutants
    while len(new_population) < POP_SIZE:
        rd = random.randrange(POP_SIZE)
        if rd not in population_tested_indexes:
            new_population.append(population[rd])
    # set new population
    population = copy.deepcopy(new_population)


# tournament to find best individual
best = population[select_parent_indexes(population, nb_parents=1, tournament_size=POP_SIZE, pressure=1)[0][0]]

# save best individual
print(best)
pickle.dump(best, open('data/genetic/best_individuals/' + time.strftime("%Y%m%d-%H%M%S") + '.pkl', 'wb'))
