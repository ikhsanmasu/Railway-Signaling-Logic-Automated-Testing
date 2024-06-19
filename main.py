from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QInputDialog, QApplication, QFileDialog, QDialog, QMessageBox
import os
import data
import pandas as pd
from PyQt5.QtCore import Qt
import pickle
from modbus import hima
from testing import testingBot

defaultITDir = "C:/File Ikhsan/Development/Testing Automation/Medan Bawah 1C/IT MEDAN BAWAH 1C - TESTINGBOT.xlsx"
defaultVDUDir = "C:/File Ikhsan/Development/Testing Automation/Medan Bawah 1C/13. REGISTER - FROM VDU.csv"
defaultIPhima = "10.10.3.107"
defaultFieldStart = "36"
defaultIndStart = "250"

class Ui_MainWindow(object):
    def __init__(self):
        # IT1, IT2, RUTE, SIGNAL, PM, TRACK, BLOK, JPL
        self.IT1 = []
        self.IT2 = []
        self.RUTE = []
        self.SIGNAL = []
        self.PM = []
        self.Wesel = []
        self.Deraileur = []
        self.TRACK = []
        self.BLOK = []
        self.JPL = []

        self.inputData = []
        self.outputData = []
        self.internalData = []

        self.simCtrlData = []
        self.simINDData = []

        self.pbStart = 28
        self.simCtrlStart = 36
        self.simINDStart = 250


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(935, 943)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 911, 241))
        self.groupBox.setStyleSheet("background-color: rgb(227, 229, 240);")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(11, 20, 891, 181))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.horizontalLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.Field_CTRL_Start = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.Field_CTRL_Start.setMaximumSize(QtCore.QSize(40, 16777215))
        self.Field_CTRL_Start.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Field_CTRL_Start.setObjectName("Field_CTRL_Start")
        self.gridLayout.addWidget(self.Field_CTRL_Start, 4, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.VDU_CTRL_Directory = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.VDU_CTRL_Directory.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.VDU_CTRL_Directory.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.VDU_CTRL_Directory.setObjectName("VDU_CTRL_Directory")
        self.gridLayout.addWidget(self.VDU_CTRL_Directory, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.search_IT_Directory = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.search_IT_Directory.setMaximumSize(QtCore.QSize(25, 16777215))
        self.search_IT_Directory.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.search_IT_Directory.setIconSize(QtCore.QSize(16, 16))
        self.search_IT_Directory.setObjectName("search_IT_Directory")
        self.gridLayout.addWidget(self.search_IT_Directory, 0, 3, 1, 1)
        self.search_VDU_CTRL_Directory = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.search_VDU_CTRL_Directory.setMaximumSize(QtCore.QSize(25, 16777215))
        self.search_VDU_CTRL_Directory.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.search_VDU_CTRL_Directory.setObjectName("search_VDU_CTRL_Directory")
        self.gridLayout.addWidget(self.search_VDU_CTRL_Directory, 1, 3, 1, 1)
        self.VDU_CTRL_Start = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.VDU_CTRL_Start.setMaximumSize(QtCore.QSize(40, 16777215))
        self.VDU_CTRL_Start.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.VDU_CTRL_Start.setObjectName("VDU_CTRL_Start")
        self.gridLayout.addWidget(self.VDU_CTRL_Start, 3, 1, 1, 1)
        self.IT_Directory = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.IT_Directory.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.IT_Directory.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.IT_Directory.setObjectName("IT_Directory")
        self.gridLayout.addWidget(self.IT_Directory, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.Field_IND_Start = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.Field_IND_Start.setMaximumSize(QtCore.QSize(40, 16777215))
        self.Field_IND_Start.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Field_IND_Start.setObjectName("Field_IND_Start")
        self.gridLayout.addWidget(self.Field_IND_Start, 5, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        self.IP_HIMA = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.IP_HIMA.setMaximumSize(QtCore.QSize(100, 16777215))
        self.IP_HIMA.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.IP_HIMA.setObjectName("IP_HIMA")
        self.gridLayout.addWidget(self.IP_HIMA, 2, 1, 1, 1)
        self.Generate_Register_Hima = QtWidgets.QPushButton(self.groupBox)
        self.Generate_Register_Hima.setGeometry(QtCore.QRect(10, 210, 891, 23))
        self.Generate_Register_Hima.setStyleSheet("background-color: rgb(85, 194, 218);")
        self.Generate_Register_Hima.setObjectName("Generate_Register_Hima")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 490, 911, 311))
        self.groupBox_3.setStyleSheet("background-color: rgb(251, 255, 202);")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_3)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(11, 20, 891, 202))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.horizontalLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_14 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_14.setText("")
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 1, 2, 1, 1)
        self.InterlockingTableTest = QtWidgets.QCheckBox(self.horizontalLayoutWidget_3)
        self.InterlockingTableTest.setEnabled(False)
        self.InterlockingTableTest.setObjectName("InterlockingTableTest")
        self.gridLayout_3.addWidget(self.InterlockingTableTest, 1, 0, 1, 1)
        self.VisualTest = QtWidgets.QCheckBox(self.horizontalLayoutWidget_3)
        self.VisualTest.setEnabled(False)
        self.VisualTest.setObjectName("VisualTest")
        self.gridLayout_3.addWidget(self.VisualTest, 3, 0, 1, 1)
        self.ConflictRouteTest = QtWidgets.QCheckBox(self.horizontalLayoutWidget_3)
        self.ConflictRouteTest.setEnabled(False)
        self.ConflictRouteTest.setObjectName("ConflictRouteTest")
        self.gridLayout_3.addWidget(self.ConflictRouteTest, 2, 0, 1, 1)
        self.Start_Route = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.Start_Route.setEnabled(False)
        self.Start_Route.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.Start_Route.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Start_Route.setObjectName("Start_Route")
        self.gridLayout_3.addWidget(self.Start_Route, 7, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 2, 2, 1, 1)
        self.Finish_Route = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.Finish_Route.setEnabled(False)
        self.Finish_Route.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.Finish_Route.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Finish_Route.setObjectName("Finish_Route")
        self.gridLayout_3.addWidget(self.Finish_Route, 7, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 6, 2, 1, 1)
        self.FunctionalTest = QtWidgets.QCheckBox(self.horizontalLayoutWidget_3)
        self.FunctionalTest.setEnabled(False)
        self.FunctionalTest.setObjectName("FunctionalTest")
        self.gridLayout_3.addWidget(self.FunctionalTest, 0, 0, 1, 1)
        self.Fucntional_Test_list = QtWidgets.QComboBox(self.horizontalLayoutWidget_3)
        self.Fucntional_Test_list.setEnabled(False)
        self.Fucntional_Test_list.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Fucntional_Test_list.setObjectName("Fucntional_Test_list")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.Fucntional_Test_list.addItem("")
        self.gridLayout_3.addWidget(self.Fucntional_Test_list, 0, 1, 1, 2)
        self.label_9 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 7, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 6, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 5, 0, 1, 1)
        self.DeepTest = QtWidgets.QCheckBox(self.horizontalLayoutWidget_3)
        self.DeepTest.setEnabled(False)
        self.DeepTest.setObjectName("DeepTest")
        self.gridLayout_3.addWidget(self.DeepTest, 4, 0, 1, 1)
        self.Start_Route_2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.Start_Route_2.setEnabled(False)
        self.Start_Route_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.Start_Route_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Start_Route_2.setObjectName("Start_Route_2")
        self.gridLayout_3.addWidget(self.Start_Route_2, 8, 0, 1, 1)
        self.Finish_Route_2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget_3)
        self.Finish_Route_2.setEnabled(False)
        self.Finish_Route_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.Finish_Route_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Finish_Route_2.setObjectName("Finish_Route_2")
        self.gridLayout_3.addWidget(self.Finish_Route_2, 8, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 8, 1, 1, 1)
        self.StartTesting = QtWidgets.QPushButton(self.groupBox_3)
        self.StartTesting.setEnabled(False)
        self.StartTesting.setGeometry(QtCore.QRect(10, 240, 891, 23))
        self.StartTesting.setStyleSheet("background-color: rgb(93, 190, 163);")
        self.StartTesting.setObjectName("StartTesting")
        self.progressBar = QtWidgets.QProgressBar(self.groupBox_3)
        self.progressBar.setGeometry(QtCore.QRect(10, 270, 891, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 260, 911, 221))
        self.groupBox_2.setStyleSheet("background-color: rgb(225, 255, 199);")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(11, 20, 891, 193))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.horizontalLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.TRACK_CLEAR_PB_DI = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.TRACK_CLEAR_PB_DI.setEnabled(False)
        self.TRACK_CLEAR_PB_DI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.TRACK_CLEAR_PB_DI.setObjectName("TRACK_CLEAR_PB_DI")
        self.gridLayout_2.addWidget(self.TRACK_CLEAR_PB_DI, 1, 5, 1, 1)
        self.THB_PB_DI = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.THB_PB_DI.setEnabled(False)
        self.THB_PB_DI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.THB_PB_DI.setObjectName("THB_PB_DI")
        self.gridLayout_2.addWidget(self.THB_PB_DI, 0, 6, 1, 1)
        self.CHECK_ECR_R = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_ECR_R.setEnabled(False)
        self.CHECK_ECR_R.setChecked(True)
        self.CHECK_ECR_R.setObjectName("CHECK_ECR_R")
        self.gridLayout_2.addWidget(self.CHECK_ECR_R, 4, 4, 1, 1)
        self.CHECK_DATA_PB_DI = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.CHECK_DATA_PB_DI.setEnabled(False)
        self.CHECK_DATA_PB_DI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.CHECK_DATA_PB_DI.setObjectName("CHECK_DATA_PB_DI")
        self.gridLayout_2.addWidget(self.CHECK_DATA_PB_DI, 0, 9, 1, 1)
        self.CLEAR_ALLTRACK_PB_DI = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.CLEAR_ALLTRACK_PB_DI.setEnabled(False)
        self.CLEAR_ALLTRACK_PB_DI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.CLEAR_ALLTRACK_PB_DI.setObjectName("CLEAR_ALLTRACK_PB_DI")
        self.gridLayout_2.addWidget(self.CLEAR_ALLTRACK_PB_DI, 1, 6, 1, 1)
        self.CHECK_ENGKOL_NORMAL = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_ENGKOL_NORMAL.setEnabled(False)
        self.CHECK_ENGKOL_NORMAL.setObjectName("CHECK_ENGKOL_NORMAL")
        self.gridLayout_2.addWidget(self.CHECK_ENGKOL_NORMAL, 2, 4, 1, 1)
        self.CHECK_HILANG_DETEKSI = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_HILANG_DETEKSI.setEnabled(False)
        self.CHECK_HILANG_DETEKSI.setObjectName("CHECK_HILANG_DETEKSI")
        self.gridLayout_2.addWidget(self.CHECK_HILANG_DETEKSI, 2, 8, 1, 1)
        self.CHECK_ENGKOL_REVERSE = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_ENGKOL_REVERSE.setEnabled(False)
        self.CHECK_ENGKOL_REVERSE.setObjectName("CHECK_ENGKOL_REVERSE")
        self.gridLayout_2.addWidget(self.CHECK_ENGKOL_REVERSE, 2, 5, 1, 1)
        self.INPUT_POINT = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.INPUT_POINT.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.INPUT_POINT.sizePolicy().hasHeightForWidth())
        self.INPUT_POINT.setSizePolicy(sizePolicy)
        self.INPUT_POINT.setMaximumSize(QtCore.QSize(100, 16777215))
        self.INPUT_POINT.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.INPUT_POINT.setObjectName("INPUT_POINT")
        self.gridLayout_2.addWidget(self.INPUT_POINT, 2, 2, 1, 1)
        self.TPR_BANTU_PB_DI = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.TPR_BANTU_PB_DI.setEnabled(False)
        self.TPR_BANTU_PB_DI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.TPR_BANTU_PB_DI.setObjectName("TPR_BANTU_PB_DI")
        self.gridLayout_2.addWidget(self.TPR_BANTU_PB_DI, 0, 5, 1, 1)
        self.TWT_ALL_PB_DI = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.TWT_ALL_PB_DI.setEnabled(False)
        self.TWT_ALL_PB_DI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.TWT_ALL_PB_DI.setObjectName("TWT_ALL_PB_DI")
        self.gridLayout_2.addWidget(self.TWT_ALL_PB_DI, 0, 4, 1, 1)
        self.CHECK_ECR_G = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_ECR_G.setEnabled(False)
        self.CHECK_ECR_G.setChecked(True)
        self.CHECK_ECR_G.setObjectName("CHECK_ECR_G")
        self.gridLayout_2.addWidget(self.CHECK_ECR_G, 4, 6, 1, 1)
        self.CHECK_ECR_Y = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_ECR_Y.setEnabled(False)
        self.CHECK_ECR_Y.setChecked(True)
        self.CHECK_ECR_Y.setObjectName("CHECK_ECR_Y")
        self.gridLayout_2.addWidget(self.CHECK_ECR_Y, 4, 5, 1, 1)
        self.LAMPTEST_PB_DI = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.LAMPTEST_PB_DI.setEnabled(False)
        self.LAMPTEST_PB_DI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.LAMPTEST_PB_DI.setObjectName("LAMPTEST_PB_DI")
        self.gridLayout_2.addWidget(self.LAMPTEST_PB_DI, 0, 7, 1, 1)
        self.CHECK_GANJAL_REVERSE = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_GANJAL_REVERSE.setEnabled(False)
        self.CHECK_GANJAL_REVERSE.setObjectName("CHECK_GANJAL_REVERSE")
        self.gridLayout_2.addWidget(self.CHECK_GANJAL_REVERSE, 2, 7, 1, 1)
        self.STOP_TEST_PB_DI = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.STOP_TEST_PB_DI.setEnabled(False)
        self.STOP_TEST_PB_DI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.STOP_TEST_PB_DI.setObjectName("STOP_TEST_PB_DI")
        self.gridLayout_2.addWidget(self.STOP_TEST_PB_DI, 0, 8, 1, 1)
        self.CHECK_GANJAL_NORMAL = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_GANJAL_NORMAL.setEnabled(False)
        self.CHECK_GANJAL_NORMAL.setObjectName("CHECK_GANJAL_NORMAL")
        self.gridLayout_2.addWidget(self.CHECK_GANJAL_NORMAL, 2, 6, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 2, 1, 1, 1)
        self.INPUT_TRACK = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.INPUT_TRACK.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.INPUT_TRACK.sizePolicy().hasHeightForWidth())
        self.INPUT_TRACK.setSizePolicy(sizePolicy)
        self.INPUT_TRACK.setMaximumSize(QtCore.QSize(100, 16777215))
        self.INPUT_TRACK.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.INPUT_TRACK.setObjectName("INPUT_TRACK")
        self.gridLayout_2.addWidget(self.INPUT_TRACK, 1, 2, 1, 1)
        self.TRACK_OCCUPIED_PB_DI = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.TRACK_OCCUPIED_PB_DI.setEnabled(False)
        self.TRACK_OCCUPIED_PB_DI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.TRACK_OCCUPIED_PB_DI.setObjectName("TRACK_OCCUPIED_PB_DI")
        self.gridLayout_2.addWidget(self.TRACK_OCCUPIED_PB_DI, 1, 4, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 1, 1, 1, 1)
        self.CHECK_EKR = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_EKR.setEnabled(False)
        self.CHECK_EKR.setChecked(True)
        self.CHECK_EKR.setObjectName("CHECK_EKR")
        self.gridLayout_2.addWidget(self.CHECK_EKR, 4, 7, 1, 1)
        self.CHECK_DKR = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_DKR.setEnabled(False)
        self.CHECK_DKR.setChecked(True)
        self.CHECK_DKR.setObjectName("CHECK_DKR")
        self.gridLayout_2.addWidget(self.CHECK_DKR, 4, 8, 1, 1)
        self.OCCUPIED_ALLTRACK_PB_DI = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.OCCUPIED_ALLTRACK_PB_DI.setEnabled(False)
        self.OCCUPIED_ALLTRACK_PB_DI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.OCCUPIED_ALLTRACK_PB_DI.setObjectName("OCCUPIED_ALLTRACK_PB_DI")
        self.gridLayout_2.addWidget(self.OCCUPIED_ALLTRACK_PB_DI, 1, 7, 1, 1)
        self.CHECK_SECR = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_SECR.setEnabled(False)
        self.CHECK_SECR.setChecked(True)
        self.CHECK_SECR.setObjectName("CHECK_SECR")
        self.gridLayout_2.addWidget(self.CHECK_SECR, 4, 9, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 4, 1, 1, 1)
        self.INPUT_SIGNAL = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.INPUT_SIGNAL.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.INPUT_SIGNAL.sizePolicy().hasHeightForWidth())
        self.INPUT_SIGNAL.setSizePolicy(sizePolicy)
        self.INPUT_SIGNAL.setMaximumSize(QtCore.QSize(100, 16777215))
        self.INPUT_SIGNAL.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.INPUT_SIGNAL.setObjectName("INPUT_SIGNAL")
        self.gridLayout_2.addWidget(self.INPUT_SIGNAL, 4, 2, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_18.setObjectName("label_18")
        self.gridLayout_2.addWidget(self.label_18, 3, 1, 1, 1)
        self.CHECK_DERAILEUR_TURUN = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_DERAILEUR_TURUN.setEnabled(False)
        self.CHECK_DERAILEUR_TURUN.setObjectName("CHECK_DERAILEUR_TURUN")
        self.gridLayout_2.addWidget(self.CHECK_DERAILEUR_TURUN, 3, 5, 1, 1)
        self.CHECK_DERAILEUR_NAIK = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_DERAILEUR_NAIK.setEnabled(False)
        self.CHECK_DERAILEUR_NAIK.setTabletTracking(False)
        self.CHECK_DERAILEUR_NAIK.setChecked(True)
        self.CHECK_DERAILEUR_NAIK.setObjectName("CHECK_DERAILEUR_NAIK")
        self.gridLayout_2.addWidget(self.CHECK_DERAILEUR_NAIK, 3, 4, 1, 1)
        self.INPUT_DERAILEUR = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.INPUT_DERAILEUR.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.INPUT_DERAILEUR.sizePolicy().hasHeightForWidth())
        self.INPUT_DERAILEUR.setSizePolicy(sizePolicy)
        self.INPUT_DERAILEUR.setMaximumSize(QtCore.QSize(100, 16777215))
        self.INPUT_DERAILEUR.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.INPUT_DERAILEUR.setObjectName("INPUT_DERAILEUR")
        self.gridLayout_2.addWidget(self.INPUT_DERAILEUR, 3, 2, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_17.setObjectName("label_17")
        self.gridLayout_2.addWidget(self.label_17, 5, 1, 1, 2)
        self.CHECK_INVERTER_FAIL = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_INVERTER_FAIL.setEnabled(False)
        self.CHECK_INVERTER_FAIL.setObjectName("CHECK_INVERTER_FAIL")
        self.gridLayout_2.addWidget(self.CHECK_INVERTER_FAIL, 6, 5, 1, 1)
        self.CHECK_VDR = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_VDR.setEnabled(False)
        self.CHECK_VDR.setChecked(True)
        self.CHECK_VDR.setObjectName("CHECK_VDR")
        self.gridLayout_2.addWidget(self.CHECK_VDR, 5, 4, 1, 1)
        self.CHECK_GENSET = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_GENSET.setEnabled(False)
        self.CHECK_GENSET.setObjectName("CHECK_GENSET")
        self.gridLayout_2.addWidget(self.CHECK_GENSET, 5, 7, 1, 1)
        self.CHECK_BBM_HABIS = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_BBM_HABIS.setEnabled(False)
        self.CHECK_BBM_HABIS.setObjectName("CHECK_BBM_HABIS")
        self.gridLayout_2.addWidget(self.CHECK_BBM_HABIS, 6, 7, 1, 1)
        self.CHECK_UPS_LOWBAT = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_UPS_LOWBAT.setEnabled(False)
        self.CHECK_UPS_LOWBAT.setObjectName("CHECK_UPS_LOWBAT")
        self.gridLayout_2.addWidget(self.CHECK_UPS_LOWBAT, 6, 4, 1, 1)
        self.CHECK_UPS = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_UPS.setEnabled(False)
        self.CHECK_UPS.setObjectName("CHECK_UPS")
        self.gridLayout_2.addWidget(self.CHECK_UPS, 5, 6, 1, 1)
        self.CHECK_GAGAL_START = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_GAGAL_START.setEnabled(False)
        self.CHECK_GAGAL_START.setObjectName("CHECK_GAGAL_START")
        self.gridLayout_2.addWidget(self.CHECK_GAGAL_START, 6, 6, 1, 1)
        self.CHECK_PLN = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.CHECK_PLN.setEnabled(False)
        self.CHECK_PLN.setChecked(True)
        self.CHECK_PLN.setObjectName("CHECK_PLN")
        self.gridLayout_2.addWidget(self.CHECK_PLN, 5, 5, 1, 1)
        self.UPDATE_POINT_PB_DI = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.UPDATE_POINT_PB_DI.setEnabled(False)
        self.UPDATE_POINT_PB_DI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.UPDATE_POINT_PB_DI.setObjectName("UPDATE_POINT_PB_DI")
        self.gridLayout_2.addWidget(self.UPDATE_POINT_PB_DI, 2, 3, 1, 1)
        self.UPDATE_DERAILEUR_PB_DI = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.UPDATE_DERAILEUR_PB_DI.setEnabled(False)
        self.UPDATE_DERAILEUR_PB_DI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.UPDATE_DERAILEUR_PB_DI.setObjectName("UPDATE_DERAILEUR_PB_DI")
        self.gridLayout_2.addWidget(self.UPDATE_DERAILEUR_PB_DI, 3, 3, 1, 1)
        self.UPDATE_SIGNAL_PB_DI = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.UPDATE_SIGNAL_PB_DI.setEnabled(False)
        self.UPDATE_SIGNAL_PB_DI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.UPDATE_SIGNAL_PB_DI.setObjectName("UPDATE_SIGNAL_PB_DI")
        self.gridLayout_2.addWidget(self.UPDATE_SIGNAL_PB_DI, 4, 3, 1, 1)
        self.UPDATE_UTILITY_PB_DI = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.UPDATE_UTILITY_PB_DI.setEnabled(False)
        self.UPDATE_UTILITY_PB_DI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.UPDATE_UTILITY_PB_DI.setObjectName("UPDATE_UTILITY_PB_DI")
        self.gridLayout_2.addWidget(self.UPDATE_UTILITY_PB_DI, 5, 3, 1, 1)
        self.START_MODBUS_PB_DI = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.START_MODBUS_PB_DI.setEnabled(False)
        self.START_MODBUS_PB_DI.setStyleSheet("background-color: rgb(70, 129, 244);")
        self.START_MODBUS_PB_DI.setObjectName("START_MODBUS_PB_DI")
        self.gridLayout_2.addWidget(self.START_MODBUS_PB_DI, 0, 1, 1, 2)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 800, 911, 101))
        self.groupBox_4.setStyleSheet("background-color: rgb(255, 211, 196);")
        self.groupBox_4.setObjectName("groupBox_4")
        self.Information = QtWidgets.QLabel(self.groupBox_4)
        self.Information.setGeometry(QtCore.QRect(10, 20, 891, 71))
        self.Information.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Information.setText("")
        self.Information.setObjectName("Information")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 935, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.search_IT_Directory.clicked.connect(self.searchITdir)
        self.search_VDU_CTRL_Directory.clicked.connect(self.searchVDUdir)
        self.Generate_Register_Hima.clicked.connect(self.generate)

        self.START_MODBUS_PB_DI.clicked.connect(self.startModbus)

        self.TWT_ALL_PB_DI.clicked.connect(self.twtAll)
        self.TPR_BANTU_PB_DI.clicked.connect(self.tprBantu)
        self.THB_PB_DI.clicked.connect(self.thbPBDI)
        self.LAMPTEST_PB_DI.clicked.connect(self.lamptestPBDI)
        self.STOP_TEST_PB_DI.clicked.connect(self.forceStopTest)
        self.CHECK_DATA_PB_DI.clicked.connect(self.cekData)

        self.UPDATE_POINT_PB_DI.clicked.connect(self.updatePoint)
        self.UPDATE_DERAILEUR_PB_DI.clicked.connect(self.updateDeraileur)
        self.UPDATE_SIGNAL_PB_DI.clicked.connect(self.updateSignal)
        self.UPDATE_UTILITY_PB_DI.clicked.connect(self.updateUtility)

        self.TRACK_OCCUPIED_PB_DI.clicked.connect(self.occTrack)
        self.TRACK_CLEAR_PB_DI.clicked.connect(self.clearTrack)
        self.OCCUPIED_ALLTRACK_PB_DI.clicked.connect(self.occAllTrack)
        self.CLEAR_ALLTRACK_PB_DI.clicked.connect(self.clearAllTrack)

        self.ConflictRouteTest.stateChanged.connect(self.ConflictRouteChangeCheck)
        self.StartTesting.clicked.connect(self.startTest)

        # threading modbus
        self.threadMosbus = QThread()
        self.modbus = hima()
        self.modbus.moveToThread(self.threadMosbus)
        self.threadMosbus.started.connect(self.modbus.run)
        self.threadMosbus.start()

        # threading testing
        self.threadTesting = QThread()
        self.testingBot = testingBot(self.modbus)
        self.testingBot.moveToThread(self.threadTesting)
        self.threadTesting.started.connect(self.testingBot.run)
        self.threadTesting.start()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Testingbot"))
        self.groupBox.setTitle(_translate("MainWindow", "Configuration"))
        self.Field_CTRL_Start.setText(_translate("MainWindow", "36"))
        self.label_3.setText(_translate("MainWindow", "Field CTRL START Address :"))
        self.label_6.setText(_translate("MainWindow", "IP HIMA :"))
        self.label.setText(_translate("MainWindow", "Interlocking Table Directorry :"))
        self.label_5.setText(_translate("MainWindow", "VDU CTRL START Address :"))
        self.search_IT_Directory.setText(_translate("MainWindow", "..."))
        self.search_VDU_CTRL_Directory.setText(_translate("MainWindow", "..."))
        self.VDU_CTRL_Start.setText(_translate("MainWindow", "28"))
        self.label_2.setText(_translate("MainWindow", "Register From VDU Diretory :"))
        self.Field_IND_Start.setText(_translate("MainWindow", "250"))
        self.label_4.setText(_translate("MainWindow", "Field IND START Address :"))
        self.IP_HIMA.setText(_translate("MainWindow", defaultIPhima))
        self.Generate_Register_Hima.setText(_translate("MainWindow", "GENERATE REGISTER HIMA"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Testing"))
        self.InterlockingTableTest.setText(_translate("MainWindow", "INTERLOCKING TABLE TEST"))
        self.VisualTest.setText(_translate("MainWindow", "VISUAL TEST"))
        self.ConflictRouteTest.setText(_translate("MainWindow", "CONFLICT ROUTE TEST"))
        self.Start_Route.setText(_translate("MainWindow", "1"))
        self.Finish_Route.setText(_translate("MainWindow", "max"))
        self.label_8.setText(_translate("MainWindow", "FINISH ROUTE :"))
        self.FunctionalTest.setText(_translate("MainWindow", "FUNCTIONAL TEST"))
        self.Fucntional_Test_list.setItemText(0, _translate("MainWindow", "ALL"))
        self.Fucntional_Test_list.setItemText(1, _translate("MainWindow", "SYSTEM FAILURE"))
        self.Fucntional_Test_list.setItemText(2, _translate("MainWindow", "CONNECTION FAILURE"))
        self.Fucntional_Test_list.setItemText(3, _translate("MainWindow", "PUSH BUTTON FAILURE"))
        self.Fucntional_Test_list.setItemText(4, _translate("MainWindow", "POWER SUPPLY FAILURE"))
        self.Fucntional_Test_list.setItemText(5, _translate("MainWindow", "PUSH BUTTON FUNCTION TEST"))
        self.Fucntional_Test_list.setItemText(6, _translate("MainWindow", "EKR"))
        self.Fucntional_Test_list.setItemText(7, _translate("MainWindow", "ECR"))
        self.Fucntional_Test_list.setItemText(8, _translate("MainWindow", "SECR"))
        self.Fucntional_Test_list.setItemText(9, _translate("MainWindow", "DKR"))
        self.Fucntional_Test_list.setItemText(10, _translate("MainWindow", "CFEK"))
        self.Fucntional_Test_list.setItemText(11, _translate("MainWindow", "Obstacle (N) and (R) "))
        self.Fucntional_Test_list.setItemText(12, _translate("MainWindow", "Detection Loss "))
        self.Fucntional_Test_list.setItemText(13, _translate("MainWindow", "Two Way Obstacle "))
        self.Fucntional_Test_list.setItemText(14, _translate("MainWindow", "Track of Point Failure (TBW)"))
        self.Fucntional_Test_list.setItemText(15, _translate("MainWindow", "Track Section Direct Locking"))
        self.Fucntional_Test_list.setItemText(16, _translate("MainWindow", "Point Locked"))
        self.Fucntional_Test_list.setItemText(17, _translate("MainWindow", "Single Callling Wesel"))
        self.Fucntional_Test_list.setItemText(18, _translate("MainWindow", "Track Section Clear"))
        self.Fucntional_Test_list.setItemText(19, _translate("MainWindow", "Rogue Track"))
        self.Fucntional_Test_list.setItemText(20, _translate("MainWindow",
                                                             "Emergency Signal (Overlap Point Detection Loss)"))
        self.Fucntional_Test_list.setItemText(21, _translate("MainWindow",
                                                             "Emergency Signal (Main Route Point Detection Loss)"))
        self.Fucntional_Test_list.setItemText(22, _translate("MainWindow", "Destination Signal Failure"))
        self.Fucntional_Test_list.setItemText(23, _translate("MainWindow", "Home/Starter Signal Failure"))
        self.Fucntional_Test_list.setItemText(24, _translate("MainWindow", "Flank Signal Failure"))
        self.Fucntional_Test_list.setItemText(25, _translate("MainWindow", "Variable Speed Signal Failure"))
        self.Fucntional_Test_list.setItemText(26, _translate("MainWindow", "Signal Failure on Bypass Line"))
        self.Fucntional_Test_list.setItemText(27, _translate("MainWindow", "POINT CONTROL"))
        self.Fucntional_Test_list.setItemText(28, _translate("MainWindow", "Route Release"))
        self.Fucntional_Test_list.setItemText(29, _translate("MainWindow", "Subroute Release"))
        self.Fucntional_Test_list.setItemText(30, _translate("MainWindow", "Conflict Route (Arrow Indicator)"))
        self.label_9.setText(_translate("MainWindow", "====>"))
        self.label_7.setText(_translate("MainWindow", " START ROUTE :"))
        self.DeepTest.setText(_translate("MainWindow", "DEEP TEST"))
        self.Start_Route_2.setText(_translate("MainWindow", "1"))
        self.Finish_Route_2.setText(_translate("MainWindow", "max"))
        self.label_11.setText(_translate("MainWindow", "====>"))
        self.StartTesting.setText(_translate("MainWindow", "START TESTING"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Tools"))
        self.TRACK_CLEAR_PB_DI.setText(_translate("MainWindow", "TRACK CLEAR"))
        self.THB_PB_DI.setText(_translate("MainWindow", "THB"))
        self.CHECK_ECR_R.setText(_translate("MainWindow", "ECR-R"))
        self.CHECK_DATA_PB_DI.setText(_translate("MainWindow", "CHECK DATA"))
        self.CLEAR_ALLTRACK_PB_DI.setText(_translate("MainWindow", "CLEAR ALL TRACK"))
        self.CHECK_ENGKOL_NORMAL.setText(_translate("MainWindow", "ENGKOL NORMAL"))
        self.CHECK_HILANG_DETEKSI.setText(_translate("MainWindow", "HILANG DETEKSI"))
        self.CHECK_ENGKOL_REVERSE.setText(_translate("MainWindow", "ENGKOL REVERSE"))
        self.INPUT_POINT.setText(_translate("MainWindow", "11A"))
        self.TPR_BANTU_PB_DI.setText(_translate("MainWindow", "TPR BANTU"))
        self.TWT_ALL_PB_DI.setText(_translate("MainWindow", "TWT ALL"))
        self.CHECK_ECR_G.setText(_translate("MainWindow", "ECR-G"))
        self.CHECK_ECR_Y.setText(_translate("MainWindow", "ECR-Y"))
        self.LAMPTEST_PB_DI.setText(_translate("MainWindow", "LAMPTEST"))
        self.CHECK_GANJAL_REVERSE.setText(_translate("MainWindow", "GANJAL REVERSE"))
        self.STOP_TEST_PB_DI.setText(_translate("MainWindow", "FORCE STOP TEST"))
        self.CHECK_GANJAL_NORMAL.setText(_translate("MainWindow", "GANJAL NORMAL"))
        self.label_15.setText(_translate("MainWindow", "POIN T  :"))
        self.INPUT_TRACK.setText(_translate("MainWindow", "12"))
        self.TRACK_OCCUPIED_PB_DI.setText(_translate("MainWindow", "TRACK OCCUPIED"))
        self.label_13.setText(_translate("MainWindow", "TRACK   :"))
        self.CHECK_EKR.setText(_translate("MainWindow", "EKR"))
        self.CHECK_DKR.setText(_translate("MainWindow", "DKR"))
        self.OCCUPIED_ALLTRACK_PB_DI.setText(_translate("MainWindow", "OCC ALL TRACK"))
        self.CHECK_SECR.setText(_translate("MainWindow", "SECR"))
        self.label_16.setText(_translate("MainWindow", "SIGNAL  :"))
        self.INPUT_SIGNAL.setText(_translate("MainWindow", "12A"))
        self.label_18.setText(_translate("MainWindow", "DERAILEUR :"))
        self.CHECK_DERAILEUR_TURUN.setText(_translate("MainWindow", "DERAILEUR TURUN"))
        self.CHECK_DERAILEUR_NAIK.setText(_translate("MainWindow", "DERAILEUR NAIK"))
        self.INPUT_DERAILEUR.setText(_translate("MainWindow", "162"))
        self.label_17.setText(_translate("MainWindow", "UTILITY  :"))
        self.CHECK_INVERTER_FAIL.setText(_translate("MainWindow", "INVERTER FAIL"))
        self.CHECK_VDR.setText(_translate("MainWindow", "VDR"))
        self.CHECK_GENSET.setText(_translate("MainWindow", "GENSET"))
        self.CHECK_BBM_HABIS.setText(_translate("MainWindow", "BBM HABIS"))
        self.CHECK_UPS_LOWBAT.setText(_translate("MainWindow", "UPS LOWBAT"))
        self.CHECK_UPS.setText(_translate("MainWindow", "UPS"))
        self.CHECK_GAGAL_START.setText(_translate("MainWindow", "GAGAL START"))
        self.CHECK_PLN.setText(_translate("MainWindow", "PLN"))
        self.UPDATE_POINT_PB_DI.setText(_translate("MainWindow", "UPDATE"))
        self.UPDATE_DERAILEUR_PB_DI.setText(_translate("MainWindow", "UPDATE"))
        self.UPDATE_SIGNAL_PB_DI.setText(_translate("MainWindow", "UPDATE"))
        self.UPDATE_UTILITY_PB_DI.setText(_translate("MainWindow", "UPDATE"))
        self.START_MODBUS_PB_DI.setText(_translate("MainWindow", "START MODBUS"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Information"))
        self.IT_Directory.setText(defaultITDir)
        self.VDU_CTRL_Directory.setText(defaultVDUDir)

    ############################################### Configuration Function #############################################
    def searchITdir(self):
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                  "", "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
        if check:
            self.IT_Directory.setText(file)
    def searchVDUdir(self):
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                  "", "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
        if check:
            self.VDU_CTRL_Directory.setText(file)
    def generate(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        # get data from Form input (IT and generator Input)
        # IT1, IT2, RUTE, SIGNAL, PM, TRACK, BLOK, JPL
        self.IT1, self.IT2, self.RUTE, self.SIGNAL, self.PM, self.TRACK, self.BLOK, self.JPL = data.ITdata(self.IT_Directory.text())
        # generate variable for register on modbus
        self.inputData, self.outputData, self.internalData = data.genVar(self.RUTE, self.SIGNAL, self.PM, self.TRACK, self.BLOK, self.JPL)

        self.pbStart = int(self.VDU_CTRL_Start.text())
        self.simCtrlStart = int(self.Field_CTRL_Start.text())
        self.simINDStart = int(self.Field_IND_Start.text())

        # generate variable with address register on modbus for input hima
        self.simCtrlData = data.genCSVData(self.simCtrlStart, self.inputData, '0_MODBUS_FROM_TESTERBOT_SIM_REG')
        self.simINDData = data.genCSVData(self.simINDStart, self.outputData, '0_MODBUS_TO_0_MODBUS_FROM_TESTERBOT_SIM_REG_REG')

        file, check = QFileDialog.getSaveFileName(None, "QFileDialog getSaveFileName() Demo",
                                                  "18. PROTOCOL - FROM FIELD SIMULATOR.csv", "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
        if check:
            dfFI = pd.DataFrame(self.simCtrlData[1:], columns=self.simCtrlData[0])
            dfFI.to_csv(file, sep=',',index=False)

        file, check = QFileDialog.getSaveFileName(None, "QFileDialog getSaveFileName() Demo",
                                                  "19. PROTOCOL - TO FIELD SIMULATOR.csv", "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
        if check:
            dfFO = pd.DataFrame(self.simINDData[1:], columns=self.simINDData[0])
            dfFO.to_csv(file, sep=',',index=False)

        QApplication.restoreOverrideCursor()
        self.START_MODBUS_PB_DI.setDisabled(False)
        self.CHECK_DATA_PB_DI.setDisabled(False)

    ################################################### Testing Function ###############################################
    def startModbus(self):
        pbData = data.readVDUCTRL(self.VDU_CTRL_Directory.text())
        dataSIM = data.genModbusData(self.simCtrlData, self.simINDData, self.internalData)

        self.modbus.startRun(self.IP_HIMA.text(), pbData, self.pbStart, dataSIM)
        self.Information.setText("Modbus is now running")

        self.TWT_ALL_PB_DI.setDisabled(False)
        self.TPR_BANTU_PB_DI.setDisabled(False)
        self.THB_PB_DI.setDisabled(False)
        self.LAMPTEST_PB_DI.setDisabled(False)
        self.STOP_TEST_PB_DI.setDisabled(False)
        self.CHECK_DATA_PB_DI.setDisabled(False)

        self.INPUT_TRACK.setDisabled(False)
        self.TRACK_OCCUPIED_PB_DI.setDisabled(False)
        self.TRACK_CLEAR_PB_DI.setDisabled(False)
        self.CLEAR_ALLTRACK_PB_DI.setDisabled(False)
        self.OCCUPIED_ALLTRACK_PB_DI.setDisabled(False)

        self.INPUT_POINT.setDisabled(False)
        self.UPDATE_POINT_PB_DI.setDisabled(False)
        self.CHECK_ENGKOL_NORMAL.setDisabled(False)
        self.CHECK_ENGKOL_REVERSE.setDisabled(False)
        self.CHECK_GANJAL_NORMAL.setDisabled(False)
        self.CHECK_GANJAL_REVERSE.setDisabled(False)
        self.CHECK_HILANG_DETEKSI.setDisabled(False)

        self.INPUT_DERAILEUR.setDisabled(False)
        self.UPDATE_DERAILEUR_PB_DI.setDisabled(False)
        self.CHECK_DERAILEUR_NAIK.setDisabled(False)
        self.CHECK_DERAILEUR_TURUN.setDisabled(False)

        self.INPUT_SIGNAL.setDisabled(False)
        self.UPDATE_SIGNAL_PB_DI.setDisabled(False)
        self.CHECK_ECR_R.setDisabled(False)
        self.CHECK_ECR_Y.setDisabled(False)
        self.CHECK_ECR_G.setDisabled(False)
        self.CHECK_EKR.setDisabled(False)
        self.CHECK_DKR.setDisabled(False)
        self.CHECK_SECR.setDisabled(False)

        self.UPDATE_UTILITY_PB_DI.setDisabled(False)
        self.CHECK_VDR.setDisabled(False)
        self.CHECK_PLN.setDisabled(False)
        self.CHECK_UPS.setDisabled(False)
        self.CHECK_GENSET.setDisabled(False)
        self.CHECK_UPS_LOWBAT.setDisabled(False)
        self.CHECK_INVERTER_FAIL.setDisabled(False)
        self.CHECK_GAGAL_START.setDisabled(False)
        self.CHECK_BBM_HABIS.setDisabled(False)

        self.Fucntional_Test_list.setDisabled(False)
        self.FunctionalTest.setDisabled(False)
        self.InterlockingTableTest.setDisabled(False)
        self.ConflictRouteTest.setDisabled(False)
        self.VisualTest.setDisabled(False)
        self.DeepTest.setDisabled(False)

        self.Start_Route.setDisabled(False)
        self.Finish_Route.setDisabled(False)

        self.StartTesting.setDisabled(False)

        self.twtAll()

    def twtAll(self):
        self.modbus.writePBVDU('TWT-PB-DI')
        for w in self.PM:
            self.modbus.writePBVDU(w[0] + '-PB-DI')
    def tprBantu(self):
        self.modbus.writePBVDU('TPR-BANTU-PB-DI')
    def thbPBDI(self):
        self.modbus.writePBVDU('THB-PB-DI')
    def lamptestPBDI(self):
        self.modbus.writePBVDU('LAMPTEST-PB-DI')
    def forceStopTest(self):
        self.testingBot.stopTesting()
    def cekData(self):
        error = ""
        allSignal = [signal[0].strip() for signal in self.RUTE] + [signal[1].strip() for signal in self.RUTE] + [signal[0].strip() for signal in self.SIGNAL]
        allWesel = [wesel[0].strip() for wesel in self.PM]
        allTrack = [track[0].strip() for track in self.TRACK]
        allRute = [(rute[0].strip() + '-' + rute[1].strip()) for rute in self.RUTE]

        for it in self.IT1:
            if it[2] and it[2] not in allSignal:
                error += "Signal \"" + it[2] + "\" di rute " + it[0] + ": " + it[1] + " kolom Start Signal" + " IT1 tidak sesuai \n"
            if it[12] and it[12] not in allSignal:
                error += "Signal \"" + it[12] + "\" di rute " + it[0] + ": " + it[1] + " kolom Distant Signal" + " IT1 tidak sesuai \n"
            if it[15] and it[15] not in allSignal:
                error += "Signal \"" + it[15] + "\" di rute " + it[0] + ": " + it[1] + " kolom Destination Signal" + " IT1 tidak sesuai \n"
            for signal in it[21].split(" "):
                if signal and signal not in allSignal:
                    error += "Signal \"" + signal + "\" di rute " + it[0] + ": " + it[1] + " kolom Shunt Signal Clear" + "  IT1 tidak sesuai \n"
            for signal in it[22].split(" "):
                if signal and signal not in allSignal:
                    error += "Signal \"" + signal + "\" di rute " + it[0] + ": " + it[1] + " kolom Opposing Signal Locked" + " IT1 tidak sesuai \n"

            for wesel in it[18].split(" "):
                if wesel and 'W' + wesel.replace('-R', '').replace('-N', '') not in allWesel:
                    error += "Wesel \"" + wesel + "\" di rute " + it[0] + ": " + it[1] + " kolom Point Locked" + " IT1 tidak sesuai \n"

            for track in it[20].split(" "):
                if track and track.replace('T', '').replace('t', '') not in allTrack:
                    error += "Track \"" + track + "\" di rute " + it[0] + ": " + it[1] + " kolom Track Circuit Clear" + " IT1 tidak sesuai \n"
            for track in it[23].split(" "):
                if track and track.replace('T', '').replace('t', '') not in allTrack:
                    error += "Track \"" + track + "\" di rute " + it[0] + ": " + it[1] + " kolom Approach Clear" + " IT1 tidak sesuai \n"

            if it[2].strip() + '-' + it[15].strip() not in allRute:
                error += "Rute \"" + it[2].strip() + '-' + it[15].strip() + "\" di rute " + it[0] + ": " + it[1] + " IT1 tidak ada \n"

            for deraileur in it[19].split(" "):
                if deraileur[0] == 'D' or deraileur[0] == 'R' and deraileur.replace('R','D') not in allWesel:
                    error += "Deraileur \"" + deraileur + "\" di rute " + it[0] + ": " + it[1] + " kolom Key Detect" + " IT1 tidak sesuai \n"

        for it in self.IT2:
            if it[2] and it[2] not in allSignal:
                error += "Signal \"" + it[2] + "\" di rute " + it[0] + ": " + it[1] + " kolom Start Signal" + " IT2 tidak sesuai \n"
            for signal in it[4].split(" "):
                if signal and signal not in allSignal:
                    error += "Signal \"" + signal + "\" di rute " + it[0] + ": " + it[1] + " kolom Signal Locked and Proved at Danger" + " IT2 tidak sesuai \n"
            if it[6] and it[6] not in allSignal:
                error += "Signal \"" + it[6] + "\" di rute " + it[0] + ": " + it[1] + " kolom Destination Signal" + " IT2 tidak sesuai \n"
            for signal in it[6].split(" "):
                if signal and signal not in allSignal:
                    error += "Signal \"" + signal + "\" di rute " + it[0] + ": " + it[1] + " kolom Opposing Signal Locked" + " IT2 tidak sesuai \n"
            for signal in it[12].split(" "):
                if signal and signal not in allSignal:
                    error += "Signal \"" + signal + "\" di rute " + it[0] + ": " + it[1] + " kolom Signal Locked & Proved at Danger" + " IT2 tidak sesuai \n"

            for wesel in it[3].split(" "):
                if wesel and 'W' + wesel.replace('-R', '').replace('-N', '') not in allWesel:
                    error += "Wesel \"" + wesel + "\" di rute " + it[0] + ": " + it[1] + " kolom Route Point Flank Locked" + " IT12 tidak sesuai \n"
            for wesel in it[7].split(" "):
                if wesel and 'W' + wesel.replace('-R', '').replace('-N', '') not in allWesel:
                    error += "Wesel \"" + wesel + "\" di rute " + it[0] + ": " + it[1] + " kolom Overlap Point Locked" + " IT12 tidak sesuai \n"
            for wesel in it[11].split(" "):
                if wesel and 'W' + wesel.replace('-R', '').replace('-N', '') not in allWesel:
                    error += "Wesel \"" + wesel + "\" di rute " + it[0] + ": " + it[1] + " kolom Overlap Route Point Flank Locked" + " IT12 tidak sesuai \n"

            for track in it[5].split(" "):
                if track and track.replace('T', '').replace('t', '') not in allTrack:
                    error += "Track \"" + track + "\" di rute " + it[0] + ": " + it[1] + " kolom Rute Track Flank" + " IT2 tidak sesuai \n"
            for track in it[9].split(" "):
                if track and track.replace('T', '').replace('t', '') not in allTrack:
                    error += "Track \"" + track + "\" di rute " + it[0] + ": " + it[1] + " kolom Overlap Track Clear" + " IT2 tidak sesuai \n"
            for track in it[13].split(" "):
                if track and track.replace('T', '').replace('t', '') not in allTrack:
                    error += "Track \"" + track + "\" di rute " + it[0] + ": " + it[1] + " kolom Overlap Track Flank Clear" + " IT2 tidak sesuai \n"

        self.show_popup("Cek Data", error)


    def clearTrack(self):
        self.modbus.writeField(self.INPUT_TRACK.text() + '-TPR-DI', 1)
    def occTrack(self):
        self.modbus.writeField(self.INPUT_TRACK.text() + '-TPR-DI', 0)
    def clearAllTrack(self):
        # clearkan semua track sebelum pengetesan
        for track in self.TRACK:
            self.modbus.writeField(track[0] + '-TPR-DI', 1)
    def occAllTrack(self):
        # clearkan semua track sebelum pengetesan
        for track in self.TRACK:
            self.modbus.writeField(track[0] + '-TPR-DI', 0)

    def updatePoint(self):
        pass
    def updateDeraileur(self):
        if self.CHECK_DERAILEUR_NAIK.isChecked():
            self.modbus.writeField('D' + self.INPUT_DERAILEUR.text() + '-NKR-DI', 1)
        if not self.CHECK_DERAILEUR_NAIK.isChecked():
            self.modbus.writeField('D' + self.INPUT_DERAILEUR.text() + '-NKR-DI', 0)
        if self.CHECK_DERAILEUR_TURUN.isChecked():
            self.modbus.writeField('D' + self.INPUT_DERAILEUR.text() + '-RKR-DI', 1)
        if not self.CHECK_DERAILEUR_TURUN.isChecked():
            self.modbus.writeField('D' + self.INPUT_DERAILEUR.text() + '-RKR-DI', 0)
    def updateSignal(self):
        pass
    def updateUtility(self):
        pass

    ################################################### Testing Function ###############################################
    def ConflictRouteChangeCheck(self):
        if self.ConflictRouteTest.isChecked():
            self.Start_Route_2.setDisabled(False)
            self.Finish_Route_2.setDisabled(False)
        else:
            self.Start_Route_2.setDisabled(True)
            self.Finish_Route_2.setDisabled(True)

    def startTest(self):
        # 0:FT | 1:IT | 2:CR | 3:VT | 4:DT
        FT = (self.Fucntional_Test_list.currentIndex() + 1) * self.FunctionalTest.isChecked()
        IT = self.InterlockingTableTest.isChecked()
        CR = self.ConflictRouteTest.isChecked()
        VT = self.VisualTest.isChecked()
        DT = self.DeepTest.isChecked()
        self.testingBot.addonData(data.forTest(self.IT1, self.IT2, self.RUTE, self.SIGNAL, self.PM, self.TRACK, self.BLOK, self.JPL, self.inputData, self.outputData, self.internalData))
        self.testingBot.startRun(self.IT1, self.IT2, [FT, IT, CR, VT, DT], self.Start_Route.text(), self.Finish_Route.text(), self.Start_Route_2.text(), self.Finish_Route_2.text())

    def show_popup(self, title="tes", text = "Noting"):
            msg = QMessageBox()
            msg.setWindowTitle("Information Detail")
            if text != "":
                msg.setText("temuan penulisan IT => cek detail untuk informasi lebih detail")
            else:
                msg.setText("tidak terdapat temuan pada penulisan IT")

            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)
            msg.setDetailedText(text)
            x = msg.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
