import tkinter as tk
import tictactoe as ttt


class GameApp(tk.Tk):
    def __init__(self, game):
        super().__init__()

        self.geometry('400x300')

        self.game = game

        self.gui = GameGUI(self, self.game)

        self.gui.grid(sticky='news')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class GameGUI(tk.Frame):
    def __init__(self, parent: tk.Tk, game: ttt.Game):
        super().__init__(parent)
        self.parent = parent
        self.game = game

        game_grid = TicTacToeGrid(self, self.game)

        game_grid.grid(sticky='news')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class TicTacToeGrid(tk.Frame):
    def __init__(self, parent: tk.Widget, game: ttt.Game):
        super().__init__(parent)
        self.parent = parent
        self.game = game

        self.cell_grid = []

        for i in range(3):
            self.cell_grid.append([])

            for j in range(3):
                new_cell = TicTacToeCell(self, self.game, (i, j), self.update)
                new_cell.grid(row=i, column=j, sticky='news')

                self.cell_grid[i].append(new_cell)

        for i in range(3):
            self.rowconfigure(i, weight=1)

        for i in range(3):
            self.columnconfigure(i, weight=1)

    def update(self):
        pass


class TicTacToeCell(tk.Button):
    def __init__(self, parent: tk.Widget, game: ttt.Game, pos: tuple[int, int], parent_update=None):
        self.parent = parent
        self.game = game
        self.pos = pos
        self.parent_update = parent_update

        super().__init__(self.parent, command=self.clicked)

    def clicked(self):
        print(f'Clicked {self.pos}')

        if not self.game.peek(self.pos):
            if self.game.current_player.has_counters():

                counter = self.game.current_player.pop_counter()

                self.game.play_counter(counter, self.pos)

            if not self.game.has_winner:
                self.game.next_turn()

        else:
            print('Nope')

        self.update()

        if self.parent_update:
            self.parent_update()

    def update(self):
        counter: ttt.Counter = self.game.peek(self.pos)

        if counter:
            self.configure(text=counter.label)
        else:
            self.configure(text='')

        print(self.game.get_grid())


my_app = GameApp(ttt.Game())

tk.mainloop()
