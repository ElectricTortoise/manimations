class Board:
    def __init__(self):
        self.board = [0 for _ in range(9)]
        self.player = 1
        self.gameOver = False

    def MakeMove(self, square):
        self.board[square] = self.player
        self.IsGameOver()
        self.player *= -1

    def IsGameOver(self):
        for row in range(0,9,3):
            rowSum = 0
            for rowSquare in range(row, row+3):
                rowSum += self.board[rowSquare]
            if rowSum == 3 or rowSum == -3:
                self.gameOver = True

        for col in range(3):
            colSum = 0
            for colSquare in range(col,9,3):
                colSum += self.board[colSquare]
            if colSum == 3 or colSum == -3:
                self.gameOver = True

        if self.board[0] == self.board[4] == self.board[8] != 0:
            self.gameOver = True
        if self.board[2] == self.board[4] == self.board[6] != 0:
            self.gameOver = True

