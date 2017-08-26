# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'graph.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1500, 900)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.menu = QtGui.QWidget(self.centralwidget)
        self.menu.setGeometry(QtCore.QRect(10, 10, 251, 831))
        self.menu.setObjectName(_fromUtf8("menu"))
        self.pushButton_edit = QtGui.QPushButton(self.menu)
        self.pushButton_edit.setGeometry(QtCore.QRect(10, 536, 221, 51))
        self.pushButton_edit.setObjectName(_fromUtf8("pushButton_edit"))
        self.pushButton_delete = QtGui.QPushButton(self.menu)
        self.pushButton_delete.setGeometry(QtCore.QRect(10, 596, 221, 51))
        self.pushButton_delete.setObjectName(_fromUtf8("pushButton_delete"))
        self.pushButton_add = QtGui.QPushButton(self.menu)
        self.pushButton_add.setGeometry(QtCore.QRect(10, 476, 221, 51))
        self.pushButton_add.setObjectName(_fromUtf8("pushButton_add"))
        self.comboBox_type = QtGui.QComboBox(self.menu)
        self.comboBox_type.setGeometry(QtCore.QRect(10, 30, 221, 51))
        self.comboBox_type.setObjectName(_fromUtf8("comboBox_type"))
        self.comboBox_type.addItem(_fromUtf8(""))
        self.comboBox_type.addItem(_fromUtf8(""))
        self.comboBox_type.addItem(_fromUtf8(""))
        self.label = QtGui.QLabel(self.menu)
        self.label.setGeometry(QtCore.QRect(100, 390, 68, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit_value = QtGui.QLineEdit(self.menu)
        self.lineEdit_value.setGeometry(QtCore.QRect(20, 346, 211, 41))
        self.lineEdit_value.setObjectName(_fromUtf8("lineEdit_value"))
        self.label_2 = QtGui.QLabel(self.menu)
        self.label_2.setGeometry(QtCore.QRect(90, 320, 68, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pushButton_save = QtGui.QPushButton(self.menu)
        self.pushButton_save.setGeometry(QtCore.QRect(10, 746, 221, 61))
        self.pushButton_save.setObjectName(_fromUtf8("pushButton_save"))
        self.label_3 = QtGui.QLabel(self.menu)
        self.label_3.setGeometry(QtCore.QRect(40, 670, 161, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit_filename = QtGui.QLineEdit(self.menu)
        self.lineEdit_filename.setGeometry(QtCore.QRect(10, 700, 221, 41))
        self.lineEdit_filename.setObjectName(_fromUtf8("lineEdit_filename"))
        self.label_4 = QtGui.QLabel(self.menu)
        self.label_4.setGeometry(QtCore.QRect(100, 10, 68, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.comboBox_node_type = QtGui.QComboBox(self.menu)
        self.comboBox_node_type.setGeometry(QtCore.QRect(10, 410, 221, 51))
        self.comboBox_node_type.setObjectName(_fromUtf8("comboBox_node_type"))
        self.comboBox_node_type.addItem(_fromUtf8(""))
        self.comboBox_node_type.addItem(_fromUtf8(""))
        self.comboBox_node_type.addItem(_fromUtf8(""))
        self.canvas = QtGui.QWidget(self.centralwidget)
        self.canvas.setGeometry(QtCore.QRect(270, 10, 1221, 831))
        self.canvas.setObjectName(_fromUtf8("canvas"))
        self.label_5 = QtGui.QLabel(self.canvas)
        self.label_5.setGeometry(QtCore.QRect(430, 10, 68, 17))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_edit.setText(_translate("MainWindow", "Editar", None))
        self.pushButton_delete.setText(_translate("MainWindow", "Borrar", None))
        self.pushButton_add.setText(_translate("MainWindow", "Agregar", None))
        self.comboBox_type.setItemText(0, _translate("MainWindow", "DFA", None))
        self.comboBox_type.setItemText(1, _translate("MainWindow", "NFA", None))
        self.comboBox_type.setItemText(2, _translate("MainWindow", "NFA EPSILON", None))
        self.label.setText(_translate("MainWindow", "Tipo", None))
        self.label_2.setText(_translate("MainWindow", "Valor", None))
        self.pushButton_save.setText(_translate("MainWindow", "Guardar", None))
        self.label_3.setText(_translate("MainWindow", " Nombre del Archivo", None))
        self.label_4.setText(_translate("MainWindow", "Menu", None))
        self.comboBox_node_type.setItemText(0, _translate("MainWindow", "START", None))
        self.comboBox_node_type.setItemText(1, _translate("MainWindow", "NORMAL", None))
        self.comboBox_node_type.setItemText(2, _translate("MainWindow", "FINAL", None))
        self.label_5.setText(_translate("MainWindow", "Canvas", None))

