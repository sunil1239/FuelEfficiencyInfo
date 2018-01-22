from PySide import QtGui, QtCore
import sys

class FuelEfficiency(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(FuelEfficiency, self).__init__(parent)

gui = QtGui.QApplication(sys.argv)
app = FuelEfficiency
app.show()
sys.exit(gui.exec_())
