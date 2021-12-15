from PyQt5 import QtWidgets
from gui import trimgui as tg


class TrimDialog(tg.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super(TrimDialog, self).__init__()
        self.setupUi(self)

