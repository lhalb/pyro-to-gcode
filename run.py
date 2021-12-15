import sys
from PyQt5 import QtWidgets
from gui import startUI as sUI


def main():
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    form = sUI.MyApp()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

