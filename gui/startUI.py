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
        self.check_data()

    def setup_trigger(self):
        # self.but_trim.clicked.connect(self.open_trimming)
        self.but_openFile.clicked.connect(self.open_file)

    def open_trimming(self):
        data = self.df
        tdia = Td(data)
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
        return
        buttons = [self.but_cnc, self.but_gCode, self.but_filter, self.but_trim, self.but_plot,
                   self.but_statusTrim, self.but_statusCNC, self.but_statuFilter]
        if self.df is not None:
            if not hasattr(self.df, 'Sollwert'):
                box.show_error_box('Keine Sollwertdaten vorhanden.\nDatei prüfen!')
                return

            self.but_status_import.setText('Geladen')

            for but in buttons:
                but.show()
                # but.setEnabled(True)
            self.resize(self.minimumSizeHint())

            if hasattr(self.df, 'Gefiltert'):
                self.but_statusTrim.setText('Gefiltert')
            else:
                self.but_statusTrim.setText('Ungefiltert')
        else:
            self.but_status_import.setText('leer')
            for but in buttons:
                but.hide()
                # but.setEnabled(False)
            self.resize(self.minimumSizeHint())







