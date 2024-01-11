from argparse import ArgumentParser
from main import Main
from utils.replay_logger import ReplayLogger


if __name__ != '__main__':
    exit(0)

parser = ArgumentParser(prog='Paicman',
                        description='Run the strategies comparisons',
                        epilog='epilog')
parser.add_argument('-t', '--test',
                    help='select which test to run, can be, all, gathering, random or versus',
                    default='all')
parser.add_argument('-s', '--strategy',
                    help='select which strategy to run the test on, can be, all, utility or behaviors',
                    default='all')
args = parser.parse_args()

# variables
map_paths = [
    'maps/original.txt',
    'maps/original_0.txt',
    'maps/original_1.txt',
    'maps/original_2.txt',
]

# Gathering test
if args.test == 'all' or args.test == 'gathering':
    if args.strategy == 'all' or args.strategy == 'utility':
        # utility
        print("Start utility gathering test")
        main = Main('maps/gathering.txt', 'utility', 'utility')
        utility_gathering_time = main.play_until_game_over()
        print(f"Utility gathering time : {utility_gathering_time}")
        ReplayLogger().log_map('maps/gathering.txt')
        ReplayLogger().save_replay('data/comparison/utility_gathering.pkl')
        ReplayLogger().reset()

    if args.strategy == 'all' or args.strategy == 'behaviors':
        # behaviors
        print("Start behaviors gathering test")
        main = Main('maps/gathering.txt', 'behaviors', 'behaviors')
        behaviors_gathering_time = main.play_until_game_over()
        print(f"Behaviors gathering time : {behaviors_gathering_time}")
        ReplayLogger().log_map('maps/gathering.txt')
        ReplayLogger().save_replay('data/comparison/behaviors_gathering.pkl')
        ReplayLogger().reset()


# Versus random strategy
if args.test == 'all' or args.test == 'random':
    if args.strategy == 'all' or args.strategy == 'utility':
        # utility
        print("Start utility versus random test")
        mains = [Main(map_path, 'utility', 'random') for map_path in map_paths]

        utility_wins_against_random = []
        utility_times_agains_random = []
        for i, (main, map_path) in enumerate(zip(mains, map_paths)):
            time = main.play_until_game_over()
            utility_times_agains_random.append(time)
            utility_wins_against_random.append(main.get_winning_team_number() == 1)
            ReplayLogger().log_map(map_path)
            ReplayLogger().save_replay('data/comparison/utility_vs_random_' + str(i) + '.pkl')
            ReplayLogger().reset()
        print(f"Utility versus random average time : {sum(utility_times_agains_random) / len(utility_times_agains_random)}")
        print(f"Utility versus random win rate : {sum(utility_wins_against_random) / len(utility_wins_against_random)}")

    if args.strategy == 'all' or args.strategy == 'behaviors':
        # behaviors
        print("Start behaviors versus random test")
        mains = [Main(map_path, 'behaviors', 'random') for map_path in map_paths]

        behaviors_wins_against_random = []
        behaviors_times_agains_random = []
        for i, (main, map_path) in enumerate(zip(mains, map_paths)):
            time = main.play_until_game_over()
            behaviors_times_agains_random.append(time)
            behaviors_wins_against_random.append(main.get_winning_team_number() == 1)
            ReplayLogger().log_map(map_path)
            ReplayLogger().save_replay('data/comparison/behaviors_vs_random_' + str(i) + '.pkl')
            ReplayLogger().reset()
        print(f"Behaviors versus random average time : {sum(behaviors_times_agains_random) / len(behaviors_times_agains_random)}")
        print(f"Behaviors versus random win rate : {sum(behaviors_wins_against_random) / len(behaviors_wins_against_random)}")


# Versus
if args.test == 'all' or args.test == 'versus':
    print("Start versus test")
    mains = [Main(map_path, 'utility', 'behaviors') for map_path in map_paths]

    utility_wins_against_behaviors = []
    utility_times_agains_behaviors = []
    for i, (main, map_path) in enumerate(zip(mains, map_paths)):
        time = main.play_until_game_over()
        utility_times_agains_behaviors.append(time)
        utility_wins_against_behaviors.append(main.get_winning_team_number() == 1)
        ReplayLogger().log_map(map_path)
        ReplayLogger().save_replay('data/comparison/versus_' + str(i) + '.pkl')
        ReplayLogger().reset()
    print(f"Utility versus behaviors average time : {sum(utility_times_agains_behaviors) / len(utility_times_agains_behaviors)}")
    print(f"Utility versus behaviors win rate : {sum(utility_wins_against_behaviors) / len(utility_wins_against_behaviors)}")
