# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chargenerator.ui'
#
# Created: Tue Oct  2 21:05:25 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(685, 581)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 50, 51, 17))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.name_field = QtGui.QLineEdit(self.centralwidget)
        self.name_field.setGeometry(QtCore.QRect(90, 40, 161, 25))
        self.name_field.setObjectName(_fromUtf8("name_field"))
        self.spritesheet_view = QtGui.QGraphicsView(self.centralwidget)
        self.spritesheet_view.setGeometry(QtCore.QRect(380, 50, 281, 361))
        self.spritesheet_view.setObjectName(_fromUtf8("spritesheet_view"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(460, 20, 121, 20))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Spritesheet View", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 100, 91, 17))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Spritesheet:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.spritesheet_open_button = QtGui.QPushButton(self.centralwidget)
        self.spritesheet_open_button.setGeometry(QtCore.QRect(90, 90, 51, 27))
        self.spritesheet_open_button.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.spritesheet_open_button.setObjectName(_fromUtf8("spritesheet_open_button"))
        self.spritesheet_open_field = QtGui.QLineEdit(self.centralwidget)
        self.spritesheet_open_field.setGeometry(QtCore.QRect(160, 90, 181, 25))
        self.spritesheet_open_field.setObjectName(_fromUtf8("spritesheet_open_field"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 150, 91, 17))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Walk Speed:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.walkspeed_field = QtGui.QLineEdit(self.centralwidget)
        self.walkspeed_field.setGeometry(QtCore.QRect(120, 140, 113, 25))
        self.walkspeed_field.setObjectName(_fromUtf8("walkspeed_field"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 200, 91, 17))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Back Speed:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.backspeed_field = QtGui.QLineEdit(self.centralwidget)
        self.backspeed_field.setGeometry(QtCore.QRect(120, 190, 113, 25))
        self.backspeed_field.setObjectName(_fromUtf8("backspeed_field"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 250, 91, 17))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Jump Height:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.jumpheight_field = QtGui.QLineEdit(self.centralwidget)
        self.jumpheight_field.setGeometry(QtCore.QRect(120, 240, 113, 25))
        self.jumpheight_field.setObjectName(_fromUtf8("jumpheight_field"))
        self.moves_button = QtGui.QPushButton(self.centralwidget)
        self.moves_button.setGeometry(QtCore.QRect(20, 340, 151, 41))
        self.moves_button.setText(QtGui.QApplication.translate("MainWindow", "Add/Edit/View Moves", None, QtGui.QApplication.UnicodeUTF8))
        self.moves_button.setObjectName(_fromUtf8("moves_button"))
        self.generate_button = QtGui.QPushButton(self.centralwidget)
        self.generate_button.setGeometry(QtCore.QRect(20, 400, 151, 41))
        self.generate_button.setText(QtGui.QApplication.translate("MainWindow", "Generate Character", None, QtGui.QApplication.UnicodeUTF8))
        self.generate_button.setObjectName(_fromUtf8("generate_button"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 685, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setObjectName(_fromUtf8("menu_File"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_Open = QtGui.QAction(MainWindow)
        self.action_Open.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open.setObjectName(_fromUtf8("action_Open"))
        self.action_Save_As = QtGui.QAction(MainWindow)
        self.action_Save_As.setText(QtGui.QApplication.translate("MainWindow", "Save &As", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save_As.setObjectName(_fromUtf8("action_Save_As"))
        self.action_Save = QtGui.QAction(MainWindow)
        self.action_Save.setText(QtGui.QApplication.translate("MainWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setObjectName(_fromUtf8("action_Save"))
        self.action_New = QtGui.QAction(MainWindow)
        self.action_New.setText(QtGui.QApplication.translate("MainWindow", "&New", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New.setObjectName(_fromUtf8("action_New"))
        self.menu_File.addAction(self.action_New)
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.action_Save_As)
        self.menu_File.addAction(self.action_Save)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.name_field, self.spritesheet_open_button)
        MainWindow.setTabOrder(self.spritesheet_open_button, self.spritesheet_open_field)
        MainWindow.setTabOrder(self.spritesheet_open_field, self.walkspeed_field)
        MainWindow.setTabOrder(self.walkspeed_field, self.backspeed_field)
        MainWindow.setTabOrder(self.backspeed_field, self.jumpheight_field)
        MainWindow.setTabOrder(self.jumpheight_field, self.moves_button)
        MainWindow.setTabOrder(self.moves_button, self.spritesheet_view)

    def retranslateUi(self, MainWindow):
        pass

