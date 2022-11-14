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

        self.game_grid = TicTacToeGrid(self, self.game, self.status_update)
        self.status_label = tk.Label(self)

        self.game_grid.grid(row=0, column=0, sticky='news')
        self.status_label.grid(row=1, column=0, sticky='ew')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        self.status_update()

    def status_update(self):
        status_text = ''

        status_text += f'Current player: {self.game.current_player.name}.'

        if self.game.has_winner:
            status_text += f' {self.game.winner.name} wins.'

        self.status_label.configure(text=status_text)


class TicTacToeGrid(tk.Frame):
    def __init__(self, parent: tk.Widget, game: ttt.Game, update_method=None):
        self.parent = parent

        super().__init__(self.parent)

        self.game = game
        self.update_method = update_method

        self.cell_grid = []

        for i in range(3):
            self.cell_grid.append([])

            for j in range(3):
                new_cell = TicTacToeCell(self, self.game, (i, j), self.update_method)
                new_cell.grid(row=i, column=j, sticky='news')

                self.cell_grid[i].append(new_cell)

        for i in range(3):
            self.rowconfigure(i, weight=1)

        for i in range(3):
            self.columnconfigure(i, weight=1)

    def update(self):
        pass


class TicTacToeCell(tk.Button):
    def __init__(self, parent: tk.Widget, game: ttt.Game, pos: tuple[int, int], update_method=None):
        self.parent = parent
        self.game = game
        self.pos = pos
        self.update_method = update_method

        super().__init__(self.parent, command=self.clicked)

    def clicked(self):
        print(f'Clicked {self.pos}')

        if not self.game.peek(self.pos):
            if self.game.current_player.has_counters():

                counter = self.game.current_player.pop_counter()

                self.game.play_counter(counter, self.pos)
                self.game.next_turn()

        else:
            print('Nope')

        self.update()

        if self.update_method:
            self.update_method()

    def update(self):
        counter: ttt.Counter = self.game.peek(self.pos)

        if counter:
            self.configure(text=counter.label)
        else:
            self.configure(text='')

        print(self.game.get_grid())


my_app = GameApp(ttt.Game())

tk.mainloop()
