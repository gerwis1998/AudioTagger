import sys

from PyQt5.QtWidgets import QApplication, QWidget


def showversion():
    print("Author: Gerard Wisniewski")
    print("AudioTagger v1.0")


def showhelp():
    print("tak")


def showui():
    w.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    width = 500
    height = 500
    w.resize(height, width)
    w.setWindowTitle("AudioTagger")
    print(sys.argv)
    directory = sys.argv[0]
    if len(sys.argv) == 1:
        showui()
    elif sys.argv[1] == "-v":
        showversion()
    elif sys.argv[1] == "-h":
        showhelp()

sys.exit(app.exec_())
