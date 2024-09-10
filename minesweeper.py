import random

class Minesweeper:
    def __init__(self, rows_nb=10, cols_nb=10, mines_nb=10):
        self.rows_nb = rows_nb
        self.cols_nb = cols_nb
        self.mines_nb = mines_nb
        self.mines_positions = set()
        self.board = []
        self.visible_board = []
        self.first_click = True

    def get_neighbors(self, row, col):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= row + i < self.rows_nb and 0 <= col + j < self.cols_nb:
                    neighbors.append((row + i, col + j))
        return neighbors

    def create_board(self, first_row, first_col):
        self.board = [[0 for _ in range(self.cols_nb)] for _ in range(self.rows_nb)]
        self.mines_positions = set()

        # Define the cells to avoid placing mines in (first clicked cell and its neighbors)
        safe_zone = set(self.get_neighbors(first_row, first_col))
        safe_zone.add((first_row, first_col))

        while len(self.mines_positions) < self.mines_nb:
            row = random.randint(0, self.rows_nb - 1)
            col = random.randint(0, self.cols_nb - 1)
            if (row, col) in safe_zone or (row, col) in self.mines_positions:
                continue
            self.mines_positions.add((row, col))

        for (row, col) in self.mines_positions:
            self.board[row][col] = -1

        for row in range(self.rows_nb):
            for col in range(self.cols_nb):
                if self.board[row][col] == -1:
                    continue
                mine_count = sum(1 for (n_row, n_col) in self.get_neighbors(row, col) if self.board[n_row][n_col] == -1)
                self.board[row][col] = mine_count

        # Initialize the visible board with all cells hidden (e.g., None)
        self.visible_board = [[None for _ in range(self.cols_nb)] for _ in range(self.rows_nb)]

    def reveal_cells(self, row, col):
        if self.first_click:
            self.create_board(row, col)
            self.first_click = False

        if not (0 <= row < self.rows_nb and 0 <= col < self.cols_nb) or self.visible_board[row][col] is not None:
            return

        if self.board[row][col] == 0:
            self.visible_board[row][col] = 0
            for n_row, n_col in self.get_neighbors(row, col):
                self.reveal_cells(n_row, n_col)
        else:
            self.visible_board[row][col] = self.board[row][col]

    def is_revealed(self, row, col):
        return self.visible_board[row][col] is not None

    def get_cell_value(self, row, col):
        return self.visible_board[row][col]

    def check_win(self):
        for row in range(self.rows_nb):
            for col in range(self.cols_nb):
                if self.visible_board[row][col] is None and self.board[row][col] != -1:
                    return False
        return True