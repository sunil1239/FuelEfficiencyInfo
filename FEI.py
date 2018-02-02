from PySide import QtGui, QtCore
import ctypes, json
from selTesting import todayFuelPrice

SCREENX = ctypes.windll.user32.GetSystemMetrics(0)
SCREENY = ctypes.windll.user32.GetSystemMetrics(1)

CUR_PRICE = todayFuelPrice().getPrice()

class myApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(myApp, self).__init__(parent)
        self.windowX = 500
        self.windowY = 350
        self.setupUi()

    def setupUi(self):
        self.setGeometry(QtCore.QRect((SCREENX-self.windowX)/2, (SCREENY-self.windowY)/2, self.windowX, self.windowY))
        self.centralWidget = QtGui.QWidget(self)
        self.mainLayout = QtGui.QGridLayout(self.centralWidget)

        self.addNew = QtGui.QPushButton(self.centralWidget)
        self.editEntry = QtGui.QPushButton(self.centralWidget)
        self.delEntry = QtGui.QPushButton(self.centralWidget)
        emptySpace = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.entryHolder = QtGui.QTableView(self.centralWidget)
        distanceLabel = QtGui.QLabel(self.centralWidget)
        distanceLabel.setText("Total Distance : ")
        self.distanceValue = QtGui.QLabel(self.centralWidget)
        amountLabel = QtGui.QLabel(self.centralWidget)
        amountLabel.setText("Todays Price : ")
        self.amountValue = QtGui.QLabel(self.centralWidget)
        verticalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        self.mainLayout.addWidget(self.addNew, 0, 0, 1, 1)#(column no., row no., no.of columns, no.of rows)
        self.mainLayout.addWidget(self.editEntry, 0, 1, 1, 1)
        self.mainLayout.addWidget(self.delEntry, 0, 2, 1, 1)
        self.mainLayout.addItem(emptySpace, 0, 3, 1, 1)
        self.mainLayout.addWidget(self.entryHolder, 1, 0, 3, 4)
        self.mainLayout.addWidget(distanceLabel, 1, 5, 1, 1)
        self.mainLayout.addWidget(self.distanceValue, 1, 6, 1, 1)
        self.mainLayout.addWidget(amountLabel, 2, 5, 1, 1)
        self.mainLayout.addWidget(self.amountValue, 2, 6, 1, 1)
        self.mainLayout.addItem(verticalSpacer, 3, 6, 1, 2)

        self.setCentralWidget(self.centralWidget)

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle("CFE(Fuel Efficiency)")
        self.addNew.setText("Add")
        self.editEntry.setText("Edit")
        self.delEntry.setText("Delete")

        self.distanceValue.setText("496.2km")
        self.amountValue.setText("Rs."+str(CUR_PRICE))


import sys
gui = QtGui.QApplication(sys.argv)
app = myApp()
app.show()
sys.exit(gui.exec_())