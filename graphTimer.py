from threads import Threads, QTimer

class GraphTimer(Threads):
    def start(self):
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.process)
        self._timer.start(1000)

        pass