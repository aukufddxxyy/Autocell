import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import AutoCell

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AutoCell()
    sys.exit(app.exec_())
