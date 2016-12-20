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

        self.deviceWidget = DeviceWidget(self.centralWidget)
        self.deviceWidget.setGeometry(QtCore.QRect(105, 0, 530, 480))
        self.scriptWidget = ScriptWidget(self.centralWidget)
        self.scriptWidget.setGeometry(QtCore.QRect(105, 0, 530, 480))

        #  self.contextWidget = QtGui.QWidget(self.centralWidget)
        #  self.contextWidget.setObjectName(_fromUtf8("contextWidget"))
        #  self.contextWidget.setGeometry(QtCore.QRect(200, 0, 100, 480))

        #  self.contextLayout = QtGui.QHBoxLayout(self.contextWidget)
        #  self.contextLayout.setObjectName(_fromUtf8("contextLayout"))
        #  self.contextLayout.setMargin(0)

        #  self.deviceWidget = DeviceWidget(self.contextWidget)
        #  self.scriptWidget = ScriptWidget(self.contextWidget)
        #  self.scriptWidget.hide()
        #  self.contextLayout.addWidget(self.deviceWidget)
        #  self.contextLayout.addWidget(self.scriptWidget)

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


def run():
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
