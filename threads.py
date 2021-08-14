from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class Threads(QObject):
    finished = pyqtSignal()
    process = pyqtSignal()
    def stop(self):
        self._timer.stop()
        self.finished.emit()

        pass