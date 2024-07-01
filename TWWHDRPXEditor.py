from PyQt6 import QtGui
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QColorDialog, QFileDialog, QTabWidget, QCheckBox, QSpinBox, QComboBox
from PyQt6 import uic
import sys
import os

class Window(QMainWindow):
    fileOpen = False
    fname = tuple
    openFile = False
    currentColor = QtGui.QColor
    alphaChanged = False
    trailChanged = False
    trailBoom = hex
    alphaBoom = int
    trailSwing = hex
    alphaSwing = int
    trailElixir = hex
    alphaElixir = int
    trailParry = hex
    alphaParry = int

    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("GUI.ui", self)

        self.statusBar()
        self.setFixedSize(515, 331)
        self.labell = self.findChild(QLabel, "label_2")
        self.newSave = self.findChild(QLabel, "label_11")
        self.sail = self.findChild(QCheckBox, "checkBox")
        self.alpha = self.findChild(QSpinBox, "spinBox")
        self.colorChoice = self.findChild(QComboBox, "comboBox")
        self.island = self.findChild(QComboBox, "comboBox_2")
        self.point = self.findChild(QComboBox, "comboBox_3")
        self.labelX1 = self.findChild(QLabel, "label_10")
        self.labelX2 = self.findChild(QLabel, "label_8")
        self.labelX3 = self.findChild(QLabel, "label_9")
        self.toolBar = self.addToolBar("Extraction")

        fontColor = QtGui.QAction('Change Color', self)
        fontColor.triggered.connect(self.color_picker)

        self.toolBar.addAction(fontColor)

        self.open = self.findChild(QtGui.QAction, 'actionOpen')
        self.save = self.findChild(QtGui.QAction, 'actionSave')
        self.default = self.findChild(QtGui.QAction, "actionDefault")
        self.tab = self.findChild(QTabWidget, "tabWidget")
        self.styleChoice = self.findChild(QLabel, "label")
        self.styleChoice.setAutoFillBackground(True)
        self.newSave.setAutoFillBackground(True)
        self.newSave.setStyleSheet("QWidget { background-color: rgb(0, 0, 0) }")
        self.labelX1.setStyleSheet("color: white")
        self.labelX2.setStyleSheet("color: white")
        self.labelX3.setStyleSheet("color: white")

        self.tab.hide()
        self.toolBar.hide()
        self.open.triggered.connect(self.Open)
        self.default.triggered.connect(self.Default)
        self.colorChoice.currentIndexChanged.connect(self.trailChanging)
        self.island.currentIndexChanged.connect(self.islandNew)
        self.alpha.valueChanged.connect(self.alphaChange)
        self.save.triggered.connect(self.Saving)

        self.show()
    def Default(self):
        self.sail.setChecked(False)
        self.trailBoom = 0xffff7b
        self.trailSwing = 0xffffff
        self.trailElixir = 0xffff7b
        self.trailParry = 0x5aff5a
        self.alphaBoom = self.alphaElixir = self.alphaParry = self.alphaSwing = 0x96
        self.alpha.setValue(self.alphaBoom)
        self.island.setCurrentIndex(25)
        self.point.setCurrentIndex(21)

    def Open(self):
        fname = QFileDialog.getOpenFileName(self, "Open TWW HD RPX File", "", "Wii U RPX File (*.rpx)")
        if fname[0]:
            if os.path.getsize(fname[0]) >= 10000000:
                if self.fileOpen == False:
                    self.fileOpen = True
                    self.save.setEnabled(True)
                    self.default.setEnabled(True)
                    self.tab.show()
                    self.toolBar.show()
                self.fname = fname
                self.CheckRPX()
            elif os.path.getsize(fname[0]) < 10000000:
                self.labell.setText("The RPX file is not decompressed.")
                self.tab.hide()
                self.toolBar.hide()
                self.save.setEnabled(False)
                self.default.setEnabled(False)
                self.fileOpen = False

    def CheckRPX(self):
        if self.fileOpen == True:
            file = open(self.fname[0], 'r+b')
            file.seek(0x192B68)
            self.trailBoom = int.from_bytes(file.read(3))
            self.alphaBoom = int.from_bytes(file.read(1))
            file.seek(0x1CF5C0)
            self.trailSwing = int.from_bytes(file.read(3))
            self.alphaSwing = int.from_bytes(file.read(1))
            self.trailElixir = int.from_bytes(file.read(3))
            self.alphaElixir = int.from_bytes(file.read(1))
            self.trailParry = int.from_bytes(file.read(3))
            self.alphaParry = int.from_bytes(file.read(1))
            self.trailChanging()
            file.seek(0x36ACA4)
            if file.read(4) == b'\x4E\x80\x00\x20':
                self.sail.setChecked(True)
            else: self.sail.setChecked(False)
            file.seek(0x7BD22F)
            mapChecking = int.from_bytes(file.read(1)) - 1
            file.seek(0x7BD233)
            xyz = 0
            paddingThing = ""
            if mapChecking < 25: 
                self.island.setCurrentIndex(mapChecking)
                pointChecking = str(int.from_bytes(file.read(1)))
                foile = open("spawnPoints.txt", 'r')
                while self.island.currentText() not in paddingThing:
                    paddingThing = foile.readline()
                self.point.setCurrentIndex(xyz)
                for line in foile:
                    try:
                        i = int(line)
                        if pointChecking != str(i):
                            xyz += 1
                            self.point.setCurrentIndex(xyz)
                        else: break
                    except ValueError:
                        break
            elif mapChecking == 43: 
                self.island.setCurrentIndex(25)
                pointChecking = str(int.from_bytes(file.read(1)))
                foile = open("spawnPoints.txt", 'r')
                while self.island.currentText() not in paddingThing:
                    paddingThing = foile.readline()
                self.point.setCurrentIndex(xyz)
                for line in foile:
                    try:
                        i = int(line)
                        if pointChecking != str(i):
                            xyz += 1
                            self.point.setCurrentIndex(xyz)
                        else: break
                    except ValueError:
                        break
            else:
                self.island.setCurrentIndex(25)
                self.point.setCurrentIndex(21)

    def trailChanging(self):
        if self.colorChoice.currentIndex() == 0:
            self.currentColor = QtGui.QColor(self.trailBoom)
            self.alpha.setValue(self.alphaBoom)
        elif self.colorChoice.currentIndex() == 1:
            self.currentColor = QtGui.QColor(self.trailSwing)
            self.alpha.setValue(self.alphaSwing)
        elif self.colorChoice.currentIndex() == 2:
            self.currentColor = QtGui.QColor(self.trailParry)
            self.alpha.setValue(self.alphaParry)
        elif self.colorChoice.currentIndex() == 3:
            self.currentColor = QtGui.QColor(self.trailElixir)
            self.alpha.setValue(self.alphaElixir)
        self.trailChanged = True
        self.color_picker()
        
    def color_picker(self):
        if self.alphaChanged == False and self.trailChanged == False:
            self.currentColor = QColorDialog.getColor()
            if self.colorChoice.currentIndex() == 0:
                self.trailBoom = f'0x{self.currentColor.red():02x}{self.currentColor.green():02x}{self.currentColor.blue():02x}'
                self.trailBoom = int(self.trailBoom, 16)
            elif self.colorChoice.currentIndex() == 1:
                self.trailSwing = f'0x{self.currentColor.red():02x}{self.currentColor.green():02x}{self.currentColor.blue():02x}'
                self.trailSwing = int(self.trailSwing, 16)
            elif self.colorChoice.currentIndex() == 2:
                self.trailParry = f'0x{self.currentColor.red():02x}{self.currentColor.green():02x}{self.currentColor.blue():02x}'
                self.trailParry = int(self.trailParry, 16)
            elif self.colorChoice.currentIndex() == 3:
                self.trailElixir = f'0x{self.currentColor.red():02x}{self.currentColor.green():02x}{self.currentColor.blue():02x}'
                self.trailElixir = int(self.trailElixir, 16)
        self.styleChoice.setStyleSheet("QWidget { background-color: rgba("+ str(self.currentColor.red()) + "," + str(self.currentColor.green()) + "," + str(self.currentColor.blue()) + "," + str(self.alpha.value()) + ") }")
        self.alphaChanged = False
        self.trailChanged = False

    def alphaChange(self):
        self.alphaChanged = True
        if self.colorChoice.currentIndex() == 0:
            self.alphaBoom = self.alpha.value()
        elif self.colorChoice.currentIndex() == 1:
            self.alphaSwing = self.alpha.value()
        elif self.colorChoice.currentIndex() == 2:
            self.alphaParry = self.alpha.value()
        elif self.colorChoice.currentIndex() == 3:
            self.alphaElixir = self.alpha.value()
        self.color_picker()

    def islandNew(self):
        file = open("spawnPoints.txt", "r")
        paddingThing = ""
        while self.island.currentText() not in paddingThing:
            paddingThing = file.readline()
        self.point.clear()
        for line in file:
            try:
                i = int(line)
                self.point.addItem(str(i))
            except ValueError:
                break

    def Saving(self):
        file = open(self.fname[0], 'r+b')
        file.seek(0x192B68)
        file.write(int(self.trailBoom).to_bytes(3))
        file.write(int(self.alphaBoom).to_bytes(1))
        file.seek(0x1CF5C0)
        file.write(int(self.trailSwing).to_bytes(3))
        file.write(int(self.alphaSwing).to_bytes(1))
        file.write(int(self.trailElixir).to_bytes(3))
        file.write(int(self.alphaElixir).to_bytes(1))
        file.write(int(self.trailParry).to_bytes(3))
        file.write(int(self.alphaParry).to_bytes(1))
        file.seek(0x36ACA4)
        if self.sail.isChecked() == False:
            sailRemoval = b'\x7C\x08\x02\xA6'
        else: sailRemoval = b'\x4E\x80\x00\x20'
        file.write(sailRemoval)
        if self.island.currentIndex() < 25:
            islandValue = self.island.currentIndex() + 1
        else: islandValue = self.island.currentIndex() + 19
        file.seek(0x7BD22F)
        file.write(int(islandValue).to_bytes(1))
        file.seek(0x7BD233)
        file.write(int(self.point.currentText()).to_bytes(1))
        file.seek(0x7BD26B)
        file.write(int(islandValue).to_bytes(1))
        file.seek(0x7BD26F)
        file.write(int(self.point.currentText()).to_bytes(1))

if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    UIWindow = Window()
    app.exec()