from window import MainWindow, QtWidgets

import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()

    #end the code
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()