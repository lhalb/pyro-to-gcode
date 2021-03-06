from PyQt5 import QtGui, QtWidgets, QtCore
import gui.mainUI as mUI
import gui.boxes as box

from lib import libdata as ld
from lib import libhelperfunctions as hf
from lib.cncimport import import_cnc, get_value, clear_code, gcode_to_values, detect_offset, get_available_axis
from lib import errors as err
from gui.errordialog import ErrorDialogue as Ed
from gui.cncimporting import CncImportDialogue as Cd
from gui.axisPicker import AxisPicker as aP


class MyApp(mUI.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        icon = QtGui.QIcon(":/img/appicon.png")
        self.setWindowIcon(icon)

        # aenderungen an der GUI
        self.tabWidget.setMaximumHeight(25)

        self.df = None
        self.trimmed = None
        self.filtered = None
        self.cnc_data = None
        self.path = None

        # Init Data-Plot
        self.pw = self.plotwidget.canvas
        self.tb = self.plotwidget.toolbar
        self.data_ax1 = self.pw.fig.add_subplot(111)
        self.data_ax2 = self.data_ax1.twinx()
        # self.data_ax1.clear()
        # self.data_ax2.clear()
        self.fline, = self.data_ax2.plot([], [])

        self.psize_h = self.plotwidget.frameGeometry().height()

        self.hide_plotwidget()

        self.move_up = QtWidgets.QAction("Move_Up", self)
        self.move_down = QtWidgets.QAction("Move_Down", self)

        self.start_size = QtCore.QSize(self.width(), self.height())

        self.setup_trigger()
        self.check_data()

    def setup_trigger(self):
        self.but_openFile.clicked.connect(self.import_data)
        self.but_import_gcode.clicked.connect(self.open_cnc_import)
        self.but_cnc_apply.clicked.connect(self.make_cnc_data_from_parameters)
        self.tabWidget.currentChanged.connect(self.toggle_tab)
        self.but_trim_apply.clicked.connect(self.trim_data)
        self.but_trim_undo.clicked.connect(self.delete_trim)
        self.but_import_par.clicked.connect(self.import_pyr_par)
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
        self.but_export_xlsx_all.clicked.connect(self.export_xls)
        self.but_gCode.clicked.connect(self.export_gcode)
        self.but_delete_data.clicked.connect(self.clear_data)
        self.actionOpen.triggered.connect(self.import_data)
        self.but_clear_cnc.clicked.connect(self.delete_cnc)
        self.but_filt_undo.clicked.connect(self.delete_filter)

        # Tabelle
        self.but_tab_row_add.clicked.connect(self.add_row)
        self.but_tab_row_del.clicked.connect(self.delete_row)
        self.but_tab_col_add.clicked.connect(self.add_col)
        self.but_tab_col_del.clicked.connect(self.delete_col)
        self.but_tab_row_up.clicked.connect(lambda: self.move_items('UP'))
        self.but_tab_row_dwn.clicked.connect(lambda: self.move_items('DOWN'))
        self.but_tab_col_left.clicked.connect(lambda: self.move_items('LEFT'))
        self.but_tab_col_right.clicked.connect(lambda: self.move_items('RIGHT'))

    def export_gcode(self):
        if self.cnc_data is not None:
            dat = self.cnc_data
        else:
            return
        lead_ax = self.cb_leading_axis.currentText()

        fname = self.save_file("SPF Files (*.SPF)")
        if not fname:
            return

        dat['sq'] = dat['P-Ausgabe']
        dat.drop(['Zeit', 'P-fakt', 'P-Ausgabe'], axis=1, inplace=True)

        g_code = ld.export_data_to_gcode(dat, lead_ax)

        #
        # den Gcode kann man sich jetzt hier nochmal anzeigen lassen
        #
        ld.save_gcode(fname, g_code)
        box.show_info_box(f'Daten erfolgreich unter\n{fname}\nexportiert.')

    def export_xls(self):
        fname = self.save_file("Excel Files (*.xlsx)")
        if not fname:
            return

        names = []
        exp_data = []
        for e, n in zip([self.df, self.trimmed, self.filtered, self.cnc_data],
                        ['raw', 'trimmed', 'filtered', 'cnc']):
            if e is not None:
                exp_data.append(e)
                names.append(n)

        ld.export_data(fname, names, exp_data)

        box.show_info_box(f'Daten erfolgreich unter\n{fname}\nexportiert.')

    def open_cnc_import(self):
        path = self.open_file(files='MPF(*.MPF)')
        if not path:
            return
        ang = float(self.sb_cnc_ang.text().replace(',', '.'))
        # part = 'NP-2' if self.cb_cnc_np.isChecked() else 'NP-1'
        axis = self.cb_leading_axis.currentText()
        cd = Cd(path=path)
        cd.exec_()
        if not cd.cleared_parameters:
            box.show_info_box('Import failed.')
            return

        box.show_info_box('Data succesfully imported.')
        data = cd.cleared_parameters
        tab = self.tab_cnc_cont
        hf.dict_to_table(d=data, table=tab)
        tab.setHorizontalHeaderLabels(data.keys())

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
        if self.df is not None:
            self.clear_data()

        try:
            data = ld.import_data(path)
            data['Zeit'] = ld.reset_timescale(data['Zeit'])
            self.path = hf.basename(path)
            self.show_plotwidget()
            self.set_current_data(data)
        except ValueError as E:
            args = E.args
            box.show_error_box(f'{args[0]}')
            return

    def set_current_data(self, d):
        self.df = d
        self.check_data()

    def make_cnc_data_from_parameters(self):
        if self.para_cnc_di.text() == '':
            box.show_error_box('Fehlender Parameter')
            self.highlight_field(self.para_cnc_di)
            return
        else:
            self.reset_field(self.para_cnc_di)

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
            except AttributeError as E:
                box.show_error_box(E.args[0])
                return


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

    def plot_data(self, ib=None, cnc=None):
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

        ax.set_xlabel('Zeit [s]')
        ax.set_ylabel('Temperatur [??C]')

        lines, labels = ax.get_legend_handles_labels()

        y21 = d['P-Ausgabe']

        if not ib:
            ax2.plot(x, y21, 'c-', label=y21.name)
            y2_string = 'P-Wert [%]'
        else:
            ax2.plot(x, ib, 'c-', label=ib.name, alpha=0.5)
            y2_string = 'Strahlstrom [mA]'

        if cnc is not None:
            ax2.plot(cnc['Zeit'], cnc['P-Ausgabe'], 'm-', label='SQ-CNC')
            if 'Strahlstrom' not in y2_string:
                y2_string += ' | Strahlstrom [mA]'

        self.fline, = self.data_ax2.plot([], [], 'g-', label='Gefiltert')
        ax2.set_ylabel(y2_string)
        lines2, labels2 = ax2.get_legend_handles_labels()

        ax2.legend(lines + lines2, labels + labels2, loc=0)

        self.pw.fig.tight_layout()
        self.pw.draw_idle()

    # Funktionen, die Daten zur??cksetzen
    def clear_data(self):
        self.df = None
        self.trimmed = None
        self.cnc_data = None
        self.filtered = None
        empty_table = {'a': ''}
        hf.dict_to_table(empty_table, self.tab_cnc_cont)
        self.hide_plotwidget()
        self.check_data()

    def delete_trim(self):
        self.trimmed = None
        self.filtered = None
        self.check_data()

    def delete_filter(self):
        self.filtered = None
        self.init_vals()
        self.check_data()

    def delete_cnc(self):
        self.cnc_data = None
        self.but_clear_cnc.setEnabled(False)
        self.check_data()

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

        # f??r gleitenden Durchschnitt
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
            # Wenn gleitender Durchschnitt ausgew??hlt wurde
            if curr_tb == 2 and self.trimmed is not None:
                answer = box.show_msg_box('Die Werte wurden bereits beschnitten. Es gehen Daten verloren. Fortfahren?')
                if answer:
                    filt_df.dropna(inplace=True)

            self.filtered = filt_df
            self.check_data()

    def init_vals(self):
        curr_tb = self.tb_filt.currentIndex()
        if self.trimmed is not None:
            data = self.trimmed['P-Ausgabe']
        else:
            if self.df is not None:
                data = self.df['P-Ausgabe']
            else:
                return

        # maximale Gl??ttung erfasst 1/10 der Messwerte
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

    def add_row(self):
        tab = self.tab_cnc_cont
        rows = tab.rowCount()
        tab.insertRow(rows)

    def delete_row(self):
        tab = self.tab_cnc_cont
        curr_row = tab.currentRow()
        tab.removeRow(curr_row)

    def move_items(self, direction='UP'):
        if direction not in ('UP', 'DOWN', 'LEFT', 'RIGHT'):
            return

        tab = self.tab_cnc_cont
        row = tab.currentRow()
        col = tab.currentColumn()

        if direction in ('UP', 'DOWN'):
            if direction == 'UP':
                before = -1
                after = 1
                test = row > 0
            else:
                before = 2
                after = 0
                test = row < tab.rowCount()-1
            if not test:
                return
            tab.insertRow(row + before)
            for i in range(tab.columnCount()):
                tab.setItem(row + before, i, tab.takeItem(row + after, i))
                tab.setCurrentCell(row + before, col)
            tab.removeRow(row + after)

        if direction in ('LEFT', 'RIGHT'):
            if direction == 'LEFT':
                before = -1
                after = 1
                test = col > 0
            else:
                before = 2
                after = 0
                test = col < tab.columnCount() - 1
            if not test:
                return
            tab.insertColumn(col + before)
            for i in range(tab.rowCount()):
                tab.setItem(i, col + before, tab.takeItem(i, col + after))
                tab.setCurrentCell(row, col + before)
            tab.removeColumn(col + after)

    def add_col(self):
        tab = self.tab_cnc_cont
        curr_ax = [tab.horizontalHeaderItem(i).text() for i in range(tab.columnCount())]
        avail_ax = get_available_axis(curr_ax)
        if not avail_ax:
            return
        axpick = aP(avail_ax)
        ret = axpick.exec_()
        if not ret:
            return

        new_ax = axpick.cb_axis.currentText()
        hf.insert_column(tab, new_ax)

    def delete_col(self):
        tab = self.tab_cnc_cont
        curr_col = tab.currentColumn()
        tab.removeColumn(curr_col)

    def toggle_tab(self, i):
        tab = self.tabWidget
        reset = False
        # Close
        if i == 5:
            reset = True
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
            h = 100
        elif i == 4:
            h = 300
        else:
            h = 16777215

        tab.setMaximumHeight(h)
        if reset:
            self.show_plotwidget()

    def hide_plotwidget(self):
        self.plotwidget.setMaximumHeight(0)
        self.plotwidget.hide()
        self.resize(self.minimumSizeHint())

    def show_plotwidget(self):
        self.plotwidget.show()
        # self.resize(self.minimumSizeHint())
        self.plotwidget.setMaximumHeight(self.psize_h)
        self.resize(self.minimumSizeHint())
        self.plotwidget.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                                    QtWidgets.QSizePolicy.Expanding))
        self.plotwidget.setMaximumHeight(1600000)

    def highlight_field(self, f):
        f.setStyleSheet('border: 2px solid red;')

    def reset_field(self, f):
        f.setStyleSheet('border: 1px solid black')

    def set_current_filelabel(self, p):
        if p:
            text = f'Loaded file: {p}'
        else:
            text = 'no file loaded. Press STRG + O or click \"input\"'
        self.lab_loaded_file.setText(text)

    def check_data(self):
        ico_on = QtGui.QIcon(":/img/green.png")
        ico_off = QtGui.QIcon(":/img/red.png")
        tab = self.tabWidget

        if self.df is not None:
            if not hasattr(self.df, 'Sollwert'):
                box.show_error_box('Keine Sollwertdaten vorhanden.\nDatei pr??fen!')
                return
            self.but_delete_data.setEnabled(True)
            for idx in range(5):
                tab.setTabEnabled(idx, True)

            if self.trimmed is not None:
                tab.setTabIcon(0, ico_on)
                self.but_trim_undo.setEnabled(True)
            else:
                tab.setTabIcon(0, ico_off)
                self.but_trim_undo.setEnabled(False)

            if self.filtered is not None:
                tab.setTabIcon(1, ico_on)
                self.but_filt_undo.setEnabled(True)
            else:
                self.but_filt_undo.setEnabled(False)
                tab.setTabIcon(1, ico_off)
        else:
            for idx in range(5):
                tab.setTabEnabled(idx, False)
                if idx not in [3, 4]:
                    tab.setTabIcon(idx, ico_off)

        if self.cnc_data is not None:
            tab.setTabIcon(2, ico_on)
            self.but_gCode.setEnabled(True)
            self.but_clear_cnc.setEnabled(True)
        else:
            tab.setTabIcon(2, ico_off)
            self.but_gCode.setEnabled(False)
            self.but_clear_cnc.setEnabled(False)

        if self.df is not None:
            if self.cnc_data is not None:
                self.plot_data(cnc=self.cnc_data)
            else:
                self.plot_data()
            if self.filtered is not None:
                self.plot_filter(self.filtered['Zeit'], self.filtered['P-Ausgabe'])
        else:
            self.path = None
            self.data_ax1.clear()
            self.data_ax2.clear()
            self.pw.draw_idle()
            self.but_delete_data.setEnabled(False)

        self.set_current_filelabel(self.path)
