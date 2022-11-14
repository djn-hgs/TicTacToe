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
    def __init__(self, parent, game):
        super().__init__(parent)
        self.parent = parent
        self.game = game

        game_grid = TicTacToeGrid(self, self.game)

        game_grid.grid(sticky='news')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class TicTacToeGrid(tk.Frame):
    def __init__(self, parent, game):
        super().__init__(parent)
        self.parent = parent
        self.game = game

        self.cell_grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        for i in range(3):
            for j in range(3):
                print(j)
                new_cell = TicTacToeCell(self, self.game, (i, j))

                self.cell_grid[i][j] = new_cell

                new_cell.grid(row=i, column=j, sticky='news')

        for i in range(3):
            self.rowconfigure(i, weight=1)

        for i in range(3):
            self.columnconfigure(i, weight=1)


class TicTacToeCell(tk.Button):
    def __init__(self, parent, game, pos):
        self.parent = parent
        self.game = game
        self.pos = pos

        super().__init__(self.parent, command=self.clicked)

    def clicked(self):
        print(f'Clicked {self.pos}')

        if self.game.peek(self.pos):
            print('Nope')
        else:
            counter = self.game.current_player.pop_counter()

            self.game.play_counter(counter, self.pos)

            self.configure(text=counter.label)

            self.game.check_for_winner()

            if self.game.has_winner:
                print(f'Winner is {self.game.winner}')
            else:
                self.game.next_turn()

        print(self.game.get_grid())


my_app = GameApp(ttt.Game())

tk.mainloop()
