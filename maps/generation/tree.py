import copy
import random


global valid_states


class Board():
    board: list[list[int, str]]

    def __init__(self, board) -> None:
        self.board = board
        self.height = len(board)
        self.width = len(board[0])
        self.valid_board = True
        self.nb_filled = 20

    def get_legal_states(self, x, y):
        global valid_states

        current = self.get_state(x - 1, y - 1)
        legal = []
        for state in valid_states:
            valid = True
            for i in range(len(state)):
                if not isinstance(current[i], int) and current[i] != state[i]:
                    valid = False
                    break
            if valid:
                legal.append(state)
        return legal

    def state_is_legal(self, given_state) -> bool:
        for state in valid_states:
            valid = True
            for i in range(len(state)):
                if not isinstance(given_state[i], int) and given_state[i] != state[i]:
                    valid = False
                    break
            if valid:
                return True
        return False

    def get_legal_char(self, x, y):
        states = self.get_legal_states(x, y)
        chars = []
        for state in states:
            if not state[4] in chars:
                chars.append(state[4])
        if 'p' in chars:
            chars.remove('p')
        if '_' in chars:
            chars.remove('_')
        if 'n' in chars:
            chars.remove('n')
        if 'h' in chars:
            chars.remove('h')
        if 'v' in chars:
            chars.remove('v')
        if 'i' in chars:
            chars.remove('i')
        if 'u' in chars:
            chars.remove('u')
        # check legality of neighboors
        # for i, j, d in zip((-1, 0, 1, -1, 1, -1, 0, -1), (-1, -1, -1, 0, 0, 1, 1, 1), (8, 7, 6, 5, 3, 2, 1, 0)):
        #     try:
        #         state_to_check = list(self.get_state(x + i - 1, y + j - 1))
        #         to_del = []
        #         for char in chars:
        #             state_to_check[d] = char
        #             if not self.state_is_legal(state_to_check):
        #                 to_del.append(char)
        #         for char in to_del:
        #             chars.remove(char)
        #     except IndexError:
        #         pass

        return chars

    def get_state(self, x, y):
        return (self.board[y][x],
                self.board[y][x + 1],
                self.board[y][x + 2],
                self.board[y + 1][x],
                self.board[y + 1][x + 1],
                self.board[y + 1][x + 2],
                self.board[y + 2][x],
                self.board[y + 2][x + 1],
                self.board[y + 2][x + 2])

    def get_smallests(self):
        global valid_states

        smallests = []
        smallest_value = len(valid_states)
        for y in range(self.height):
            for x in range(self.width):
                if not isinstance(self.board[y][x], int):
                    continue
                if self.board[y][x] < smallest_value:
                    smallests = [(x, y)]
                    smallest_value = self.board[y][x]
                elif self.board[y][x] == smallest_value:
                    smallests.append((x, y))
        return smallests

    def apply(self, char, x, y):
        self.board[y][x] = char
        self.nb_filled += 1
        self.update()

    def update(self):
        bad_state = False
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if isinstance(self.board[y][x], int):
                    update = len(self.get_legal_char(x, y))
                    if update == 0:
                        bad_state = True
                    self.board[y][x] = update
        if bad_state:
            self.valid_board = False

    def get_completion(self):
        return self.nb_filled / (14 * 31) * 100

    def __str__(self):
        width = 0
        for line in self.board:
            for char in line:
                if len(str(char)) > width:
                    width = len(str(char))
        out = ''
        for line in self.board:
            for char in line:
                if char == 0:
                    # out += ' \033[91m' + str(char) + '\033[0m' + ' ' * (width - len(str(char)) - 1)
                    out += ' ' + str(char) + ' ' * (width - len(str(char)) - 1)
                out += ' ' + str(char) + ' ' * (width - len(str(char)) - 1)
            out += '\n'
        return out


class Node():
    def __init__(self, board) -> None:
        self.board = board
        self.children = None

    def build(self):
        self.children = []
        for x, y in self.board.get_smallests():
            for char in self.board.get_legal_char(x, y):
                self.children.append(
                    Node(copy.deepcopy(self.board)))
                self.children[-1].board.apply(char, x, y)

    def __str__(self) -> str:
        return str(self.valid_children)


#############################################
half_board_width = len('╔════════════╗p') + 2
board_height = 33


def load_states(path):
    with open(path, 'r', encoding="utf-8") as file:
        table = [['end' for i in range(half_board_width)]]
        for line in file.readlines():
            line = line.rstrip('\n')
            table.append(['end'] + list(line) + ['end'])
        table.append(['end' for i in range(half_board_width)])

    valid_states = []
    for y in range(board_height - 2):
        for x in range(half_board_width - 2):
            state = (
                table[y][x],
                table[y][x + 1],
                table[y][x + 2],
                table[y + 1][x],
                table[y + 1][x + 1],
                table[y + 1][x + 2],
                table[y + 2][x],
                table[y + 2][x + 1],
                table[y + 2][x + 2]
            )
            if state not in valid_states:
                valid_states.append(state)
    return valid_states


# load states
paths = (
    'template-specific.txt',
)
valid_states = []
for path in paths:
    for state in load_states(path):
        if state not in valid_states:
            valid_states.append(state)
print(f'{len(valid_states)} valid states have been loaded')

# initiate board
init_board = [['end' for i in range(half_board_width)]]
init_board += [['end'] + [0 for i in range(half_board_width - 3)] + ['p', 'end'] for y in range(12)]
init_board += [['end'] + [0 for i in range(half_board_width - 7)] + list('nhh_p') + ['end']]
init_board += [['end'] + [0 for i in range(half_board_width - 7)] + list('uiiip') + ['end'] for y in range(3)]
init_board += [['end'] + [0 for i in range(half_board_width - 7)] + list('vhhhp') + ['end']]
init_board += [['end'] + [0 for i in range(half_board_width - 3)] + ['p', 'end'] for y in range(14)]
init_board += [['end' for i in range(half_board_width)]]

# init_board = [['end' for i in range(26)]]
# init_board = [['end'] + list('0' * 23) + ['p', 'end'] for y in range(12)]
# init_board += [['end'] + list('0' * 10) + list('nhh__hhn') + list('0' * 5) + ['p', 'end']]
# init_board += [['end'] + list('0' * 10) + list('uiiiiiiu') + list('0' * 5) + ['p', 'end'] for y in range(3)]
# init_board += [['end'] + list('0' * 10) + list('nhhhhhhn') + list('0' * 5) + ['p', 'end']]
# init_board = [['end'] + list('0' * 23) + ['p', 'end'] for y in range(14)]
# init_board = [['end' for i in range(26)]]

init_board = Board(init_board)
print(init_board)
init_board.apply('end', 5, 0)
print(init_board)

# root
root = Node(init_board)
stack = [root]
node = root

step = 0
child_step_count = 0
avg_recording = [-4 for i in range(20)] + [0 for i in range(20)]
avg_trigger = 0.05
trigger_duration = 0
max_duration = 250
while stack != []:
    if sum(avg_recording[20:]) - sum(avg_recording[:20]) < 20 * avg_trigger:
        trigger_duration += 1
    if trigger_duration > 250 and node.board.get_completion() < 90:
        trigger_duration = 0
        node = random.choice(stack)
        stack.remove(node)
        print('avg triggered\n')
        avg_recording = [-1 for i in range(10)] + [0 for i in range(30)]
    else:
        node = stack.pop()
    avg_recording.pop(0)
    avg_recording.append(node.board.get_completion())

    if node.children is None:
        node.build()

    # display
    if child_step_count > 250:
        child_step_count = 0
        print(node.board)
        print('  step   stack  child  %       average %')
    step += 1
    child_step_count += len(node.children)
    print('  ' + str(step) + ' ' * (6 - len(str(step))),
          str(len(stack)) + ' ' * (6 - len(str(len(stack)))),
          str(len(node.children)) + ' ' * (6 - len(str(len(node.children)))),
          str(node.board.get_completion())[:4] + '%  ',
          str(sum(avg_recording[20:]) / 20 - sum(avg_recording[:20]) / 20)[:5],
          end='\r')

    if node.children == []:
        print('=== found leaf !')
        print(node.board)
        break

    random.shuffle(node.children)
    for child in node.children:
        if child.board.valid_board:
            stack.append(child)

if stack == []:
    print('Empty Stack')
print(node.board)
