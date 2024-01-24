from PyQt5 import QtCore, QtGui, QtWidgets
from UI.login import *
import sys


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = zjuerLogin()
    ui.show()
    sys.exit(app.exec_())