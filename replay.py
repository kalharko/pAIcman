from front.cli.cli_replay import CliReplay
from argparse import ArgumentParser
import pickle


# parser = ArgumentParser(prog='replay for pacman saved game',
#                         description='Run two opposing teams in a pacman game',
#                         epilog='epilog')
# parser.add_argument('-p', '-path',
#                     help='path to the replay file',
#                     default='replay.pkl')

# args = parser.parse_args()
replay = pickle.load(open('last_replay.pkl', 'rb'))
clireplay = CliReplay(replay)
