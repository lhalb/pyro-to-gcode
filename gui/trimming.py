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

        self.cid = self.pw.mpl_connect('button_release_event', self.onclick)

        self.init_plot()

        self.init_slider()
        self.setup_slots()

    def setup_slots(self):
        self.slider_left.valueChanged.connect(self.update_left_vline)
        self.slider_right.valueChanged.connect(self.update_right_vline)
        self.but_trim_right.clicked.connect(self.hide_left)
        self.but_trim_left.clicked.connect(self.hide_rigth)

    def hide_left(self):
        self.slider_left.hide()
        self.lab_left.hide()
        self.but_trim_right.hide()
        self.slider_right.show()
        self.lab_right.show()
        self.but_trim_right.show()

    def hide_rigth(self):
        self.slider_left.show()
        self.lab_left.show()
        self.but_trim_right.show()
        self.slider_right.hide()
        self.lab_right.hide()
        self.but_trim_right.hide()

    def init_slider(self):
        sli_1 = self.slider_left
        sli_2 = self.slider_right

        x_min = int(self.td['Zeit'].min())
        x_max = int(self.td['Zeit'].max())

        x_med = int((x_max - x_min)/2)

        sli_1.setMinimum(x_min)
        if sli_2.isVisible():
            sli_1.setMaximum(x_med - 1)
        else:
            sli_1.setMaximum(x_max)

        if sli_1.isVisible():
            sli_2.setMinimum(x_med + 1)
        else:
            sli_2.setMinimum(x_min)

        sli_2.setMaximum(x_max)

        sli_1.setValue(x_min)
        sli_2.setValue(x_max)

        sli_1.setTickInterval(1)
        sli_2.setTickInterval(1)

        self.update_left_vline()
        self.update_right_vline()


    def onclick(self, event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))

    def update_left_vline(self):
        val = self.slider_left.value()
        self.lab_left.setText(str(val))
        self.vs_left.set_xdata(val * 1e-9)
        self.pw.draw_idle()

    def update_right_vline(self):
        val = self.slider_right.value()
        self.lab_right.setText(str(val))
        self.vs_right.set_xdata(val * 1e-9)
        self.pw.draw_idle()

    def init_plot(self):
        ax1 = self.data_ax1
        td = self.td

        x = td['Zeit'] * 1e-9
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
