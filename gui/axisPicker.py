from PyQt5 import QtWidgets
import gui.axis_pickerUI as aP


class AxisPicker(aP.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, axlist):
        super(AxisPicker, self).__init__()
        self.setupUi(self)

        self.cb_axis.addItems(axlist)

