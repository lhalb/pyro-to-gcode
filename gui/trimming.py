from PyQt5 import QtWidgets
from gui import trimgui as tg


class TrimDialog(tg.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, trimdata):
        super(TrimDialog, self).__init__()
        self.setupUi(self)

        self.td = trimdata

        # Init Data-Plot
        self.pw = self.plotwidget.canvas
        self.data_ax1 = self.pw.fig.add_subplot(111)
        self.vs_left = self.data_ax1.axvline(c='b')
        self.vs_right = self.data_ax1.axvline(x=1, c='r')

        self.init_plot()

        self.init_slider()
        self.setup_slots()

    def setup_slots(self):
        self.slider_left.valueChanged.connect(self.update_left_vline)
        self.slider_right.valueChanged.connect(self.update_right_vline)

    def init_slider(self):
        sli_1 = self.slider_left
        sli_2 = self.slider_right

        x_min = self.td['Zeit'].min()
        x_max = self.td['Zeit'].max()

        x_med = int((x_max - x_min)/2)

        sli_1.setMinimum(x_min)
        if not sli_2.isVisible():
            sli_1.setMaximum(x_max)
        else:
            sli_1.setMaximum(x_med - 1)

        if not sli_1.isVisible():
            sli_2.setMinimum(x_min)
        else:
            sli_2.setMinimum(x_med + 1)

        sli_2.setMaximum(x_max)

        sli_1.setValue(x_min)
        sli_2.setValue(x_max)

        self.update_left_vline()
        self.update_right_vline()

    def update_left_vline(self):
        val = self.slider_left.value()
        self.vs_left.set_xdata(val)
        print(val)

    def update_right_vline(self):
        val = self.slider_right.value()
        self.vs_right.set_xdata(val)
        print(val)

    def init_plot(self):
        ax1 = self.data_ax1
        td = self.td

        x = td['Zeit'] * 10e-9
        y11 = td['Temperatur']
        y12 = td['Sollwert']

        ax1.plot(x, y11, 'r-', label=y11.name)
        ax1.plot(x, y12, 'k-', label=y12.name)
        ax1.set_xlim([x.min(), x.max()])

        lines, labels = ax1.get_legend_handles_labels()

        ax2 = ax1.twinx()

        y2 = td['P-Ausgabe']

        ax2.plot(x, y2, label=y2.name)

        lines2, labels2 = ax2.get_legend_handles_labels()

        ax2.legend(lines + lines2, labels + labels2, loc=0)

        self.pw.fig.tight_layout()
        self.pw.draw_idle()
