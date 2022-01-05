from PyQt5 import QtGui, QtWidgets
from gui import errordiaUI as err


class ErrorDialogue(err.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, ang, errormessage, critical=False):
        super(ErrorDialogue, self).__init__()
        self.setupUi(self)

        warn_icon = QtGui.QPixmap(":/err/warning.png")
        err_icon = QtGui.QPixmap(":/err/error.png")

        self.message.setText(errormessage)

        self.retval = False
        self.ang = ang

        if not critical:
            self.icon.setPixmap(warn_icon)
            self.lab_ang.setText('Continue?')
            self.par_ang.hide()
            self.but_ok.setText('Yes')
            self.but_back.setText('No')
        else:
            self.par_ang.setValue(self.ang)
            self.icon.setPixmap(err_icon)
            self.but_ok.setText('OK')
            self.but_back.setText('Cancel')

        self.connect_buttons()

    def connect_buttons(self):
        self.but_ok.clicked.connect(self.ok_clicked)
        self.but_back.clicked.connect(self.cancel_clicked)

    def ok_clicked(self):
        self.retval = True
        self.ang = float(self.par_ang.text().replace(',', '.'))
        self.close()

    def cancel_clicked(self):
        self.retval = False
        self.close()




