import sys
from PyQt5.QtWidgets import QDesktopWidget, QCheckBox, QMainWindow, QComboBox, QPushButton
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
import os
from AutoCell import Space
import config
from MainBoard import Board


class AutoCell(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_board = Board(self)
        self.custom_check = QCheckBox('自定义', self)
        self.pause_button = QPushButton('开始', self)
        self.reset_button = QPushButton('重启', self)
        self.map_combo = QComboBox(self)
        self.status_bar = self.statusBar()

        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.main_board)
        self.pause_button.setCheckable(True)
        self.custom_check.move(1000, 50)
        self.pause_button.move(1000, 100)
        self.reset_button.move(1000, 200)
        for i in config.maps:
            self.map_combo.addItem(i)
        self.map_combo.move(1000, 300)

        self.custom_check.stateChanged.connect(self.main_board.diy)
        self.map_combo.activated[str].connect(self.main_board.load_map)
        self.reset_button.clicked.connect(self.main_board.reset)
        self.pause_button.clicked[bool].connect(self.main_board.pause)
        self.pause_button.clicked[bool].connect(self.pause)
        self.main_board.msg2_status_bar[str].connect(self.status_bar.showMessage)

        self.main_board.start()

        self.resize(1200, 900)
        self.setMinimumSize(1200, 900)

        self.map_combo.resize(150, 25)
        self.center()
        self.setWindowTitle('AutoCell')
        self.show()

    def pause(self, pressed):
        if pressed:
            self.pause_button.setText('暂停')
        else:
            self.pause_button.setText('开始')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
