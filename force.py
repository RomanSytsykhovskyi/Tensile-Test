from serial import Serial

class Force(Serial):
    def getName(self):
        return self.name

    def addData(self, var):
        self.list.append(var)

        pass