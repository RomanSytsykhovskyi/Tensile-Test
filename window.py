from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtSerialPort import QSerialPortInfo


from force import Force
from length import Length
from comPortsTimer import ComPortsTimer
from graphTimer import GraphTimer

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #Load the UI Page
        uic.loadUi('design.ui', self)


        #thread
        self.thread = QThread()
        self.thread_graph = QThread()


        #timer
        self.time = 0
        self.timer = ComPortsTimer()
        self.timer.moveToThread(self.thread)
        self.timer_draw = GraphTimer()
        self.timer_draw.moveToThread(self.thread_graph)


        #data for plotting (test version)
        self.traces = dict()
        self.mainGraph = "graph"
        self.traces[self.mainGraph] = self.graph.plot(pen='y')


        #lists associate with com ports
        self.portList = []
        ports = QSerialPortInfo.availablePorts()
        for port in ports:
            self.portList.append(port.portName())

        self.comLForce.addItems(self.portList)   #add available com ports to the comboBox(comLForce)
        self.comLLength.addItems(self.portList)  #add available com ports to the comboBox(comLLength)

        self.usedPortList = []  #this list is for knowing about used ports
        self.forceConnection = False    #to know whether com port for force is connected
        self.lengthConnection = False   #to know whether com port for length is connected


        #signals
        self.openBForce.clicked.connect(self.onOpenForce)   #click on button(openBForce)
        self.closeBForce.clicked.connect(self.onCloseForce) #click on button(closeBForce)
        self.openBLength.clicked.connect(self.onOpenLength) #click on button(openBLength)
        self.closeBLength.clicked.connect(self.onCloseLength)   #click on button(closeBLength)
        self.drawB.clicked.connect(self.startClock)  #click on button to start clocking
        self.stopDB.clicked.connect(self.stopClock) #click on button to stop clocking
        self.thread.started.connect(self.timer.start)
        self.timer.process.connect(self.clock)
        self.timer.finished.connect(self.finishComsThread)
        self.thread_graph.started.connect(self.timer_draw.start)
        self.timer_draw.process.connect(self.drawing)
        self.timer_draw.finished.connect(self.finishGraphThread)

        pass



    #THREADS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



    def finishComsThread(self):
        self.thread.quit()
        self.thread.wait()

        pass

    def finishGraphThread(self):
        self.thread_graph.quit()
        self.thread_graph.wait()

        pass



    #PLUG!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



    def onOpenLength(self):
        name = self.comLLength.currentText()

        self.usedPortList.append(name)
        self.portList.remove(name)

        self.comBox()

        #set oportunity to click on the buttons
        self.openBLength.setEnabled(False)
        self.closeBLength.setEnabled(True)


        #set style and text of labels
        self.labelPortLength.setText(name)
        self.labelPortLength.setStyleSheet('color: rgb(0, 170, 0)')
        self.labelConditionLength.setText("CONNECTED")
        self.labelConditionLength.setStyleSheet('color: rgb(0, 170, 0)')


        #serial
        self.length = Length(name)
        self.lengthConnection = True

        pass

    def onCloseLength(self):    #click on button to close the com port
        self.usedPortList.remove(self.length.getName())
        self.portList.append(self.length.getName())

        self.comBox()


        #set oportunity to click on the buttons
        self.openBLength.setEnabled(True)
        self.closeBLength.setEnabled(False)


        #set style and text of labels
        self.labelPortLength.setText("None")
        self.labelPortLength.setStyleSheet('color: rgb(255, 0, 0)')
        self.labelConditionLength.setText("None")
        self.labelConditionLength.setStyleSheet('color: rgb(255, 0, 0)')

        self.lengthConnection = False

        pass

    def onOpenForce(self):  #click on button to connect the com port for force
        name = self.comLForce.currentText()

        self.usedPortList.append(name)
        self.portList.remove(name)

        self.comBox()

        #set oportunity to click on the buttons
        self.openBForce.setEnabled(False)
        self.closeBForce.setEnabled(True)

        #set style and text of labels
        self.labelPortForce.setText(name)
        self.labelPortForce.setStyleSheet('color: rgb(0, 170, 0)')
        self.labelConditionForce.setText("CONNECTED")
        self.labelConditionForce.setStyleSheet('color: rgb(0, 170, 0)')

        #serial
        self.force = Force(name)
        self.forceConnection = True

        pass

    def onCloseForce(self): #click on button to close the com port
        self.usedPortList.remove(self.force.getName())
        self.portList.append(self.force.getName())

        self.comBox()

        #set opportunity to click on the buttons
        self.openBForce.setEnabled(True)
        self.closeBForce.setEnabled(False)

        #set style and text of labels
        self.labelPortForce.setText("None")
        self.labelPortForce.setStyleSheet('color: rgb(255, 0, 0)')
        self.labelConditionForce.setText("None")
        self.labelConditionForce.setStyleSheet('color: rgb(255, 0, 0)')

        self.forceConnection = False

        pass



    #TIME!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



    def clock(self):    #function for recieving the date using QTimer(variable timer)
        self.lcdN.display(self.time)
        self.time += 0.10

        try:
            rxL = self.length.serial.readLine()
            rxF = self.force.serial.readLine()

            try:
                rxsL = str(rxL, 'utf-8')
                rxsL = rxsL[1:-6]
                rxsL = self.module(float(rxsL))
            except:
                rxsL = self.lastLength
            try:
                rxsF = str(rxF, 'utf-8')
                rxsF = rxsF[1:-6]
                rxsF = self.module(float(rxsF))
            except:
                rxsF = self.lastLength
        except:
            rxsL = self.lastLength
            rxsF = self.lastForce


        self.length.addData(rxsL)
        self.force.addData(rxsF)
        print("LENGTH: " + str(rxsL) + " | Force: " + str(rxsF))

        self.lastLength = rxsL
        self.lastForce = rxsF

        pass

    def startClock(self):   #to start all QTimers
        if(self.forceConnection and self.lengthConnection):
            self.length.setSerial()
            self.force.setSerial()

            self.thread.start()
            self.thread_graph.start()

            self.closeBLength.setEnabled(False)
            self.closeBForce.setEnabled(False)
            self.drawB.setEnabled(False)
            self.stopDB.setEnabled(True)

            self.lastLength = 0.0
            self.lastForce = 0.0
        else:
            QMessageBox.about(self, "CAUTION!!!", "No connection")

        pass

    def stopClock(self):    #function for stoping all QTimers
        self.length.closePort()
        self.force.closePort()

        self.time = 0
        self.lcdN.display(self.time)
        self.timer.stop()
        self.timer_draw.stop()

        self.closeBLength.setEnabled(True)
        self.closeBForce.setEnabled(True)
        self.drawB.setEnabled(True)
        self.stopDB.setEnabled(False)

        pass



    #GRAPH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



    def drawing(self): #function for drawing the graph using QTimer(variable timer_draw)
        self.traces[self.mainGraph].setData(self.length.getData(), self.force.getData())

        pass



    #MATH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



    def module(self, var):
        if var < 0:
            return -1 * var
        return var



    #WIDGETS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



    def comBox(self):   #reload a new list of comboBox
        self.comLLength.clear()
        self.comLLength.addItems(self.portList)
        self.comLForce.clear()
        self.comLForce.addItems(self.portList)

        pass