# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui
from device import DeviceMgr
from recorder import Recorder

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


def signal(s):
    return QtCore.SIGNAL(_fromUtf8(s))


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
        self.deviceList = QtGui.QListWidget(self)
        self.deviceList.setObjectName(_fromUtf8("deviceList"))
        self.connectButton = QtGui.QPushButton(_fromUtf8("连接"), self)
        self.connectButton.setObjectName(_fromUtf8("connectButton"))
        self.deviceListLayout = QtGui.QHBoxLayout()
        self.deviceListLayout.setObjectName(_fromUtf8("deviceListLayout"))
        self.deviceListLayout.addWidget(self.deviceList)
        self.deviceListLayout.addWidget(self.connectButton)

        self.deviceIdLabel = QtGui.QLabel(_fromUtf8("deviceId: "), self)
        self.deviceIdLabel.setObjectName(_fromUtf8("deviceIdLabel"))
        self.deviceIdVal = QtGui.QLabel(_fromUtf8("deviceId"), self)
        self.deviceIdVal.setObjectName(_fromUtf8("deviceIdVal"))
        self.infoLayout = QtGui.QVBoxLayout()
        self.infoLayout.setObjectName(_fromUtf8("infoLayout"))
        self.infoLayout.addWidget(self.deviceIdLabel)
        self.infoLayout.addWidget(self.deviceIdVal)

        self.ctrlButton = QtGui.QPushButton(_fromUtf8("开始"), self)
        self.stopButton = QtGui.QPushButton(_fromUtf8("结束"), self)
        self.saveButton = QtGui.QPushButton(_fromUtf8("保存"), self)
        self.replayButton = QtGui.QPushButton(_fromUtf8("回放"), self)
        self.ctrlLayput = QtGui.QVBoxLayout()
        self.ctrlLayput.addWidget(self.ctrlButton)
        self.ctrlLayput.addWidget(self.stopButton)
        self.ctrlLayput.addWidget(self.saveButton)
        self.ctrlLayput.addWidget(self.replayButton)

        self.deviceLayout = QtGui.QHBoxLayout()
        self.deviceLayout.setObjectName(_fromUtf8("deviceLayout"))
        self.deviceLayout.addLayout(self.infoLayout)
        self.deviceLayout.addLayout(self.ctrlLayput)

        self.ipLabel = QtGui.QLabel(_fromUtf8("IP: "), self)
        self.ipLabel.setObjectName(_fromUtf8("ipLabel"))
        self.ipEdit = QtGui.QLineEdit()
        self.ipEdit.setObjectName(_fromUtf8("ipEdit"))
        self.colonLabel = QtGui.QLabel(_fromUtf8(":"), self)
        self.colonLabel.setObjectName(_fromUtf8("colonLabel"))
        self.portEdit = QtGui.QLineEdit()
        self.portEdit.setObjectName(_fromUtf8("portEdit"))
        self.addButton = QtGui.QPushButton(_fromUtf8("添加"), self)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.ipLayout = QtGui.QHBoxLayout()
        self.ipLayout.setObjectName(_fromUtf8("ipLayout"))
        self.ipLayout.addWidget(self.ipLabel)
        self.ipLayout.addWidget(self.ipEdit)
        self.ipLayout.addWidget(self.colonLabel)
        self.ipLayout.addWidget(self.portEdit)
        self.ipLayout.addWidget(self.addButton)

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setObjectName(_fromUtf8("layout"))
        self.layout.addLayout(self.deviceLayout)
        self.layout.addLayout(self.deviceListLayout)
        self.layout.addLayout(self.ipLayout)

        self.connectSignal()
        self.initDevices()
        self.initRecorder()

    def connectSignal(self):
        connect = QtCore.QObject.connect
        connect(self.addButton, signal("clicked()"), self.addDevice)
        connect(self.connectButton, signal("clicked()"), self.connectDevice)
        connect(self.ctrlButton, signal("clicked()"), self.startRecord)
        connect(self.stopButton, signal("clicked()"), self.stopRecord)

    def initDevices(self):
        self.deviceMgr = DeviceMgr()
        self.deviceMgr.initDevices()
        for device in self.deviceMgr.getAllDevices():
            self.insertDevice(device)

    def initRecorder(self):
        self.recorder = Recorder()

    def addDevice(self):
        ip = str(self.ipEdit.text())
        port = int(self.portEdit.text())
        device = self.deviceMgr.addDevice(ip, port)
        self.insertDevice(device)

    def insertDevice(self, device):
        self.deviceList.addItem(QtGui.QListWidgetItem(
            _fromUtf8(device.deviceId or "%s:%d" % device.deviceIp)))

    def connectDevice(self):
        item = self.deviceList.selectedItems()[0]
        deviceId = str(item.text())
        device = self.deviceMgr.findDeviceById(deviceId) \
            or self.deviceMgr.findDeviceByIp(deviceId)
        result = True if device.deviceId else device.connect()
        if result:
            print(device.getDeviceEvent())
            print(device.getDeviceResolution())
            self.recorder.setDevice(device)
        else:
            print("can not connect")

    def startRecord(self):
        self.recorder.start()

    def stopRecord(self):
        self.recorder.stop()
        print(self.recorder.minitouchEvents)


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
