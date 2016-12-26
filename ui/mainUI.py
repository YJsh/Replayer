# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtCore, QtGui
from device import DeviceMgr
from recorder import Recorder
from replayer import Replayer

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

connect = QtCore.QObject.connect
disconnect = QtCore.QObject.disconnect
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
        self.deviceMgr = DeviceMgr()
        self.deviceWidget = DeviceWidget(self.deviceMgr, self.centralWidget)
        self.deviceWidget.setGeometry(contextRect)
        self.scriptWidget = ScriptWidget(self.deviceMgr, self.centralWidget)
        self.scriptWidget.setGeometry(contextRect)
        self.scriptWidget.hide()

    def switch2DevicePage(self):
        self.scriptWidget.hide()
        self.deviceWidget.show()

    def switch2ScriptPage(self):
        self.deviceWidget.hide()
        self.scriptWidget.show()
        self.scriptWidget.refresh()


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

    def __init__(self, deviceMgr, parent=None):
        super(DeviceWidget, self).__init__(parent)
        self.deviceMgr = deviceMgr
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
        self.stopButton.setEnabled(False)
        self.saveButton = QtGui.QPushButton(_fromUtf8("保存"), self)
        self.saveButton.setEnabled(False)
        self.replayButton = QtGui.QPushButton(_fromUtf8("回放"), self)
        self.replayButton.setEnabled(False)
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

    def connectSignal(self):
        connect(self.addButton, signal("clicked()"), self.addDevice)
        connect(self.connectButton, signal("clicked()"), self.connectDevice)
        connect(self.ctrlButton, signal("clicked()"), self.doStart)
        connect(self.stopButton, signal("clicked()"), self.doStop)
        connect(self.saveButton, signal("clicked()"), self.doSave)
        connect(self.replayButton, signal("clicked()"), self.doReplay)

    def initDevices(self):
        self.deviceMgr.initDevices()
        for device in self.deviceMgr.getAllDevices():
            self.insertDevice(device)

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
            self.device = device
        else:
            print("can not connect")

    def doStart(self):
        self.replayButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        if not self.device:
            return
        self.recorder = Recorder(self.device)
        self.ctrlButton.setText(_translate("MainWindow", "暂停", None))
        disconnect(self.ctrlButton, signal("clicked()"), self.doStart)
        connect(self.ctrlButton, signal("clicked()"), self.doPause)
        self.recorder.start()
        self.stopButton.setEnabled(True)

    def doPause(self):
        self.ctrlButton.setText(_translate("MainWindow", "继续", None))
        disconnect(self.ctrlButton, signal("clicked()"), self.doPause)
        connect(self.ctrlButton, signal("clicked()"), self.doContinue)
        self.recorder.changeStatus()

    def doContinue(self):
        self.ctrlButton.setText(_translate("MainWindow", "暂停", None))
        disconnect(self.ctrlButton, signal("clicked()"), self.doContinue)
        connect(self.ctrlButton, signal("clicked()"), self.doPause)
        self.recorder.changeStatus()

    def doStop(self):
        self.stopButton.setEnabled(False)
        self.ctrlButton.setText(_translate("MainWindow", "开始", None))
        disconnect(self.ctrlButton, signal("clicked()"), self.doContinue)
        disconnect(self.ctrlButton, signal("clicked()"), self.doPause)
        connect(self.ctrlButton, signal("clicked()"), self.doStart)
        self.recorder.stop()
        self.events = self.recorder.getMinitouchEvents()
        print(self.events)
        self.saveButton.setEnabled(True)
        self.replayButton.setEnabled(True)

    def doSave(self):
        if not self.events:
            return
        fileName = QtGui.QFileDialog.getSaveFileName(filter=".script")
        if fileName:
            with open(str(fileName), "w") as f:
                f.write("".join(self.events))

    def doReplay(self):
        self.replayer = Replayer(self.events, self.device)
        self.replayer.start()


class ScriptWidget(QtGui.QWidget):

    def __init__(self, deviceMgr, parent=None):
        super(ScriptWidget, self).__init__(parent)
        self.deviceMgr = deviceMgr
        self.dirPushButton = QtGui.QPushButton(_fromUtf8("选择"), self)
        self.dirPushButton.setObjectName(_fromUtf8("dirPushButton"))
        self.dirLineEdit = QtGui.QLineEdit(self)
        self.dirLineEdit.setObjectName(_fromUtf8("dirLineEdit"))
        self.dirChooseLayout = QtGui.QHBoxLayout()
        self.dirChooseLayout.setObjectName(_fromUtf8("dirChooseLayout"))
        self.dirChooseLayout.addWidget(self.dirPushButton)
        self.dirChooseLayout.addWidget(self.dirLineEdit)

        self.fileListWidget = QtGui.QListWidget(self)
        self.fileListWidget.setObjectName(_fromUtf8("fileListWidget"))

        self.chooseButton = QtGui.QPushButton(_fromUtf8("设备选择"), self)
        self.runButton = QtGui.QPushButton(_fromUtf8("执行"), self)

        self.dirLayout = QtGui.QVBoxLayout()
        self.dirLayout.addWidget(self.chooseButton)
        self.dirLayout.addWidget(self.runButton)
        self.dirLayout.addWidget(self.fileListWidget)
        self.dirLayout.addLayout(self.dirChooseLayout)

        self.scriptWidget = QtGui.QListWidget(self)
        self.scriptWidget.setObjectName(_fromUtf8("scriptWidget"))

        self.scriptLayout = QtGui.QHBoxLayout(self)
        self.scriptLayout.addLayout(self.dirLayout)
        self.scriptLayout.addWidget(self.scriptWidget)

        self.connectSignal()
        self.initDir()

    def connectSignal(self):
        connect(self.dirPushButton, signal("clicked()"), self.chooseDir)
        connect(self.fileListWidget,
                signal("itemSelectionChanged()"), self.chooseFile)
        connect(self.runButton, signal("clicked()"), self.run)
        connect(self.chooseButton, signal("clicked()"), self.chooseDevice)

    def initDir(self):
        path = os.path.join(os.getcwd(), "testcase")
        if not os.path.exists(path):
            os.makedirs(path)
        self.chooseDir(path)

    def refresh(self):
        self.chooseDir(self.dirPath)

    def chooseDir(self, dirPath=""):
        self.dirPath = dirPath or QtGui.QFileDialog.getExistingDirectory()
        print(self.dirPath)
        if self.dirPath:
            self.dirLineEdit.setText(self.dirPath)
            self.showFileList(self.dirPath)

    def showFileList(self, dirPath):
        self.fileListWidget.clear()
        for path in os.listdir(dirPath):
            if os.path.isdir(path):
                continue
            if str(path).endswith(".script"):
                item = QtGui.QListWidgetItem(path)
                self.fileListWidget.addItem(item)

    def chooseFile(self):
        items = self.fileListWidget.selectedItems()
        fileName = str(items[0].text())
        self.handleContext(fileName)

    def handleContext(self, fileName):
        with open(os.path.join(str(self.dirLineEdit.text()), fileName)) as f:
            context = f.read()
        self.scriptWidget.clear()
        for line in context.split("\n"):
            item = QtGui.QListWidgetItem(line)
            self.scriptWidget.addItem(item)

    def chooseDevice(self):
        boxNames = []
        for device in self.deviceMgr.getAllDevices():
            if device.deviceId:
                boxNames.append(device.deviceId)
        self.result = []
        QCheckBoxList(boxNames, self.result, self).show()

    def run(self):
        events = []
        for index in xrange(self.scriptWidget.count()):
            events.append(str(self.scriptWidget.item(index).text()))
        for deviceId in self.result:
            device = self.deviceMgr.findDeviceById(deviceId)
            replayer = Replayer(events, device)
            replayer.start()


class QCheckBoxList(QtGui.QDialog):

    def __init__(self, boxNames, result, parent):
        super(QCheckBoxList, self).__init__(parent)
        self.boxNames = boxNames
        self.result = result
        self.boxes = []
        self.button = QtGui.QPushButton(_fromUtf8("确定"), self)
        self.layout = QtGui.QVBoxLayout(self)
        self.initCheckBox()
        self.layout.addWidget(self.button)
        self.connectSignal()

    def connectSignal(self):
        connect(self.button, signal("clicked()"), self.getResult)

    def initCheckBox(self):
        for name in self.boxNames:
            box = QtGui.QCheckBox(_fromUtf8(name), self)
            self.layout.addWidget(box)
            self.boxes.append(box)

    def getResult(self):
        for box in self.boxes:
            if box.isChecked():
                self.result.append(box.text())
        self.close()


def run():
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
