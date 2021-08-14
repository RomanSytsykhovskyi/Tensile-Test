from serial import Serial

class Length(Serial):
    def getName(self):
        return self.name

    def setLength(self, len):
        self.length = len

        pass

    def addData(self, var):
        self.list.append(var)

        pass