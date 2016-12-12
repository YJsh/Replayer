# -*- coding: utf-8 -*-
import os
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

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.ctrlWidget = QtGui.QWidget(self.centralwidget)
        self.ctrlWidget.setObjectName(_fromUtf8("ctrlWidget"))
        self.ctrlWidget.setGeometry(QtCore.QRect(400, 60, 220, 320))

        self.ctrlLayout = QtGui.QHBoxLayout()
        self.ctrlLayout.setObjectName(_fromUtf8("ctrlLayout"))

        self.ctrl = QtGui.QPushButton(self.ctrlWidget)
        self.ctrl.setObjectName(_fromUtf8("ctrl"))
        self.ctrlLayout.addWidget(self.ctrl)

        self.stop = QtGui.QPushButton(self.ctrlWidget)
        self.stop.setObjectName(_fromUtf8("stop"))
        self.ctrlLayout.addWidget(self.stop)

        self.replay = QtGui.QPushButton(self.ctrlWidget)
        self.replay.setObjectName(_fromUtf8("replay"))
        self.ctrlLayout.addWidget(self.replay)

        self.scriptLayout = QtGui.QVBoxLayout(self.ctrlWidget)
        self.scriptLayout.setObjectName(_fromUtf8("scriptLayout"))
        self.scriptLayout.addLayout(self.ctrlLayout)

        self.scriptWidget = QtGui.QListWidget(self.ctrlWidget)
        self.scriptWidget.setObjectName(_fromUtf8("scriptWidget"))
        self.scriptLayout.addWidget(self.scriptWidget)

        self.dirWidget = QtGui.QWidget(self.centralwidget)
        self.dirWidget.setObjectName(_fromUtf8("dirWidget"))
        self.dirWidget.setGeometry(QtCore.QRect(20, 190, 340, 220))

        self.dirLayout = QtGui.QVBoxLayout(self.dirWidget)
        self.dirLayout.setObjectName(_fromUtf8("dirLayout"))

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

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.ctrl, QtCore.SIGNAL(_fromUtf8("clicked()")), self.doStart)
        QtCore.QObject.connect(self.stop, QtCore.SIGNAL(_fromUtf8("clicked()")), self.doStop)
        QtCore.QObject.connect(
            self.dirPushButton,
            QtCore.SIGNAL(_fromUtf8("clicked()")),
            self.chooseDir)
        QtCore.QObject.connect(
            self.fileListWidget,
            QtCore.SIGNAL(_fromUtf8("itemSelectionChanged()")),
            self.chooseFile)

    def retranslateUi(self, MainWindow):
        self.ctrl.setText(_translate("MainWindow", "开始", None))
        self.stop.setText(_translate("MainWindow", "结束", None))
        self.replay.setText(_translate("MainWindow", "回放", None))
        self.dirPushButton.setText(_translate("MainWindow", "选择", None))
        self.chooseDir("E:\workspace\ScriptRecord")

    def doStart(self):
        self.ctrl.setText(_translate("MainWindow", "暂停", None))
        QtCore.QObject.connect(self.ctrl, QtCore.SIGNAL(_fromUtf8("clicked()")), self.doPause)

    def doPause(self):
        self.ctrl.setText(_translate("MainWindow", "继续", None))
        QtCore.QObject.connect(self.ctrl, QtCore.SIGNAL(_fromUtf8("clicked()")), self.doStart)

    def doStop(self):
        self.ctrl.setText(_translate("MainWindow", "开始", None))
        QtCore.QObject.connect(self.ctrl, QtCore.SIGNAL(_fromUtf8("clicked()")), self.doStart)

    def chooseDir(self, dirPath=""):
        dirPath = dirPath or QtGui.QFileDialog.getExistingDirectory()
        print(dirPath)
        if dirPath:
            self.dirLineEdit.setText(dirPath)
            self.showFileList(dirPath)

    def saveScript(self):
        fileName = QtGui.QFileDialog.getSaveFileName()
        print(fileName)

    def showFileList(self, dirPath):
        self.fileListWidget.clear()
        for path in os.listdir(dirPath):
            if os.path.isdir(path):
                continue
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


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
