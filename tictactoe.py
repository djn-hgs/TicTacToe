# A counter has a name and a position
# I subclass to create the specific "0" and "X" counters
class Counter:
    def __init__(self):
        self.pos = None
        self.label = None

    def __repr__(self):
        return f'{self.label} at {self.pos}'
    
    def set_pos(self, pos):
        self.pos = pos

    def get_pos(self):
        return self.pos


class Nought(Counter):
    def __init__(self):
        super().__init__()

        self.label = "O"


class Cross(Counter):
    def __init__(self):
        super().__init__()

        self.label = "X"


# A player just has a name and some counters

class Player:
    def __init__(self, name):
        self.name = name
        self.counters = []

    def __str__(self):
        return f'{self.name} - {self.counters}'

    def add_counter(self, my_counter):
        self.counters.append(my_counter)

    def pop_counter(self):
        return self.counters.pop()


# This is our game

class Game:
    def __init__(self):

        # This is a two player game

        self.player1 = Player('Arthur')
        self.player2 = Player('Boris')

        # Somewhere to place counters in the game

        self.placed_counters = []

        # The state of the game
        
        self.has_winner = False
        self.winner = None

        # How do we know who plays next? Easy for tic-tac-tow

        self.successor_dict = {
            self.player1: self.player2,
            self.player2: self.player1
        }

        # Who's going first?

        self.current_player = self.player1

        # Give each player some counters - six is more than enough in tic-tac-toe!

        for i in range(6):
            self.player1.add_counter(Nought())
            self.player2.add_counter(Cross())
            
        # These are all the winning plays for tic-tac-toe

        self.winning_plays = {
            self.player1: [
                ([(0, 0), (1, 0), (2, 0)], Nought),
                ([(0, 1), (1, 1), (2, 1)], Nought),
                ([(0, 2), (1, 2), (2, 2)], Nought),

                ([(0, 0), (0, 1), (0, 2)], Nought),
                ([(1, 0), (1, 1), (1, 2)], Nought),
                ([(2, 0), (2, 1), (2, 2)], Nought),

                ([(0, 2), (1, 1), (2, 0)], Nought),
                ([(0, 0), (1, 1), (2, 2)], Nought)
            ],
            self.player2: [
                ([(0, 0), (1, 0), (2, 0)], Cross),
                ([(0, 1), (1, 1), (2, 1)], Cross),
                ([(0, 2), (1, 2), (2, 2)], Cross),

                ([(0, 0), (0, 1), (0, 2)], Cross),
                ([(1, 0), (1, 1), (1, 2)], Cross),
                ([(2, 0), (2, 1), (2, 2)], Cross),

                ([(0, 2), (1, 1), (2, 0)], Cross),
                ([(0, 0), (1, 1), (2, 2)], Cross)
            ]
        }

    def play_counter(self, my_counter, pos):
        my_counter.set_pos(pos)
        self.placed_counters.append(my_counter)

    def next_turn(self):
        self.current_player = self.successor_dict[self.current_player]
        
    def check_for_winner(self):
        for candidate in self.winning_plays:
            for (plays, target) in self.winning_plays[candidate]:

                matches = [counter.pos for counter in self.placed_counters if isinstance(counter, target)]

                if all([play in matches for play in plays]):
                    self.has_winner = True
                    self.winner = candidate

    def peek(self, pos):
        for c in self.placed_counters:
            if c.pos == pos:
                return c
        return None

    def get_grid(self):
        grid = [[None, None, None],
                [None, None, None],
                [None, None, None]
        ]

        for c in self.placed_counters:
            c_row, c_col = c.pos
            grid[c_row][c_col] = c.label

        return grid


if __name__ == '__main__':
    my_game = Game()

    while not my_game.has_winner:
        counter = my_game.current_player.pop_counter()

        getting_choice = True

        row = 0
        col = 0

        while getting_choice:
            print(my_game.get_grid())
            print(f'Current player: {my_game.current_player.name}')
            row = int(input('Row:\t'))
            col = int(input('Column:\t'))

            if my_game.peek((row, col)):
                print('Invalid move')
                getting_choice = True
            else:
                getting_choice = False

        my_game.play_counter(counter, (row, col))
        my_game.check_for_winner()

        if not my_game.has_winner:
            my_game.next_turn()

    print(f'The winner is {my_game.winner}')
