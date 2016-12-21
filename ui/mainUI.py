# -*- coding: utf-8 -*-
import sys
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
        MainWindow.resize(640, 480)
        MainWindow.setWindowFlags(
                QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralwidget"))
        MainWindow.setCentralWidget(self.centralWidget)

        self.navigationWidget = QtGui.QWidget(self.centralWidget)
        self.navigationWidget.setObjectName(_fromUtf8("navigationWidget"))
        self.navigationWidget.setGeometry(QtCore.QRect(0, 0, 100, 480))

        self.navigationLayout = QtGui.QHBoxLayout(self.navigationWidget)
        self.navigationLayout.setObjectName(_fromUtf8("navigationLayout"))

        self.navigation = QNavigation(MainWindow)
        self.navigation.setObjectName(_fromUtf8("navigation"))
        self.navigation.addEntry("设备", self.switch2DevicePage)
        self.navigation.addEntry("脚本", self.switch2ScriptPage)
        self.navigationLayout.addWidget(self.navigation)

        contextRect = QtCore.QRect(105, 0, 530, 480)
        self.deviceWidget = DeviceWidget(self.centralWidget)
        self.deviceWidget.setGeometry(contextRect)
        self.scriptWidget = ScriptWidget(self.centralWidget)
        self.scriptWidget.setGeometry(contextRect)
        self.scriptWidget.hide()

    def switch2DevicePage(self):
        self.scriptWidget.hide()
        self.deviceWidget.show()

    def switch2ScriptPage(self):
        self.deviceWidget.hide()
        self.scriptWidget.show()


class QNavigation(QtGui.QListWidget):
    def __init__(self, parent=None):
        super(QNavigation, self).__init__(parent)
        QtCore.QObject.connect(
                self,
                QtCore.SIGNAL(_fromUtf8("itemSelectionChanged()")),
                self.callEntry)

    def addEntry(self, entryName, entryCall=None):
        entry = QtGui.QListWidgetItem(_fromUtf8(entryName))
        entry.call = entryCall
        self.addItem(entry)

    def callEntry(self):
        entry = self.selectedItems()[0]
        if entry.call:
            entry.call()


class DeviceWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(DeviceWidget, self).__init__(parent)
        self.deviceLayout = QtGui.QHBoxLayout(self)
        self.deviceList = QtGui.QListWidget(self)
        self.deviceList.setObjectName(_fromUtf8("deviceList"))
        self.deviceList.addItem(QtGui.QListWidgetItem(_fromUtf8("test")))
        self.deviceLayout.addWidget(self.deviceList)


class ScriptWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ScriptWidget, self).__init__(parent)
        self.scriptLayout = QtGui.QHBoxLayout(self)

        self.scriptWidget = QtGui.QListWidget(self)
        self.scriptWidget.setObjectName(_fromUtf8("scriptWidget"))
        self.scriptLayout.addWidget(self.scriptWidget)

        self.dirWidget = QtGui.QWidget(self)
        self.dirWidget.setObjectName(_fromUtf8("dirWidget"))
        self.dirWidget.setGeometry(QtCore.QRect(20, 190, 340, 220))

        self.dirLayout = QtGui.QVBoxLayout(self.dirWidget)
        self.fileListWidget = QtGui.QListWidget(self.dirWidget)
        self.fileListWidget.setObjectName(_fromUtf8("fileListWidget"))
        self.dirLayout.addWidget(self.fileListWidget)

        self.dirChooseLayout = QtGui.QHBoxLayout()
        self.dirChooseLayout.setObjectName(_fromUtf8("dirChooseLayout"))
        self.dirPushButton = QtGui.QPushButton(self.dirWidget)
        self.dirPushButton.setObjectName(_fromUtf8("dirPushButton"))
        self.dirChooseLayout.addWidget(self.dirPushButton)
        self.dirLineEdit = QtGui.QLineEdit(self.dirWidget)
        self.dirLineEdit.setObjectName(_fromUtf8("dirLineEdit"))
        self.dirChooseLayout.addWidget(self.dirLineEdit)
        self.dirLayout.addLayout(self.dirChooseLayout)


def run():
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
