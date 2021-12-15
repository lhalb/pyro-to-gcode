# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './gui/mainUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(176, 229)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.but_openFile = QtWidgets.QPushButton(self.centralwidget)
        self.but_openFile.setObjectName("but_openFile")
        self.gridLayout.addWidget(self.but_openFile, 0, 0, 1, 1)
        self.but_cnc = QtWidgets.QPushButton(self.centralwidget)
        self.but_cnc.setObjectName("but_cnc")
        self.gridLayout.addWidget(self.but_cnc, 3, 0, 1, 1)
        self.but_filter = QtWidgets.QPushButton(self.centralwidget)
        self.but_filter.setObjectName("but_filter")
        self.gridLayout.addWidget(self.but_filter, 2, 0, 1, 1)
        self.but_gCode = QtWidgets.QPushButton(self.centralwidget)
        self.but_gCode.setObjectName("but_gCode")
        self.gridLayout.addWidget(self.but_gCode, 5, 0, 1, 2)
        self.but_status_import = QtWidgets.QPushButton(self.centralwidget)
        self.but_status_import.setObjectName("but_status_import")
        self.gridLayout.addWidget(self.but_status_import, 0, 1, 1, 1)
        self.but_trim = QtWidgets.QPushButton(self.centralwidget)
        self.but_trim.setObjectName("but_trim")
        self.gridLayout.addWidget(self.but_trim, 1, 0, 1, 1)
        self.but_plot = QtWidgets.QPushButton(self.centralwidget)
        self.but_plot.setObjectName("but_plot")
        self.gridLayout.addWidget(self.but_plot, 4, 0, 1, 2)
        self.but_statusTrim = QtWidgets.QPushButton(self.centralwidget)
        self.but_statusTrim.setObjectName("but_statusTrim")
        self.gridLayout.addWidget(self.but_statusTrim, 1, 1, 1, 1)
        self.but_statuFilter = QtWidgets.QPushButton(self.centralwidget)
        self.but_statuFilter.setObjectName("but_statuFilter")
        self.gridLayout.addWidget(self.but_statuFilter, 2, 1, 1, 1)
        self.but_statusCNC = QtWidgets.QPushButton(self.centralwidget)
        self.but_statusCNC.setObjectName("but_statusCNC")
        self.gridLayout.addWidget(self.but_statusCNC, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 176, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "G-Code Converter"))
        self.but_openFile.setText(_translate("MainWindow", "OPEN"))
        self.but_cnc.setText(_translate("MainWindow", "GEN_CNC"))
        self.but_filter.setText(_translate("MainWindow", "FILTER"))
        self.but_gCode.setText(_translate("MainWindow", "MAKE G-Code"))
        self.but_status_import.setText(_translate("MainWindow", "Status"))
        self.but_trim.setText(_translate("MainWindow", "TRIM"))
        self.but_plot.setText(_translate("MainWindow", "PLOT"))
        self.but_statusTrim.setText(_translate("MainWindow", "Status"))
        self.but_statuFilter.setText(_translate("MainWindow", "Status"))
        self.but_statusCNC.setText(_translate("MainWindow", "Status"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
