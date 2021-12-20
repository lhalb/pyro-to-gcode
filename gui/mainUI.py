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
        MainWindow.resize(529, 896)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.but_statusCNC = QtWidgets.QPushButton(self.centralwidget)
        self.but_statusCNC.setObjectName("but_statusCNC")
        self.gridLayout.addWidget(self.but_statusCNC, 3, 1, 1, 1)
        self.but_statusTrim = QtWidgets.QPushButton(self.centralwidget)
        self.but_statusTrim.setObjectName("but_statusTrim")
        self.gridLayout.addWidget(self.but_statusTrim, 1, 1, 1, 1)
        self.but_openFile = QtWidgets.QPushButton(self.centralwidget)
        self.but_openFile.setObjectName("but_openFile")
        self.gridLayout.addWidget(self.but_openFile, 0, 0, 1, 1)
        self.but_status_import = QtWidgets.QPushButton(self.centralwidget)
        self.but_status_import.setObjectName("but_status_import")
        self.gridLayout.addWidget(self.but_status_import, 0, 1, 1, 1)
        self.but_statuFilter = QtWidgets.QPushButton(self.centralwidget)
        self.but_statuFilter.setObjectName("but_statuFilter")
        self.gridLayout.addWidget(self.but_statuFilter, 2, 1, 1, 1)
        self.but_gCode = QtWidgets.QPushButton(self.centralwidget)
        self.but_gCode.setObjectName("but_gCode")
        self.gridLayout.addWidget(self.but_gCode, 4, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(-1, 10, 10, 10)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.plotwidget = MplWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotwidget.sizePolicy().hasHeightForWidth())
        self.plotwidget.setSizePolicy(sizePolicy)
        self.plotwidget.setMinimumSize(QtCore.QSize(500, 300))
        self.plotwidget.setObjectName("plotwidget")
        self.verticalLayout_4.addWidget(self.plotwidget)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setContentsMargins(10, -1, -1, -1)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.txt_trim_cut = QtWidgets.QLineEdit(self.tab)
        self.txt_trim_cut.setMaximumSize(QtCore.QSize(35, 16777215))
        self.txt_trim_cut.setObjectName("txt_trim_cut")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txt_trim_cut)
        self.label = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.txt_trim_start = QtWidgets.QLineEdit(self.tab)
        self.txt_trim_start.setMaximumSize(QtCore.QSize(100, 16777215))
        self.txt_trim_start.setObjectName("txt_trim_start")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txt_trim_start)
        self.label_2 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.txt_trim_end = QtWidgets.QLineEdit(self.tab)
        self.txt_trim_end.setMaximumSize(QtCore.QSize(100, 16777215))
        self.txt_trim_end.setObjectName("txt_trim_end")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.txt_trim_end)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.FieldRole, spacerItem)
        self.horizontalLayout.addLayout(self.formLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.but_trim_apply = QtWidgets.QPushButton(self.tab)
        self.but_trim_apply.setObjectName("but_trim_apply")
        self.verticalLayout_3.addWidget(self.but_trim_apply)
        self.but_trim_undo = QtWidgets.QPushButton(self.tab)
        self.but_trim_undo.setObjectName("but_trim_undo")
        self.verticalLayout_3.addWidget(self.but_trim_undo)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.toolBox = QtWidgets.QToolBox(self.tab_2)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 476, 71))
        self.page.setObjectName("page")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.page)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.para_filt_sav_n = QtWidgets.QSlider(self.page)
        self.para_filt_sav_n.setOrientation(QtCore.Qt.Horizontal)
        self.para_filt_sav_n.setObjectName("para_filt_sav_n")
        self.horizontalLayout_3.addWidget(self.para_filt_sav_n)
        self.txt_para_filt_sav_n = QtWidgets.QLineEdit(self.page)
        self.txt_para_filt_sav_n.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.txt_para_filt_sav_n.setFont(font)
        self.txt_para_filt_sav_n.setObjectName("txt_para_filt_sav_n")
        self.horizontalLayout_3.addWidget(self.txt_para_filt_sav_n)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setContentsMargins(10, -1, 10, -1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_6 = QtWidgets.QLabel(self.page)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 1, 2, 1, 1, QtCore.Qt.AlignRight)
        self.para_filt_sav_deriv = QtWidgets.QSpinBox(self.page)
        self.para_filt_sav_deriv.setObjectName("para_filt_sav_deriv")
        self.gridLayout_3.addWidget(self.para_filt_sav_deriv, 1, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.page)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 1, 4, 1, 1, QtCore.Qt.AlignRight)
        self.label_5 = QtWidgets.QLabel(self.page)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.label_8 = QtWidgets.QLabel(self.page)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 1, 6, 1, 1, QtCore.Qt.AlignRight)
        self.para_filt_sav_poly = QtWidgets.QSpinBox(self.page)
        self.para_filt_sav_poly.setObjectName("para_filt_sav_poly")
        self.gridLayout_3.addWidget(self.para_filt_sav_poly, 1, 1, 1, 1)
        self.para_filt_sav_delta = QtWidgets.QDoubleSpinBox(self.page)
        self.para_filt_sav_delta.setObjectName("para_filt_sav_delta")
        self.gridLayout_3.addWidget(self.para_filt_sav_delta, 1, 5, 1, 1)
        self.para_filt_sav_mode = QtWidgets.QComboBox(self.page)
        self.para_filt_sav_mode.setObjectName("para_filt_sav_mode")
        self.para_filt_sav_mode.addItem("")
        self.para_filt_sav_mode.addItem("")
        self.para_filt_sav_mode.addItem("")
        self.para_filt_sav_mode.addItem("")
        self.gridLayout_3.addWidget(self.para_filt_sav_mode, 1, 7, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_3)
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 476, 204))
        self.page_2.setObjectName("page_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_9 = QtWidgets.QLabel(self.page_2)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_4.addWidget(self.label_9)
        self.para_filt_med_n = QtWidgets.QSlider(self.page_2)
        self.para_filt_med_n.setOrientation(QtCore.Qt.Horizontal)
        self.para_filt_med_n.setObjectName("para_filt_med_n")
        self.horizontalLayout_4.addWidget(self.para_filt_med_n)
        self.txt_para_filt_n_med = QtWidgets.QLineEdit(self.page_2)
        self.txt_para_filt_n_med.setMaximumSize(QtCore.QSize(60, 16777215))
        self.txt_para_filt_n_med.setObjectName("txt_para_filt_n_med")
        self.horizontalLayout_4.addWidget(self.txt_para_filt_n_med)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.toolBox.addItem(self.page_2, "")
        self.verticalLayout_7.addWidget(self.toolBox)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.but_filt_apply = QtWidgets.QPushButton(self.tab_2)
        self.but_filt_apply.setObjectName("but_filt_apply")
        self.horizontalLayout_5.addWidget(self.but_filt_apply)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.but_filt_undo = QtWidgets.QPushButton(self.tab_2)
        self.but_filt_undo.setObjectName("but_filt_undo")
        self.horizontalLayout_5.addWidget(self.but_filt_undo)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.cb_cnc_np = ToggleSwitch(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_cnc_np.sizePolicy().hasHeightForWidth())
        self.cb_cnc_np.setSizePolicy(sizePolicy)
        self.cb_cnc_np.setObjectName("cb_cnc_np")
        self.horizontalLayout_6.addWidget(self.cb_cnc_np)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_12 = QtWidgets.QLabel(self.tab_3)
        self.label_12.setObjectName("label_12")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.sb_cnc_ang = QtWidgets.QDoubleSpinBox(self.tab_3)
        self.sb_cnc_ang.setObjectName("sb_cnc_ang")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.sb_cnc_ang)
        self.horizontalLayout_6.addLayout(self.formLayout_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, 0, 0, -1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.groupBox = QtWidgets.QGroupBox(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setObjectName("label_10")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.para_cnc_i0 = QtWidgets.QLineEdit(self.groupBox)
        self.para_cnc_i0.setMaximumSize(QtCore.QSize(30, 16777215))
        self.para_cnc_i0.setObjectName("para_cnc_i0")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.para_cnc_i0)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setObjectName("label_11")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.para_cnc_di = QtWidgets.QLineEdit(self.groupBox)
        self.para_cnc_di.setMaximumSize(QtCore.QSize(30, 16777215))
        self.para_cnc_di.setObjectName("para_cnc_di")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.para_cnc_di)
        self.verticalLayout_8.addLayout(self.formLayout_2)
        self.horizontalLayout_7.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.tab_cnc_cont = QtWidgets.QTableWidget(self.groupBox_2)
        self.tab_cnc_cont.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.tab_cnc_cont.setAlternatingRowColors(True)
        self.tab_cnc_cont.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tab_cnc_cont.setObjectName("tab_cnc_cont")
        self.tab_cnc_cont.setColumnCount(4)
        self.tab_cnc_cont.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tab_cnc_cont.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tab_cnc_cont.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tab_cnc_cont.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tab_cnc_cont.setHorizontalHeaderItem(3, item)
        self.tab_cnc_cont.horizontalHeader().setVisible(False)
        self.tab_cnc_cont.horizontalHeader().setCascadingSectionResizes(False)
        self.tab_cnc_cont.horizontalHeader().setDefaultSectionSize(50)
        self.tab_cnc_cont.horizontalHeader().setHighlightSections(False)
        self.tab_cnc_cont.horizontalHeader().setStretchLastSection(False)
        self.tab_cnc_cont.verticalHeader().setVisible(False)
        self.tab_cnc_cont.verticalHeader().setCascadingSectionResizes(False)
        self.verticalLayout_9.addWidget(self.tab_cnc_cont)
        self.horizontalLayout_7.addWidget(self.groupBox_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_8.addWidget(self.pushButton_2)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem4)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_8.addWidget(self.pushButton_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.tabWidget.addTab(self.tab_6, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tabWidget.addTab(self.tab_5, "")
        self.verticalLayout_4.addWidget(self.tabWidget)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 529, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        self.toolBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "G-Code Converter"))
        self.but_statusCNC.setText(_translate("MainWindow", "Status"))
        self.but_statusTrim.setText(_translate("MainWindow", "Status"))
        self.but_openFile.setText(_translate("MainWindow", "OPEN"))
        self.but_openFile.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.but_status_import.setText(_translate("MainWindow", "Status"))
        self.but_statuFilter.setText(_translate("MainWindow", "Status"))
        self.but_gCode.setText(_translate("MainWindow", "MAKE G-Code"))
        self.but_gCode.setShortcut(_translate("MainWindow", "Ctrl+Return"))
        self.label_3.setText(_translate("MainWindow", "Cut"))
        self.txt_trim_cut.setInputMask(_translate("MainWindow", "d000"))
        self.txt_trim_cut.setText(_translate("MainWindow", "500"))
        self.label.setText(_translate("MainWindow", "Start"))
        self.label_2.setText(_translate("MainWindow", "End"))
        self.but_trim_apply.setText(_translate("MainWindow", "Apply"))
        self.but_trim_undo.setText(_translate("MainWindow", "Undo"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Trimming"))
        self.label_4.setText(_translate("MainWindow", "n"))
        self.label_6.setText(_translate("MainWindow", "d"))
        self.label_7.setText(_translate("MainWindow", "D"))
        self.label_5.setText(_translate("MainWindow", "p"))
        self.label_8.setText(_translate("MainWindow", "mode"))
        self.para_filt_sav_mode.setItemText(0, _translate("MainWindow", "nearest"))
        self.para_filt_sav_mode.setItemText(1, _translate("MainWindow", "mirror"))
        self.para_filt_sav_mode.setItemText(2, _translate("MainWindow", "constant"))
        self.para_filt_sav_mode.setItemText(3, _translate("MainWindow", "wrap"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("MainWindow", "Savgol"))
        self.label_9.setText(_translate("MainWindow", "n"))
        self.txt_para_filt_n_med.setInputMask(_translate("MainWindow", "d00000000"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("MainWindow", "Median"))
        self.but_filt_apply.setText(_translate("MainWindow", "Apply"))
        self.but_filt_undo.setText(_translate("MainWindow", "Undo"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Filter"))
        self.cb_cnc_np.setText(_translate("MainWindow", "CheckBox"))
        self.label_12.setText(_translate("MainWindow", "ANG"))
        self.groupBox.setTitle(_translate("MainWindow", "Regelung"))
        self.label_10.setText(_translate("MainWindow", "I0"))
        self.label_11.setText(_translate("MainWindow", "dIS"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Kontur"))
        item = self.tab_cnc_cont.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ANG"))
        item = self.tab_cnc_cont.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "IB"))
        item = self.tab_cnc_cont.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "IL"))
        item = self.tab_cnc_cont.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "vs"))
        self.pushButton_2.setText(_translate("MainWindow", "Apply"))
        self.pushButton_3.setText(_translate("MainWindow", "Undo"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "CNC"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Export"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("MainWindow", "Plot"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Close"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
from gui.mplwidget import MplWidget
from gui.toggleswitch import ToggleSwitch


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
