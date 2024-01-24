from PyQt5 import QtCore, QtGui, QtWidgets
import login
import sys


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = login.zjuerLogin()
    ui.show()
    sys.exit(app.exec_())