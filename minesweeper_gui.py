import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox, QGridLayout, QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
from minesweeper import Minesweeper

class MinesweeperGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game = Minesweeper()
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_time = 0
        
    def initUI(self):
        self.setWindowTitle('Minesweeper')
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        
        # Timer label
        self.timer_label = QLabel('Time: 0')
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet('color: red; font-size: 16px')
        self.central_layout.addWidget(self.timer_label)

        # Grid widget and layout
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(2)  # Set space between buttons to 2 pixels
        self.central_layout.addWidget(self.grid_widget, alignment=Qt.AlignCenter)
        
        self.setCentralWidget(self.central_widget)
        self.buttons = {}
        
        for row in range(self.game.rows_nb):
            for col in range(self.game.cols_nb):
                button = QPushButton('')
                button.setFixedSize(40, 40)
                button.setStyleSheet('background-color: lightgray')
                button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                button.clicked.connect(self.button_clicked)
                self.grid_layout.addWidget(button, row, col)
                self.buttons[(row, col)] = button
        
        self.show()

    def start_timer(self):
        self.timer.start(1000)  # Update every second
        self.elapsed_time = 0
        self.update_timer()

    def update_timer(self):
        self.elapsed_time += 1
        self.timer_label.setText(f'Time: {self.elapsed_time}')
    
    def stop_timer(self):
        self.timer.stop()

    def button_clicked(self):
        button = self.sender()
        row, col = [(r, c) for (r, c), b in self.buttons.items() if b == button][0]
        
        if self.game.first_click:
            self.start_timer()
        
        self.reveal_cells(row, col)
        if self.game.check_win():
            self.stop_timer()
            self.game_over(True)

    def reveal_cells(self, row, col):
        self.game.reveal_cells(row, col)
        for r in range(self.game.rows_nb):
            for c in range(self.game.cols_nb):
                if self.game.is_revealed(r, c):
                    value = self.game.get_cell_value(r, c)
                    button = self.buttons[(r, c)]
                    label = QLabel(str(value) if value != 0 else '')
                    label.setFixedSize(40, 40)
                    label.setAlignment(Qt.AlignCenter)
                    label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                    if value == 0:
                        label.setStyleSheet('background-color: white')
                    elif value == -1:
                        label.setText('M')
                        label.setStyleSheet('background-color: red')
                    else:
                        self.set_label_color(label, value)
                    self.grid_layout.replaceWidget(button, label)
                    button.deleteLater()
                    self.buttons[(r, c)] = label
                    if value == -1:
                        self.stop_timer()
                        self.game_over(False)

    def set_label_color(self, label, value):
        colors = {
            1: 'blue',
            2: 'green',
            3: 'red',
            4: 'darkblue',
            5: 'darkred',
            6: 'cyan',
            7: 'black',
            8: 'gray'
        }
        if value in colors:
            label.setStyleSheet(f'color: {colors[value]}; background-color: white')
    
    def game_over(self, win):
        msg = QMessageBox()
        if win:
            msg.setWindowTitle("Congratulations!")
            msg.setText(f"You win! Time: {self.elapsed_time} seconds")
        else:
            msg.setWindowTitle("Game Over")
            msg.setText("You clicked on a mine.")
        msg.exec_()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = MinesweeperGUI()
    sys.exit(app.exec_())
