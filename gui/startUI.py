from PyQt5 import QtWidgets
import gui.mainUI as mUI
import gui.boxes as box

from lib import libdata as ld
from gui.trimming import TrimDialog as Td


class MyApp(mUI.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.df = None
        self.setup_trigger()

    def setup_trigger(self):
        self.but_trim.clicked.connect(self.open_trimming)
        self.but_openFile.clicked.connect(self.open_file)

    def open_trimming(self):
        tdia = Td()
        tdia.exec_()

    def open_file(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Gib den Pfad zur Datei an', "", "csv(*.csv)")[0]
        # Falls keine Datei angegeben
        if not path:
            return

        self.import_data(path)

    def import_data(self, p):
        try:
            data = ld.import_data(p)
            data['Zeit'] = ld.reset_timescale(data['Zeit'])
            self.set_current_data(data)
        except ValueError as E:
            args = E.args
            box.show_error_box(f'{args[0]}')
            return

    def clear_data(self):
        self.df = None
        self.check_data()

    def set_current_data(self, d):
        self.df = d
        self.check_data()

    def check_data(self):
        if self.df is not None:
            self.but_status_import.setText('Geladen')
        else:
            self.but_status_import.setText('leer')






