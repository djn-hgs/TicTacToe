import tkinter as tk
import tictactoe as ttt


class GameApp(tk.Tk):
    def __init__(self, game):
        self.game = game

        super().__init__()

        # Size of app window

        self.geometry('400x300')

        # Place GUI on window

        self.gui = GameGUI(self, self.game)

        # Layout

        self.gui.grid(sticky='news')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class GameGUI(tk.Frame):
    def __init__(self, parent: tk.Tk, game: ttt.Game):
        self.parent = parent
        self.game = game

        super().__init__(parent)

        # Simple GUI - just grid and status bar

        self.game_grid = TicTacToeGrid(self, self.game, self.status_update)
        self.status_label = tk.Label(self)

        # Layout

        self.game_grid.grid(row=0, column=0, sticky='news')
        self.status_label.grid(row=1, column=0, sticky='ew')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        # Populate controls

        self.status_update()

    def status_update(self):

        # Build status text

        status_text = ''

        status_text += f'Current player: {self.game.current_player.name}.'

        if self.game.has_winner:
            status_text += f' {self.game.winner.name} wins.'

        # And update box

        self.status_label.configure(text=status_text)


class TicTacToeGrid(tk.Frame):
    def __init__(self, parent: tk.Widget, game: ttt.Game, update_method=None):

        # Store parameter values

        self.parent = parent
        self.game = game
        self.update_method = update_method

        super().__init__(self.parent)

        # Grid to store the cells

        self.cell_grid: list[list[TicTacToeCell]] = []

        # Build rows and columns

        for i in range(3):
            self.cell_grid.append([])

            for j in range(3):

                # Create cell and layout using grid

                new_cell = TicTacToeCell(self, self.game, (i, j), self.update_method)
                new_cell.grid(row=i, column=j, sticky='news')

                # Store cell to grid

                self.cell_grid[i].append(new_cell)

        # Describe layout

        for i in range(3):
            self.rowconfigure(i, weight=1)

        for i in range(3):
            self.columnconfigure(i, weight=1)

    def update(self):

        # The grid itself consists only of the cells,
        # so updating really just updates the cells

        for row in self.cell_grid:
            for cell in row:
                cell.update()


class TicTacToeCell(tk.Button):
    def __init__(self, parent: tk.Widget, game: ttt.Game, pos: tuple[int, int], update_method=None):

        # Store the parameter values

        self.parent = parent
        self.game = game
        self.pos = pos
        self.update_method = update_method

        super().__init__(self.parent, command=self.clicked)

    def clicked(self):
        if not self.game.peek(self.pos):
            if self.game.current_player.has_counters():

                # Get next counter to play

                counter = self.game.current_player.pop_counter()

                # Play the counter

                self.game.play_counter(counter, self.pos)

                # Move to the next play

                self.game.next_turn()

        # Show current cell value after a change

        self.update()

        # Get parent widget to update itself

        if self.update_method:
            self.update_method()

    def update(self):
        # This will find the counter, if any, that is stored in this cell's position

        counter: ttt.Counter = self.game.peek(self.pos)

        # Show label for this counter, or a blank cell

        if counter:
            self.configure(text=counter.label)
        else:
            self.configure(text='')


# Create one of our apps to run our tic-tac-toe game

my_app = GameApp(ttt.Game())

tk.mainloop()
