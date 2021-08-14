from threads import Threads, QTimer

class ComPortsTimer(Threads):
    def start(self):
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.process)
        self._timer.start(100)

        pass