from PySide import QtGui, QtCore
import ctypes, json, datetime, os
from selTesting import todayFuelPrice
import matplotlib.pyplot as plt
from toggelSwitch import toggleSwitch

SCREENX = ctypes.windll.user32.GetSystemMetrics(0)
SCREENY = ctypes.windll.user32.GetSystemMetrics(1)

DATETODAY = datetime.date.today()

WRK_DIR = os.getcwd().replace("\\","/")

if os.path.exists(os.path.expanduser('~/Documents').replace('\\','/')):
    finalJson = os.path.expanduser('~/Documents').replace('\\','/')+"/FuelInfoCalculator"
    try:
        os.mkdir(finalJson)
    except:
        pass
    finalJson = finalJson+"/fuelInfo.json"
    if not os.path.exists(finalJson):
        with open(finalJson, 'w') as fd:
            fd.write('{"DailyRate":{}, "FuelInfo": {"FilledAmount": [], "FilledOn": []}, "TotalKMS": {}}')
jsonFile = os.path.expanduser('~/Documents').replace('\\','/')+"/FuelInfoCalculator/fuelInfo.json"
DATASTORE = jsonFile

class adDialog(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(adDialog, self).__init__(parent)
        self.width = 300
        self.height = 150
        self.setWindowTitle("Add new Values")
        self.setFixedSize(self.width, self.height)
        self.centralWidget = QtGui.QWidget(self)
        self.mainLayout = QtGui.QGridLayout(self.centralWidget)
        amtLab = QtGui.QLabel(self.centralWidget)
        amtLab.setText("Amount : ")
        self.amtEdit = QtGui.QLineEdit(self.centralWidget)
        self.amtEdit.setPlaceholderText("Enter amount here")
        upDate = QtGui.QLabel(self.centralWidget)
        upDate.setText("Date : ")
        self.upDateBox = QtGui.QComboBox(self.centralWidget)
        self.upDateBox.addItem(myApp().sysDateToDate(datetime.date.today()))
        self.upDateBox.addItem(myApp().sysDateToDate(datetime.date.today()-datetime.timedelta(1)))
        adBtn = QtGui.QPushButton(self.centralWidget)
        adBtn.setText("Add Amount")
        adBtn.clicked.connect(self.addInfo)
        canBtn = QtGui.QPushButton(self.centralWidget)
        canBtn.setText("Cancel")
        canBtn.clicked.connect(self.close)
        self.mainLayout.addWidget(amtLab, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.amtEdit, 0, 1, 1, 3)
        self.mainLayout.addWidget(upDate, 1, 0, 1, 1)
        self.mainLayout.addWidget(self.upDateBox, 1, 1, 1, 3)
        self.mainLayout.addWidget(adBtn, 2, 2, 1, 1)
        self.mainLayout.addWidget(canBtn, 2, 3, 1, 1)
        # self.mainLayout.addLayout(toggleSwitch.layout,0,3,1,1)

        self.setCentralWidget(self.centralWidget)

    def addInfo(self):
        with open(DATASTORE, 'r') as fd:
            data = json.load(fd)
        if self.amtEdit.text() != "":
            data['FuelInfo']['FilledAmount'].append(float(self.amtEdit.text()))
            data['FuelInfo']['FilledOn'].append(str(self.upDateBox.itemText(self.upDateBox.currentIndex())))
        with open(DATASTORE, 'w') as fd:
            json.dump(data, fd)
        myApp().updateTable()
        self.close()

class myApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(myApp, self).__init__(parent)
        self.windowX = 650
        self.windowY = 350
        self.avgDays = [0]
        self.avgEst = self.avgDays[0]
        self.avgPdLst = []
        self.avgPd = 0
        self.totAmtLst = []
        self.totAmt = 0
        self.getFuelPrice()
        self.setupUi()

    def DateToSysDate(self, date):
        form = date.split('-')
        return datetime.date(int(form[2]), int(form[1]), int(form[0]))

    def sysDateToDate(self, date):
        return str(date.strftime('%d-%m-%Y'))

    def getFuelPrice(self):
        with open(DATASTORE) as fd:
            dailyData = json.load(fd)
        if self.sysDateToDate(DATETODAY) in dailyData["DailyRate"].keys():
            self.curPrice = dailyData["DailyRate"][self.sysDateToDate(DATETODAY)]
        else:
            self.curPrice = todayFuelPrice().getPrice()
            dailyData["DailyRate"][self.sysDateToDate(DATETODAY)] = self.curPrice
            with open(DATASTORE, 'w') as fd:
                json.dump(dailyData, fd)

    def setupUi(self):
        self.setGeometry(QtCore.QRect((SCREENX-self.windowX)/2, (SCREENY-self.windowY)/2, self.windowX, self.windowY))
        self.centralWidget = QtGui.QWidget(self)
        self.mainLayout = QtGui.QGridLayout(self.centralWidget)

        self.addNew = QtGui.QPushButton(self.centralWidget)
        self.editEntry = QtGui.QPushButton(self.centralWidget)
        self.editEntry.clicked.connect(self.displayGraph)
        self.delEntry = QtGui.QPushButton(self.centralWidget)
        emptySpace = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.entryHolder = QtGui.QTableView(self.centralWidget)
        self.nextEntryLab = QtGui.QLabel(self.centralWidget)

        self.addNew.clicked.connect(self.inputAmount)

        self.delEntry.setEnabled(False)

        self.dataEntryModel = QtGui.QStandardItemModel(0, 6)
        self.dataEntryModel.setHorizontalHeaderItem(0, QtGui.QStandardItem("Amount"))
        self.dataEntryModel.setHorizontalHeaderItem(1, QtGui.QStandardItem("Date"))
        self.dataEntryModel.setHorizontalHeaderItem(2,QtGui.QStandardItem("Liters"))
        self.dataEntryModel.setHorizontalHeaderItem(3, QtGui.QStandardItem("Average Date"))
        self.dataEntryModel.setHorizontalHeaderItem(4, QtGui.QStandardItem("Total Days"))
        self.dataEntryModel.setHorizontalHeaderItem(5, QtGui.QStandardItem("Spent/Day"))
        self.entryHolder.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.entryHolder.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.entryHolder.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.entryHolder.setModel(self.dataEntryModel)
        self.header = self.entryHolder.horizontalHeader()
        self.header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        self.header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        self.header.setResizeMode(3, QtGui.QHeaderView.ResizeToContents)
        self.header.setResizeMode(4, QtGui.QHeaderView.ResizeToContents)
        self.header.setResizeMode(5, QtGui.QHeaderView.Stretch)

        distanceLabel = QtGui.QLabel(self.centralWidget)
        distanceLabel.setText("Total Amount : ")
        self.distanceValue = QtGui.QLabel(self.centralWidget)
        amountLabel = QtGui.QLabel(self.centralWidget)
        amountLabel.setText("Todays Price : ")
        self.amountValue = QtGui.QLabel(self.centralWidget)
        avgPerDayLab = QtGui.QLabel(self.centralWidget)
        avgPerDayLab.setText("Average Per Day : ")
        self.avgPerDay = QtGui.QLabel(self.centralWidget)

        verticalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        self.mainLayout.addWidget(self.addNew, 0, 0, 1, 1)#(column no., row no., no.of columns, no.of rows)
        self.mainLayout.addWidget(self.editEntry, 0, 1, 1, 1)
        self.mainLayout.addWidget(self.delEntry, 0, 2, 1, 1)
        self.mainLayout.addItem(emptySpace, 0, 3, 1, 1)
        self.mainLayout.addWidget(self.nextEntryLab, 0, 5, 1, 2)
        self.mainLayout.addWidget(self.entryHolder, 1, 0, 4, 4)
        self.mainLayout.addWidget(distanceLabel, 1, 5, 1, 1)
        self.mainLayout.addWidget(self.distanceValue, 1, 6, 1, 1)
        self.mainLayout.addWidget(amountLabel, 2, 5, 1, 1)
        self.mainLayout.addWidget(self.amountValue, 2, 6, 1, 1)
        self.mainLayout.addWidget(avgPerDayLab, 3, 5, 1, 1)
        self.mainLayout.addWidget(self.avgPerDay, 3, 6, 1, 1)
        self.mainLayout.addItem(verticalSpacer, 4, 6, 1, 2)

        self.setCentralWidget(self.centralWidget)

        self.retranslateUi()
        self.updateTable()

    def retranslateUi(self):
        self.setWindowTitle("CFE(Fuel Efficiency)")
        self.addNew.setText("Add")
        self.editEntry.setText("Show Rate Graph")
        self.delEntry.setText("Delete")

        self.distanceValue.setText("496.2km")
        self.amountValue.setText("Rs."+str(self.curPrice))

    def inputAmount(self):
        dial = adDialog(self)
        dial.show()

    def updateTable(self):
        with open(DATASTORE) as fd:
            data = json.load(fd)
        indAmt = 0
        for amount in data["FuelInfo"]["FilledOn"]:
            onDate = amount
            nextUp = None
            try:
                nextUp = data["FuelInfo"]["FilledOn"][indAmt+1]
            except:
                pass
            if nextUp != None:
                days = (self.DateToSysDate(nextUp) - self.DateToSysDate(onDate)).days
                self.avgDays.append(days)
            indAmt += 1
        for each in self.avgDays:
            self.avgEst += each
        if len(self.avgDays) != 1:
            self.avgEst = round(self.avgEst/(len(self.avgDays)-1))
        indAmt = 0
        for amount in data["FuelInfo"]["FilledAmount"]:
            self.totAmtLst.append(amount)
            item = QtGui.QStandardItem("Rs."+str(amount))
            self.dataEntryModel.setItem(indAmt, 0, item)
            onDate = data["FuelInfo"]["FilledOn"][indAmt]
            item = QtGui.QStandardItem(onDate)
            self.dataEntryModel.setItem(indAmt, 1, item)
            item = QtGui.QStandardItem(str(round(amount/data["DailyRate"][onDate],2))+" Lts")
            self.dataEntryModel.setItem(indAmt, 2, item)
            nextUp = None
            totalDays = None
            try:
                nextUp = data["FuelInfo"]["FilledOn"][indAmt+1]
            except:
                pass
            if nextUp != None:
                item = QtGui.QStandardItem(nextUp)
                totalDays = self.avgDays[indAmt+1]
            else:
                nextUp = self.sysDateToDate(self.DateToSysDate(onDate)+datetime.timedelta(days=self.avgEst))
                if not (self.DateToSysDate(nextUp)-DATETODAY).days < 0:
                    self.nextEntryLab.setText("Next Fuel may be with in "+str((self.DateToSysDate(nextUp)-DATETODAY).days)+" days")
                else:
                    self.nextEntryLab.setText(
                        "Ohhh! You're doing great... \nYou crossed by " + str((DATETODAY - (self.DateToSysDate(nextUp))).days) + " days")
                item = QtGui.QStandardItem(nextUp+"(Avg)")
                totalDays = str((self.DateToSysDate(nextUp)-self.DateToSysDate(onDate)).days)+" Avg"
            self.dataEntryModel.setItem(indAmt, 3, item)
            item = QtGui.QStandardItem(str(totalDays)+" Days")
            self.dataEntryModel.setItem(indAmt, 4, item)
            try:
                perDay = round(amount/totalDays,2)
                item = QtGui.QStandardItem("Rs"+str(perDay))
                self.avgPdLst.append(perDay)
            except:
                item = QtGui.QStandardItem("Progress")
            self.dataEntryModel.setItem(indAmt, 5, item)
            indAmt += 1
        for each in self.avgPdLst:
            self.avgPd += each
        if len(self.avgPdLst)!=0:
            self.avgPd = round(self.avgPd/len(self.avgPdLst),2)
        self.avgPerDay.setText("Rs."+str(self.avgPd))
        for each in self.totAmtLst:
            self.totAmt += each

        latestUpdate = QtGui.QStandardItem(str(int(round(amount/self.avgPd)))+" Avg Days")
        self.dataEntryModel.setItem(indAmt-1, 4, latestUpdate)
        lastDate = QtGui.QStandardItem(self.sysDateToDate(self.DateToSysDate(onDate)+datetime.timedelta(days=int(round(amount/self.avgPd))))+"(Avg)")
        self.dataEntryModel.setItem(indAmt-1, 3, lastDate)
        self.nextEntryLab.setText("Will Update")
        finalUp = self.sysDateToDate(self.DateToSysDate(onDate)+datetime.timedelta(days=int(round(amount/self.avgPd))))
        if not (self.DateToSysDate(finalUp) - DATETODAY).days < 0:
            self.nextEntryLab.setText(
                "Next Fuel may be with in " + str((self.DateToSysDate(finalUp) - DATETODAY).days) + " days")
        else:
            self.nextEntryLab.setText(
                "Ohhh! You're doing great... \nYou crossed by " + str(
                    (DATETODAY - (self.DateToSysDate(finalUp))).days) + " days")

        self.distanceValue.setText("Rs."+str(round(self.totAmt,2)))

    def displayGraph(self):
        with open(finalJson) as fd:
            data = json.load(fd)
        dates = []
        rates = []
        for keys, values in data['DailyRate'].items():
            dated = self.DateToSysDate(keys)
            if int(datetime.date.today().month) == int(str(dated).split("-")[1]):
                # print(keys)
                dates.append(keys)

        dates.sort()
        for each in dates:
            rates.append(data['DailyRate'][each])
        x = dates
        y = rates
        mydate = datetime.datetime.now()
        x = [i.split('-')[0] for i in x]
        plt.figure(num="Rate graph for %s month"%mydate.strftime("%B"))
        plt.plot(x,y)
        plt.xlabel("Dates in %s"%mydate.strftime("%B"))
        plt.ylabel("Petrol Rates")

        plt.show()

if __name__ == '__main__':
    import sys
    gui = QtGui.QApplication(sys.argv)
    app = myApp()
    app.show()
    sys.exit(gui.exec_())