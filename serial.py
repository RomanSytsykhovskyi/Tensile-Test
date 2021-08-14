from PyQt5.QtCore import QIODevice
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

class Serial:

    def __init__(self, name):
        self.name = name

        self.list = list()

        pass

    def setSerial(self):
        # serial
        self.serial = QSerialPort()
        self.serial.setBaudRate(9600)

        self.serial.setPortName(self.name)
        self.serial.open(QIODevice.ReadWrite)

        pass

    def closePort(self):
        self.serial.close()

        pass

    def getData(self):
        return self.list