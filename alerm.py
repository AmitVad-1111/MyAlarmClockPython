from PyQt5.QtWidgets import QLCDNumber,QMainWindow,QApplication,QFrame,QVBoxLayout,QPushButton,QComboBox,QHBoxLayout,QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QEvent as evnt,QUrl
from pygame import mixer
from os import path
import datetime as dt
import sys,threading,time


class Alram(QMainWindow):

    def __init__(self):
        super().__init__()
        self.hour = '00'
        self.minute = '00'

        #set and load music
        try:
            self.song = path.abspath(path.join(path.dirname(__name__),"carol_of_the_bells-alarm.mp3")) 
            self.isMusicPlay = False
            mixer.init()
            mixer.music.load(self.song)
            mixer.music.set_volume(0.7)

            self.setWindowTitle('Alram')
            self.setGeometry(300,200,350,200)
            self.buildGui()
            self.getCurrentTime()
            self.show()
        except Exception as e:
            pass


    def buildGui(self):
        self.digiClock = QFrame(self)
        self.digiClock_ly = QVBoxLayout()
        self.digiClock.setLayout(self.digiClock_ly)


        self.setALrmBox = QFrame(self.digiClock)
        self.setALrmBox_ly = QHBoxLayout()
        self.setALrmBox.setLayout(self.setALrmBox_ly)

        self.LCDDisplay = QLCDNumber(self.digiClock)
        self.LCDDisplay.setMaximumHeight(200)
        self.LCDDisplay.setMaximumWidth(350)
        self.LCDDisplay.setDigitCount(8)
        self.LCDDisplay.setSegmentStyle(QLCDNumber.Flat)
        #self.LCDDisplay.setBaseSize(150,100)

        self.stopAlrm = QPushButton("Stop Alram")
        self.stopAlrm.clicked.connect(self.stopAlarmTone)

        self.HHour = QComboBox(self.setALrmBox)
        self.MMunit = QComboBox(self.setALrmBox)

        self.HHour.addItem('Hour')
        self.MMunit.addItem('Minute')

        for s in range(0,24):
            s = '0'+str(s) if s in [0,1,2,3,4,5,6,7,8,9] else str(s)
            self.HHour.addItem(s)

        for m in range(0,61):
            m = '0'+str(m) if m in [0,1,2,3,4,5,6,7,8,9] else str(m)
            self.MMunit.addItem(m)

        self.setAlrm = QPushButton("Set Alarm",self.setALrmBox)
        self.setAlrm.clicked.connect(self.setAlrmBtnClick)

        self.setALrmBox_ly.addWidget(self.HHour)
        self.setALrmBox_ly.addWidget(self.MMunit)
        self.setALrmBox_ly.addWidget(self.setAlrm)

        self.digiClock_ly.addWidget(self.LCDDisplay)
        self.digiClock_ly.addWidget(self.setALrmBox)
        self.setCentralWidget(self.digiClock)

    def getCurrentTime(self):
        CTime = dt.datetime.now()
        h = '0'+str(CTime.hour) if CTime.hour in [0,1,2,3,4,5,6,7,8,9] else str(CTime.hour)
        m = '0'+str(CTime.minute) if CTime.minute in [0,1,2,3,4,5,6,7,8,9] else str(CTime.minute)
        s = '0'+str(CTime.second) if CTime.second in [0,1,2,3,4,5,6,7,8,9] else str(CTime.second)
        c = h + ':' + m + ':' + s

        if h == self.getHour() and m == self.getMinute():
            if self.isMusicPlay == False:
                mixer.music.play()
                self.isMusicPlay = True                
                if self.stopAlrm.parentWidget() == None:
                    self.stopAlrm.setParent(self.digiClock)
                else:
                    self.stopAlrm.show()
                self.digiClock_ly.addWidget(self.stopAlrm)

        self.LCDDisplay.display(c)
        self.task1 = threading.Timer(1,self.getCurrentTime)
        self.task1.start()

    def setAlrmBtnClick(self):
        if self.isMusicPlay == True:
            self.stopAlrm.hide()
            self.isMusicPlay = False
        self.hour = str(self.HHour.currentText())
        self.minute = str(self.MMunit.currentText())
        QMessageBox.information(self,'Alerm Set Info',"Alerm set Successfully...!",QMessageBox.Ok)
        #print(f'Hour:{self.hour} Minute:{self.minute}')

    def getHour(self):
        return self.hour

    def getMinute(self):
        return self.minute

    def stopAlarmTone(self):
        mixer.music.stop()

    def closeEvent(self,evnt):
        self.task1.cancel()
        return super().closeEvent(evnt)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = Alram()
    sys.exit(app.exec_())
