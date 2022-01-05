from PyQt5 import QtGui, QtWidgets
import gui.mainUI as mUI
import gui.boxes as box

from lib import libdata as ld
from lib import libhelperfunctions as hf
from lib.cncimport import evaluate_pb_expression, gcode_to_values, detect_offset
from lib import errors as err
from gui.errordialog import ErrorDialogue as Ed
from gui.trimming import TrimDialog as Td
from gui.cncimporting import CncImportDialogue as Cd


class MyApp(mUI.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.df = None
        self.trimmed = None
        self.cnc_data = None

        # Init Data-Plot
        self.pw = self.plotwidget.canvas
        self.data_ax1 = self.pw.fig.add_subplot(111)
        self.data_ax2 = self.data_ax1.twinx()

        self.setup_trigger()
        self.check_data()



    def setup_trigger(self):
        # self.but_trim.clicked.connect(self.open_trimming)
        self.but_openFile.clicked.connect(self.import_data)
        self.but_import_gcode.clicked.connect(self.open_cnc_import)
        self.but_cnc_apply.clicked.connect(self.make_cnc_data_from_parameters)
        self.tabWidget.currentChanged.connect(self.toggle_tab)
        self.but_trim_apply.clicked.connect(self.trim_data)
        self.but_trim_undo.clicked.connect(self.delete_trim)

    def open_file(self, files: str):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Gib den Pfad zur Datei an', "", f'{files}')[0]
        # Falls keine Datei angegeben
        if not path:
            return False
        else:
            return path

    def open_cnc_import(self):
        path = self.open_file(files='MPF(*.MPF)')
        if not path:
            return
        ang = float(self.sb_cnc_ang.text().replace(',', '.'))
        part = 'NP-2' if self.cb_cnc_np.isChecked() else 'NP-1'
        axis = self.cb_leading_axis.currentText()
        cd = Cd(path=path, leading_axis=axis, angle=ang, part=part)
        cd.exec_()
        if not cd.cleared_parameters:
            box.show_info_box('Import failed.')
            return

        box.show_info_box('Data succesfully imported.')
        data = cd.cleared_parameters
        tab = self.tab_cnc_cont
        hf.dict_to_table(d=data, table=tab)
        tab.setHorizontalHeaderLabels(data.keys())

        if 'sq' in data.keys():
            # Text aus SQ-Spalte in Zahlen umwandeln
            sq = [evaluate_pb_expression(s) for s in data['sq'] if s]
            # den Maximalwert als SQ_0 setzen
            self.para_cnc_i0.setText(str(max(sq)))

    def import_data(self):
        path = self.open_file(files='csv(*.csv)')
        if not path:
            return
        try:
            data = ld.import_data(path)
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

    def make_cnc_data_from_parameters(self):
        corrected_values = hf.table_to_dict(self.tab_cnc_cont)
        increment = float(self.sb_cnc_ang.text().replace(',', '.'))
        force_calc = False
        axis = self.cb_leading_axis.currentText().lower()
        lead_offset = detect_offset(corrected_values, axis)

        while True:
            try:
                gcode = gcode_to_values(corrected_values,
                                        lead_axis=axis,
                                        inc=increment,
                                        offset=lead_offset,
                                        force_fill=force_calc
                                        )
                break
            except err.ValueTooLargeError as E:
                ed = Ed(increment, f'{E.args[0]}\nProvide an new Increment.', critical=True)
                ed.exec_()
                new_inc = ed.ang
                increment = new_inc
            except (err.ValueNearlyTooLargeError, err.ValueTooSmallError) as E:
                force_calc = False
                ed = Ed(increment, f'{E.args[0]}\nContinue anyway?.', critical=True)
                ed.exec_()
                response = ed.retval
                if response:
                    force_calc = True
                else:
                    new_inc = ed.ang
                    increment = new_inc

        self.cnc_data = gcode
        self.check_data()

    def toggle_tab(self, i):
        tab = self.tabWidget
        # Close
        if i == 5:
            h = 25
        # Trimming
        elif i == 0:
            h = 125
        # Filter
        elif i == 1:
            h = 200
        # Export
        elif i == 3:
            h = 80
        else:
            h = 16777215

        tab.setMaximumHeight(h)
        self.resize(self.minimumSizeHint())

    def trim_data(self):
        threshold = float(self.txt_trim_cut.text().replace(',', '.'))
        if self.trimmed is not None:
            d = self.trimmed
        else:
            d = self.df
        td = d[d['Sollwert'] > threshold]
        first = td.first_valid_index()
        last = td.last_valid_index()
        try:
            left = int(self.txt_trim_start.text().replace(',', '.'))
            td = td.iloc[left:]
        except ValueError:
            pass
        try:
            right = int(self.txt_trim_end.text().replace(',', '.'))
            td = td.iloc[:-right]
        except ValueError:
            pass

        self.trimmed = td
        self.check_data()

    def delete_trim(self):
        self.trimmed = None
        self.check_data()

    def check_data(self):
        ico_on = QtGui.QIcon(":/img/green.png")
        ico_off = QtGui.QIcon(":/img/red.png")
        tab = self.tabWidget
        if self.df is not None:
            if not hasattr(self.df, 'Sollwert'):
                box.show_error_box('Keine Sollwertdaten vorhanden.\nDatei prüfen!')
                return
            #
            # Hier müsste das Label für die Geladenen Daten eingefügt werden
            #

            for idx in range(5):
                tab.setTabEnabled(idx, True)

            if self.trimmed is not None:
                tab.setTabIcon(0, ico_on)
            else:
                tab.setTabIcon(0, ico_off)

            if hasattr(self.df, 'Gefiltert'):
                tab.setTabIcon(1, ico_on)
            else:
                tab.setTabIcon(1, ico_off)
        else:
            for idx in range(5):
                tab.setTabEnabled(idx, False)
                if idx not in [3, 4]:
                    tab.setTabIcon(idx, ico_off)

        if self.cnc_data:
            tab.setTabIcon(2, ico_on)
        else:
            tab.setTabIcon(2, ico_off)

        if self.df is not None:
            self.plot_data()

    def plot_data(self, ib=None, cnc=None, filt=None):
        self.data_ax1.clear()
        self.data_ax2.clear()

        ax = self.data_ax1
        ax2 = self.data_ax2
        if self.trimmed is not None:
            d = self.trimmed
        else:
            d = self.df

        x = d['Zeit'] * 10e-9
        y11 = d['Temperatur']
        y12 = d['Sollwert']

        ax.plot(x, y11, 'r-', label=y11.name)
        ax.plot(x, y12, 'k-', label=y12.name)

        lines, labels = ax.get_legend_handles_labels()

        y21 = d['P-Ausgabe']

        if not ib:
            ax2.plot(x, y21, label=y21.name)
        else:
            ax2.plot(x, ib, label=ib.name)

        lines2, labels2 = ax2.get_legend_handles_labels()

        ax2.legend(lines + lines2, labels + labels2, loc=0)

        self.pw.fig.tight_layout()
        self.pw.draw_idle()



