from PyQt5 import QtWidgets
from gui import cncimportUI as cUI
from gui.errordialog import ErrorDialogue as ED
from lib import cncimport as cnc
from lib import libhelperfunctions as hf
from gui import boxes as box


class CncImportDialogue(cUI.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, path: str, leading_axis: str, angle: float, part: str):
        super(CncImportDialogue, self).__init__()

        self.fname = path
        self.inc = angle
        self.la = leading_axis
        self.np = part

        self.raw = None
        self.cleared_cnc = None
        self.strt = None
        self.c_strt = None
        self.raw_parameters = None
        self.cleared_parameters = None

        self.setupUi(self)
        self.setup_buttons()

        self.tab_para.hide()

        self.display_raw()

    def setup_buttons(self):
        self.but_accept.clicked.connect(self.ok_clicked)
        self.but_back_close.clicked.connect(self.close_clicked)

    def ok_clicked(self):
        # Wenn noch gar nichts erstellt wurde
        if not any([self.raw, self.cleared_cnc, self.raw_parameters]):
            txt = self.txt_cnc.toPlainText()
            if not txt:
                box.show_error_box('No Data available.\nTry to reload the data.')
                self.close()
            self.raw = txt
            self.display_cleared_cnc()
            return
        # Wenn es Rohdaten gibt
        elif self.raw and not any([self.cleared_cnc, self.raw_parameters]):
            self.cleared_cnc = self.txt_cnc.toPlainText().splitlines()
            self.txt_cnc.hide()
            self.tab_para.show()
            self.display_parameters()
        elif self.cleared_cnc and not self.raw_parameters:
            self.raw_parameters = hf.table_to_dict(table=self.tab_para)
            self.resolve_variables()
        else:
            self.cleared_parameters = hf.table_to_dict(self.tab_para)
            self.close()

    def close_clicked(self):
        # Wenn noch gar nichts erstellt wurde
        if not any([self.raw, self.cleared_cnc,
                    self.raw_parameters, self.cleared_parameters]):
            self.close()

        # Wenn es Rohdaten gibt
        elif self.raw and not any([self.cleared_cnc, self.raw_parameters, self.cleared_parameters]):
            self.raw = None
            self.display_raw()

        elif self.cleared_cnc and not any([self.raw_parameters, self.cleared_parameters]):
            self.cleared_cnc = None
            self.c_strt = None
            self.strt = None
            self.tab_para.hide()
            self.txt_cnc.show()
            self.display_cleared_cnc()

        else:
            self.raw_parameters = None
            self.display_parameters()

    def display_raw(self):
        self.info_txt.setText('Rawdata of G-Code. Continue with cleaning?')
        self.but_accept.setText('Continue')
        self.but_back_close.setText('Close')

        try:
            raw_data = cnc.import_cnc(self.fname)
        except FileNotFoundError as E:
            box.show_error_box(f'{E.args[0]}')
            return
        self.txt_cnc.setPlainText(raw_data)

    def display_cleared_cnc(self):
        self.info_txt.setText('All cleared up. Continue with parameter search?')
        self.but_accept.setText('Continue')
        self.but_back_close.setText('Undo')
        cleared = cnc.clear_code(self.raw)
        txt_cleared = '\n'.join(cleared)
        self.txt_cnc.setPlainText(txt_cleared)

    def display_parameters(self):
        self.info_txt.setText('These parameters were found. Continue with the replacement of variables?')
        self.but_accept.setText('Continue')
        self.but_back_close.setText('Undo')

        code = self.cleared_cnc

        self.strt, end = cnc.find_desired_section(code)
        ebh_cnc = code[self.strt:end]

        self.c_strt, c_end = cnc.find_desired_section(ebh_cnc, start_string='PYR_STRT'.lower(), end_string=['PYR_STOP'.lower()])

        contour_cnc = code[self.strt + self.c_strt:self.strt + c_end]
        contour_mode = cnc.get_parameter_mode(contour_cnc)

        contour_parameters = cnc.get_parameters(contour_cnc, mode=contour_mode, n_p=self.np)

        hf.dict_to_table(d=contour_parameters, table=self.tab_para)

    def resolve_variables(self):
        self.info_txt.setText('I found those replacements. Finish import?')
        self.but_accept.setText('Finish')
        self.but_back_close.setText('Undo')

        code = self.cleared_cnc
        contour_parameters = self.raw_parameters
        strt = self.strt
        c_strt = self.c_strt
        n_p = self.np

        par_cnc = code[strt:strt + c_strt]
        par_mode = cnc.get_parameter_mode(par_cnc)

        unknown_vars = cnc.get_unknown_vars(contour_parameters.values())

        values = cnc.get_values_from_parameters(code, unknown_vars,
                                                p_start=strt, p_end=strt + c_strt, mode=par_mode, n_p=n_p)

        corrected_values = cnc.replace_missing_values(contour_parameters, values)

        hf.dict_to_table(corrected_values, self.tab_para)

