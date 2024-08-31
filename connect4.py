import tkinter as tk
from tkinter.ttk import Separator
from functools import partial

class ConnectFour:
    def __init__(self, window):
        self.window = window
        self.window.title("Menu")
        self.lblPlayer1 = tk.Label(self.window, text="Enter player 1 name:")
        self.lblPlayer1.grid(column=0, row=0, pady=5, sticky='e')
        self.entPlayer1 = tk.Entry(self.window)
        self.entPlayer1.grid(column=1, row=0, pady=5, sticky='w')
        self.lblPlayer2 = tk.Label(self.window, text="Enter player 2 name:")
        self.lblPlayer2.grid(column=0, row=1, pady=5, sticky='e')
        self.entPlayer2 = tk.Entry(self.window)
        self.entPlayer2.grid(column=1, row=1, pady=5, sticky='w')
        self.btnPlay = tk.Button(self.window, text="PLAY", bg='red', fg='white', command=self.play)
        self.btnPlay.grid(column=0, row=2, columnspan=2, padx=25, pady=5)
        self.btnLeaderboard = tk.Button(self.window, text="LEADERBOARD", bg='red', fg='white', command=self.leaderboard)
        self.btnLeaderboard.grid(column=0, row=3, columnspan=2, padx=25, pady=5)

    def play(self):
        self.player1 = self.entPlayer1.get()
        self.player2 = self.entPlayer2.get()
        self.newWindow = tk.Toplevel(self.window)
        self.game = Game(self.newWindow, self.player1, self.player2)

    def leaderboard(self):
        self.newWindow = tk.Toplevel(self.window)
        self.leaderboard = Leaderboard(self.newWindow)

class Leaderboard:
    def __init__(self, window):
        self.window = window
        self.window.title("Leaderboard")
        self.leadersWins = {}
        try:
            fin = open("records.txt", 'r')
        except FileNotFoundError:
            fout = open("records.txt", "w")
            fout.close()
            fin = open("records.txt", "r")
        self.recordsList = [line for line in fin]
        fin.close()
        for name in self.recordsList:
            if name not in self.leadersWins:
                self.leadersWins[name] = 1
            else:
                self.leadersWins[name] += 1
        self.leadersList = []
        for i, (value, key) in enumerate(zip(sorted(self.leadersWins.values(), reverse=True), sorted(self.leadersWins, key=self.leadersWins.get, reverse=True))):
            self.leadersList.append(f"{i+1}. {key}" + "." * (40 - (len(key) * 2)) + str(value))
        self.conRecords = tk.StringVar()
        self.lstRecords = tk.Listbox(self.window, width=20, height=10, listvariable=self.conRecords)
        self.lstRecords.grid(padx=75, pady=20)
        self.conRecords.set(self.leadersList)

class Game:
    def __init__(self, window, player1, player2):
        self.window = window
        self.player1 = player1
        self.player2 = player2
        self.window.title("Connect-4")
        self.spaces = []
        self.turn = "red"
        for i in range(7):
            self.spaces.append(i)
            self.spaces[i] = []
            for j in range(6):
                self.spaces[i].append(j)
                self.spaces[i][j] = tk.Label(self.window, width=2)
                self.spaces[i][j].grid(row=i, column=j, padx=5, pady=5)
        for i in range(6):
            Separator(self.window, orient=tk.VERTICAL).grid(column=i, row=0, rowspan=7, sticky='nsw')
        for i in range(7):
            Separator(self.window, orient=tk.HORIZONTAL).grid(column=0, row=i, columnspan=6, sticky='sew')
        self.playButtons = []
        for i in range(6):
            make_move_with_arg = partial(self.make_move, i)
            self.playButtons.append(i)
            self.playButtons[i] = tk.Button(self.window, width=2, height=1, bg='blue', command=make_move_with_arg)
            self.playButtons[i].grid(row=7, column=i, padx=5, pady=5)

    def make_move(self, x):
        for y in range(len(self.spaces)):
            if self.spaces[-(y + 1)][x].cget("bg") != "red" and self.spaces[-(y + 1)][x].cget("bg") != "yellow":
                self.spaces[-(y + 1)][x].config(bg=self.turn)
                if self.turn == "red":
                    self.turn = "yellow"
                elif self.turn == "yellow":
                    self.turn = "red"
                break
        if self.check_tie(self.spaces):
            self.game_over()
        if self.check_win("red"):
            self.update_leader(self.player1)
            self.game_over(self.player1)
        if self.check_win("yellow"):
            self.update_leader(self.player2)
            self.game_over(self.player2)

    def check_tie(self, board):
        for row in board:
            for spot in row:
                if spot.cget("bg") != "red" and spot.cget("bg") != "yellow":
                    return False
        return True

    def check_win(self, turn):
        boardHeight = len(self.spaces)
        boardWidth = len(self.spaces[0])
        for y in range(boardHeight):
            for x in range(boardWidth):
                #check horizontal
                try:
                    if self.spaces[y][x].cget("bg") == turn and self.spaces[y][x+1].cget("bg") == turn and self.spaces[y][x+2].cget("bg") == turn and self.spaces[y][x+3].cget("bg") == turn:
                        return True
                except IndexError:
                    continue
        for y in range(boardHeight):
            for x in range(boardWidth):
                #check vertical
                try:
                    if self.spaces[y][x].cget("bg") == turn and self.spaces[y+1][x].cget("bg") == turn and self.spaces[y+2][x].cget("bg") == turn and self.spaces[y+3][x].cget("bg") == turn:
                        return True
                except IndexError:
                    continue
        for y in range(boardHeight):
            for x in range(boardWidth):
                #check / diagonal
                try:
                    if self.spaces[y][x].cget("bg") == turn and self.spaces[y-1][x+1].cget("bg") == turn and self.spaces[y-2][x+2].cget("bg") == turn and self.spaces[y-3][x+3].cget("bg") == turn:
                        return True
                except IndexError:
                    continue
        for y in range(boardHeight):
            for x in range(boardWidth):
                #check \ diagonal
                try:
                    if self.spaces[y][x].cget("bg") == turn and self.spaces[y+1][x+1].cget("bg") == turn and self.spaces[y+2][x+2].cget("bg") == turn and self.spaces[y+3][x+3].cget("bg") == turn:
                        return True
                except IndexError:
                    continue
        return False

    def update_leader(self, winner):
        try:
            file = open("records.txt", "a")
            file.write(winner + "\n")
            file.close()
        except FileNotFoundError:
            file = open("records.txt", "w")
            file.write(winner + "\n")
            file.close()

    def game_over(self, winner):
        for button in self.playButtons:
            button.destroy()
        if winner == self.player1:
            self.lblResult = tk.Label(self.window, text=f"{self.player1} wins!")
        elif winner == self.player2:
            self.lblResult = tk.Label(self.window, text=f"{self.player2} wins!")
        elif winner == "tie":
            self.lblResult = tk.Label(self.window, text="It is a tie.")
        self.lblResult.grid(row=7, column=0, columnspan=6, padx=50, pady=10)
        self.btnDone = tk.Button(self.window, text="DONE", command=self.exit)
        self.btnDone.grid(row=8, column=0, columnspan=6, padx=50, pady=10)


    def exit(self):
        self.window.destroy()

def main():
    root = tk.Tk()
    app = ConnectFour(root)
    root.mainloop()

if __name__ == "__main__":
    main()
