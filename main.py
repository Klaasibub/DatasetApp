from MainWindow import QtWidgets, Mainwindow
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Mainwindow()
    widget.show()
    sys.exit(app.exec_())
