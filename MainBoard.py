import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QMainWindow, QFrame
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.Qt import QCursor
import os
from AutoCell import Space
import config


class Board(QFrame):

    msg2_status_bar = pyqtSignal(str)
    Speed = config.speed

    def __init__(self, parent):
        super().__init__(parent)

        self.isStarted = False
        self.isLoaded = False
        self.isCustomized = False

        self.cur_map = Space()
        self.BoardSize = self.cur_map.size()
        self.board = []
        self.board_top = 0
        self.board_left = 0

        self.timer = QBasicTimer()
        self.time_passed = 0

        self.init_board()

    def init_board(self):
        self.setFocusPolicy(Qt.StrongFocus)
        self.clear_board()

    def status(self, i, j):
        return self.board[(i * self.BoardSize[0]) + j]
        # return self.board[(x * self.BoardWidth) + y]

    def set_status(self, time_passed):
        level = time_passed % 2
        for i in range(self.BoardSize[1]):
            for j in range(self.BoardSize[0]):
                self.board[(i * self.BoardSize[0]) + j] = self.cur_map.space[i][j][level]

    def square_size(self):
        square_width = self.contentsRect().width() // self.BoardSize[0]
        square_height = self.contentsRect().height() // self.BoardSize[1]
        if square_height > square_width:
            return square_width
        else:
            return square_height

    def start(self):
        self.msg2_status_bar.emit(str(self.time_passed))
        self.timer.start(config.speed, self)

    def pause(self, pressed):
        if pressed:
            print('start')
            self.isStarted = True
            self.timer.start(config.speed, self)
            self.msg2_status_bar.emit(str(self.time_passed))
        else:
            print('pause')
            self.isStarted = False
            self.timer.stop()
            self.msg2_status_bar.emit('paused')

    def new_map(self):
        if self.isStarted:
            self.cur_map.new_map(self.time_passed)
            self.time_passed = self.time_passed + 1

        self.set_status(self.time_passed)
        self.update()

    def paintEvent(self, event):
        # print('done %s' % event.timerId())
        painter = QPainter(self)
        rect = self.contentsRect()

        # left_edge = self.left_edge

        self.board_top = rect.bottom() - self.BoardSize[1] * self.square_size()
        self.board_left = rect.left()

        for i in range(self.BoardSize[1]):
            for j in range(self.BoardSize[0]):
                life_status = self.status(i, j)
                self.draw_points(painter,
                                 rect.left() + i * self.square_size(),
                                 self.board_top - 1 + j * self.square_size(),
                                 life_status)

        self.msg2_status_bar.emit(str(self.time_passed))

    def draw_points(self, painter, x, y, life_status):
        colors = [0xffffff, 0x000000]
        color = QColor(colors[life_status])
        painter.fillRect(y + 1, x + 1, self.square_size() - 1,
                         self.square_size() - 1, color)

    def timerEvent(self, event):

        if event.timerId() == self.timer.timerId():
            if self.isStarted and self.isLoaded:
                self.new_map()
        else:
            super(Board, self).timerEvent(event)

    def clear_board(self):
        for _ in range(self.BoardSize[0] * self.BoardSize[1]):
            self.board.append(0)

    def load_map(self, text):
        if not self.isStarted and self.time_passed == 0:
            self.cur_map.reload_map(text)
            self.BoardSize = self.cur_map.size()
            self.cur_map.new_map(self.time_passed)
            self.isLoaded = True
            self.set_status(self.time_passed)
            self.update()

    def reset(self):
        print('reset')
        if not self.isStarted:
            if self.time_passed > 0:
                self.timer.stop()
            self.isLoaded = False
            self.time_passed = 0
            self.cur_map.reload_map('')
            self.set_status(self.time_passed)
            self.msg2_status_bar.emit(str(self.time_passed))
            self.update()

    def diy(self, state):
        if state == Qt.Checked:
            self.isCustomized = True
        else:
            self.isCustomized = False

    def mousePressEvent(self, event):
        if self.isCustomized:
            cur_x = event.localPos().x()
            cur_y = event.localPos().y()
            if not self.isStarted and self.time_passed == 0:
                col = int((cur_x - self.board_top) // self.square_size())
                row = int((cur_y - self.board_left) // self.square_size())
                if 0 <= col < self.BoardSize[0] and 0 <= row < self.BoardSize[1]:
                    print([col, row])
                    self.cur_map.change_map([col, row])
                    self.set_status(self.time_passed)
                    self.update()
        if self.cur_map.get_lives() > 0:
            self.isLoaded = True
        else:
            self.isLoaded = False



