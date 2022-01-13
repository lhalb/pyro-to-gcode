from PyQt5 import QtGui, QtWidgets
import gui.mainUI as mUI
import gui.boxes as box

from lib import libdata as ld
from lib import libhelperfunctions as hf
from lib.cncimport import import_cnc, get_value, clear_code, evaluate_pb_expression, gcode_to_values, detect_offset
from lib import errors as err
from gui.errordialog import ErrorDialogue as Ed
from gui.cncimporting import CncImportDialogue as Cd

import pandas as pd

class MyApp(mUI.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # aenderungen an der GUI
        self.tabWidget.setMaximumHeight(25)

        self.df = None
        self.trimmed = None
        self.filtered = None
        self.cnc_data = None

        # Init Data-Plot
        self.pw = self.plotwidget.canvas
        self.data_ax1 = self.pw.fig.add_subplot(111)
        self.data_ax2 = self.data_ax1.twinx()
        self.fline, = self.data_ax2.plot([], [])

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
        self.but_import_par.clicked.connect(self.import_pyr_par)
        self.but_trim_undo.clicked.connect(self.delete_trim)
        self.para_filt_sav_n.valueChanged.connect(lambda: self.update_filter(False))
        self.para_filt_med_n.valueChanged.connect(lambda: self.update_filter(False))
        self.para_filt_sav_delta.valueChanged.connect(lambda: self.update_filter(False))
        self.para_filt_sav_deriv.valueChanged.connect(lambda: self.update_filter(False))
        self.para_filt_sav_poly.valueChanged.connect(lambda: self.update_filter(False))
        self.para_filt_sav_mode.currentTextChanged.connect(lambda: self.update_filter(False))
        self.tb_filt.currentChanged.connect(self.init_vals)
        self.txt_para_filt_sav_n.returnPressed.connect(lambda: self.update_filter(False))
        self.para_filt_med_n.valueChanged.connect(lambda: self.update_filter(False))
        self.txt_para_filt_med_n.returnPressed.connect(lambda: self.update_filter(False))
        self.para_filt_rol_n.valueChanged.connect(lambda: self.update_filter(False))
        self.txt_para_filt_rol_n.returnPressed.connect(lambda: self.update_filter(False))
        self.but_filt_apply.clicked.connect(lambda: self.update_filter(True))
        self.but_export_xlsx_all.clicked.connect(lambda: self.export_xls('all'))
        self.but_export_xlsx_raw.clicked.connect(lambda: self.export_xls('raw'))
        self.but_export_xlsx_trimmed.clicked.connect(lambda: self.export_xls('trimmed'))
        self.but_export_xlsx_filtered.clicked.connect(lambda: self.export_xls('filtered'))
        self.but_export_xlsx_cnc.clicked.connect(lambda: self.export_xls('cnc'))
        self.but_gCode.clicked.connect(self.export_gcdoe)

    def export_gcode(self):
        if self.cnc_data is not None:
            dat = self.cnc_data
        else:
            return
        lead_ax = self.cb_leading_axis.currentText()

        fname = self.save_file("SPF Files (*.SPF)")
        if not fname:
            return

        ld.export_data_to_gcode(fname, dat, lead_ax)



    def export_xls(self, data='raw'):
        fname = self.save_file("Excel Files (*.xlsx)")
        if not fname:
            return

        if data == 'raw':
            exp_data = [self.df]
            names = [data]
        elif data == 'trimmed':
            exp_data = [self.trimmed]
            names = [data]
        elif data == 'filtered':
            exp_data = [self.filtered]
            names = [data]
        elif data == 'cnc':
            exp_data = [self.cnc_data]
            names = [data]
        else:
            names = []
            exp_data = []
            for e, n in zip([self.df, self.trimmed, self.filtered, self.cnc_data],
                            ['raw', 'trimmed', 'filtered', 'cnc']):
                if e is not None:
                    exp_data.append(e)
                    names.append(n)

        ld.export_data(fname, names, exp_data)

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

        self.but_cnc_apply.setEnabled(True)

    def import_pyr_par(self):
        path = self.open_file(files='SPF-Files (*.SPF)')
        if not path:
            return
        raw_code = import_cnc(path)
        cleared_code = clear_code(raw_code)
        code = hf.list_to_lower(cleared_code)
        result = get_value(code, '_dsq_max')
        if not result:
            box.show_info_box('Es konnte kein Parameter extrahiert werden.')
            return
        else:
            try:
                dsq = float(result)
                box.show_info_box(f'Strahlstromamplitude von {dsq} gefunden')
                self.para_cnc_di.setText(result)
            except ValueError:
                box.show_error_box(f'{result} scheint kein akzeptabler Wert zu sein.')
                return

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

    def set_current_data(self, d):
        self.df = d
        self.check_data()

    def make_cnc_data_from_parameters(self):
        testfields = [self.para_cnc_di, self.para_cnc_i0]
        for f in testfields:
            if f.text() == '':
                box.show_error_box('Fehlender Parameter')
                self.highlight_field(f)
                return
            else:
                self.reset_field(f)

        corrected_values = hf.table_to_dict(self.tab_cnc_cont)
        increment = float(self.sb_cnc_ang.text().replace(',', '.'))
        force_calc = False
        axis = self.cb_leading_axis.currentText().lower()
        lead_offset = detect_offset(corrected_values, axis)
        try:
            dsq = float(self.para_cnc_di.text())
        except ValueError:
            box.show_error_box('Falsche Strahlstromangabe')
            return

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

        cdf = hf.dict_to_dataframe(gcode)
        if self.filtered is not None:
            d = self.filtered
        elif self.trimmed is not None:
            d = self.trimmed
        else:
            d = self.df
        cdf['Zeit'] = ld.get_cnc_times(d['Zeit'], len(cdf.index))

        cdf['P-fakt'] = ld.get_corresponding_powers(source_data=d,
                                                    dest_data=cdf,
                                                    comp_col='Zeit', search_col='P-Ausgabe')
        cdf['P-Ausgabe'] = cdf['sq'] + (cdf['P-fakt'] * 0.01 * dsq)
        if lead_offset:
            cdf['P-Ausgabe'].iloc[0] = 0
        self.cnc_data = cdf
        self.check_data()
        self.but_clear_cnc.setEnabled(True)

    def trim_data(self):
        threshold = float(self.txt_trim_cut.text().replace(',', '.'))
        if self.trimmed is not None:
            d = self.trimmed
        else:
            d = self.df
        td = d[d['Sollwert'] > threshold]
        td.reset_index(drop=True, inplace=True)
        td['Zeit'] = ld.reset_timescale(td['Zeit'])
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
        self.filtered = None
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
            self.but_export_xlsx_raw.setEnabled(True)
            for idx in range(5):
                tab.setTabEnabled(idx, True)

            if self.trimmed is not None:
                tab.setTabIcon(0, ico_on)
                self.but_trim_undo.setEnabled(True)
                self.but_export_xlsx_trimmed.setEnabled(True)
            else:
                tab.setTabIcon(0, ico_off)
                self.but_trim_undo.setEnabled(False)
                self.but_export_xlsx_trimmed.setEnabled(False)

            if self.filtered is not None:
                tab.setTabIcon(1, ico_on)
                self.but_filt_undo.setEnabled(True)
                self.but_export_xlsx_filtered.setEnabled(True)
            else:
                self.but_filt_undo.setEnabled(False)
                tab.setTabIcon(1, ico_off)
                self.but_export_xlsx_filtered.setEnabled(False)
        else:
            for idx in range(5):
                tab.setTabEnabled(idx, False)
                if idx not in [3, 4]:
                    tab.setTabIcon(idx, ico_off)

        if self.cnc_data is not None:
            tab.setTabIcon(2, ico_on)
            self.but_gCode.setEnabled(True)
            self.but_clear_cnc.setEnabled(True)
            self.but_export_xlsx_cnc.setEnabled(True)
        else:
            tab.setTabIcon(2, ico_off)
            self.but_gCode.setEnabled(False)
            self.but_clear_cnc.setEnabled(False)
            self.but_export_xlsx_cnc.setEnabled(False)

        if self.df is not None:
            self.plot_data(cnc=self.cnc_data)
            if self.filtered is not None:
                self.plot_filter(self.filtered['Zeit'], self.filtered['P-Ausgabe'])
        else:
            self.data_ax1.clear()
            self.data_ax2.clear()

            self.but_export_xlsx_raw.setEnabled(False)

    def plot_data(self, ib=None, cnc=None, filt=None):
        self.data_ax1.clear()
        self.data_ax2.clear()

        ax = self.data_ax1
        ax2 = self.data_ax2
        if self.trimmed is not None:
            d = self.trimmed
        else:
            d = self.df

        x = d['Zeit']
        y11 = d['Temperatur']
        y12 = d['Sollwert']

        ax.plot(x, y11, 'r-', label=y11.name)
        ax.plot(x, y12, 'k--', label=y12.name)

        lines, labels = ax.get_legend_handles_labels()

        y21 = d['P-Ausgabe']

        if not ib:
            ax2.plot(x, y21, 'c-', label=y21.name)
        else:
            ax2.plot(x, ib, 'c-', label=ib.name, alpha=0.5)

        if cnc is not None:
            ax2.plot(cnc['Zeit'], cnc['P-Ausgabe'], 'g-', label='SQ-CNC')

        self.fline, = self.data_ax2.plot([], [], 'g-', label='Gefiltert')

        lines2, labels2 = ax2.get_legend_handles_labels()

        ax2.legend(lines + lines2, labels + labels2, loc=0)

        self.pw.fig.tight_layout()
        self.pw.draw_idle()

    # Funktionen, die Daten zurücksetzen
    def clear_data(self):
        self.df = None
        self.trimmed = None
        self.cnc_data = None
        self.filtered = None
        self.check_data()

    def delete_trim(self):
        self.trimmed = None
        self.filtered = None
        self.check_data()

    def delete_cnc(self):
        self.cnc_data = None
        self.but_clear_cnc.setEnabled(False)

    def plot_filter(self, x, y):
        self.fline.set_xdata(x)
        self.fline.set_ydata(y)
        self.pw.draw_idle()

    def update_filter(self, apply=False):
        def switch_sender(send, slider, txt):
            if send == slider:
                i = slider.value()
            else:
                i = int(txt.text())
                if i > slider.maximum():
                    i = slider.maximum()
                if i < slider.minimum():
                    i = slider.minimum()
            return i

        sender = self.sender()
        curr_tb = self.tb_filt.currentIndex()

        if self.trimmed is not None:
            data = self.trimmed
        else:
            data = self.df

        filtered = []
        # Savgol-Filter --> 0
        if curr_tb == 0:
            sli = self.para_filt_sav_n
            tex = self.txt_para_filt_sav_n
            n = switch_sender(sender, sli, tex)

            if (n % 2) == 0:
                n -= 1

            poly = self.para_filt_sav_poly.value()
            if poly > n:
                box.show_error_box('p muss kleiner n sein.')
                return
            deriv = self.para_filt_sav_deriv.value()
            delta = self.para_filt_sav_delta.value()
            mode = self.para_filt_sav_mode.currentText()
            self.txt_para_filt_sav_n.setText(str(n))
            try:
                filtered = ld.apply_savgol_filter(data['P-Ausgabe'],
                                                  window=n, polyorder=poly,
                                                  deriv=deriv, delta=delta, mode=mode)

            except ValueError:
                return
        elif curr_tb == 1:
            sli = self.para_filt_med_n
            tex = self.txt_para_filt_med_n
            n = switch_sender(sender, sli, tex)

            if (n % 2) == 0:
                n -= 1

            filtered = ld.apply_median_filter(data['P-Ausgabe'], n)

        # für gleitenden Durchschnitt
        elif curr_tb == 2:
            sli = self.para_filt_rol_n
            tex = self.txt_para_filt_rol_n

            n = switch_sender(sender, sli, tex)

            filtered = ld.apply_rolling_average(data['P-Ausgabe'], n)

        self.plot_filter(data['Zeit'], filtered)

        if sender == tex:
            sli.setValue(n)
        else:
            tex.setText(str(n))

        if apply:
            if curr_tb != 2:
                filtered = hf.to_series(filtered, 'P-Ausgabe')
            filt_df = filtered.to_frame()
            filt_df['Zeit'] = data['Zeit']
            # Wenn gleitender Durchschnitt ausgewählt wurde
            if curr_tb == 2 and self.trimmed is not None:
                answer = box.show_msg_box('Die Werte wurden bereits beschnitten. Es gehen Daten verloren. Fortfahren?')
                if answer:
                    filt_df.dropna(inplace=True)

            self.filtered = filt_df
            self.check_data()

    def delete_filtered(self):
        self.filtered = None

    def init_vals(self):
        curr_tb = self.tb_filt.currentIndex()
        if self.trimmed is not None:
            data = self.trimmed['P-Ausgabe']
        else:
            data = self.df['P-Ausgabe']

        # maximale Glättung erfasst 1/10 der Messwerte
        max_win = hf.round_to_odd(len(data.index)/10)
        max_val = data.max()

        # Savgol-Filter --> 0
        if curr_tb == 0:
            sli = self.para_filt_sav_n
            max_val = max_win
            min_val = 3
            txt = self.txt_para_filt_sav_n

            poly = self.para_filt_sav_poly
            poly.setMinimum(1)
            poly.setMaximum(max_win)

            der = self.para_filt_sav_deriv
            der.setMinimum(0)
            der.setMaximum(10)

            delt = self.para_filt_sav_delta
            delt.setMinimum(1.0)
            # Delta kann maximal 1/10 des Maximums sein
            delt.setMaximum(max_val / 10)
        if curr_tb == 1:
            sli = self.para_filt_med_n
            txt = self.txt_para_filt_med_n
            max_val = max_win
            min_val = 3

        if curr_tb == 2:
            sli = self.para_filt_rol_n
            txt = self.txt_para_filt_rol_n
            max_val = max_win
            min_val = 1

        sli.setMinimum(min_val)
        sli.setMaximum(max_val)
        sli.setValue(min_val)
        sli.setPageStep(1)
        sli.setSingleStep(1)
        txt.setText(str(min_val))

        self.update_filter()

        return

    # Hilfsfunktionen
    def open_file(self, files: str):
        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Gib den Pfad zur Datei an', "", f'{files}')[0]
        # Falls keine Datei angegeben
        if not path:
            return False
        else:
            return path

    def save_file(self, files: str):
        path = QtWidgets.QFileDialog.getSaveFileName(self, 'Gib einen Dateinamen an', "", f'{files}')[0]
        if not path:
            return False
        else:
            return path

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
            self.init_vals()
            h = 230
        # Export
        elif i == 3:
            h = 180
        else:
            h = 16777215

        tab.setMaximumHeight(h)
        self.resize(self.minimumSizeHint())

    def highlight_field(self, f):
        f.setStyleSheet('border: 2px solid red;')

    def reset_field(self, f):
        f.setStyleSheet('border: 1px solid black')
