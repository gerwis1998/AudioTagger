import glob
import os
import re
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLineEdit, QPushButton


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'AudioTagger'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.openFileNamesDialog()
        sys.exit(app.exec_())

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        temp, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                               "All Files (*);;Python Files (*.py)", options=options)
        if len(temp) != 0:
            for file in temp:
                files.append(file)
            self.openRegexDialog()

    def openRegexDialog(self):
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.title = "Type in your regex"
        self.resize(400, 150)
        self.textbox.resize(280, 40)
        self.button = QPushButton('Confirm', self)
        self.button.move(20, 80)
        self.button.clicked.connect(self.on_click)
        self.show()

    def on_click(self):
        textboxValue = self.textbox.text()
        regexsplit = textboxValue.split('/')
        if len(regexsplit) == 1:
            print("Invalid regex")
            exit(1)
        if regexsplit[1] == "author":
            first = "author"
        elif regexsplit[1] == "title":
            first = "title"
        else:
            print("Invalid regex")
            exit(1)
        regexbefore = regexsplit[0]
        regexmid = regexsplit[2]
        regexafter = regexsplit[4]
        size = len(files)
        for file in files:
            temp = file.split('/')
            file = temp[len(temp) - 1]
            start = re.findall(regexbefore, file)[0]  # TODO
            mid = re.findall(regexmid, file)[0]
            end = re.findall(regexafter, file)[0]
            if len(mid) != 0:
                if len(start) != 0:
                    author = file.split(start)[1].split(mid)[0]
                else:
                    author = file.split(mid)[0]
                if len(end) != 0:
                    title = file.split(mid)[1].split(end)[0]
                else:
                    title = file.split(mid)[1]
            else:
                continue
            if first == "title":
                temp = title
                title = author
                author = temp
            os.system('id3v2 -t "' + title + '" -a "' + author + '" "' + file + '"')


def addtags():
    regexsplit = regex.split('/')
    if len(regexsplit) == 1:
        print("Invalid regex")
        exit(1)
    if regexsplit[1] == "author":
        first = "author"
    elif regexsplit[1] == "title":
        first = "title"
    else:
        print("Invalid regex")
        exit(1)
    regexbefore = regexsplit[0]
    regexmid = regexsplit[2]
    regexafter = regexsplit[4]
    regexfind = regexbefore + "*" + regexmid + "*" + regexafter
    os.chdir(directory)
    print("Songs tagged:")
    size = len(glob.glob(regexfind))
    for file in glob.glob(regexfind):
        print(file)
        start = re.findall(regexbefore, file)[0]
        mid = re.findall(regexmid, file)[0]
        end = re.findall(regexafter, file)[0]
        if len(mid) != 0:
            if len(start) != 0:
                author = file.split(start)[1].split(mid)[0]
            else:
                author = file.split(mid)[0]
            if len(end) != 0:
                title = file.split(mid)[1].split(end)[0]
            else:
                title = file.split(mid)[1]
        else:
            continue
        if first == "title":
            temp = title
            title = author
            author = temp
        os.system('id3v2 -t "' + title + '" -a "' + author + '" "' + file + '"')
    exit(0)


def showversion():
    print("Author: Gerard Wisniewski")
    print("AudioTagger v1.0")
    exit(0)


def showhelp():
    print("AudioTagger can be used in both terminal and gui version\n"
          'For gui version use "python3 AudioTagger.py" without any parameters\n'
          'For terminal version use "python3 AudioTagger.py -r" or "python3 AudioTagger.py -r regex"\n'
          'This script uses pythons\' basic regular expression rules\n'
          'Example: for files like 1.Author - Title.mp3 regex would be:\n'
          '[0-9][.]/author/ - /title/[.]mp3')
    exit(0)


def showui():
    ex.show()


if __name__ == '__main__':
    # screen = app.primaryScreen()
    # size = screen.size()
    # w = QWidget()
    # w.setLayout(QGridLayout())
    # width = 500
    # height = 500
    # w.resize(height, width)
    # w.move(size.width() / 2 - width / 2, size.height() / 2 - height / 2)
    # w.setWindowTitle("AudioTagger")
    files = []
    app = QApplication(sys.argv)
    ex = App()
    directory = os.getcwd()
    if len(sys.argv) == 1:
        showui()
    elif sys.argv[1] == "-v":
        showversion()
    elif sys.argv[1] == "-h":
        showhelp()
    elif sys.argv[1] == "-r" and len(sys.argv) == 2:
        regex = input("Write your regex: ")
        addtags()
    elif sys.argv[1] == "-r" and len(sys.argv) == 3:
        regex = sys.argv[2]
        addtags()
    else:
        print("Invalid arguments. See -h for help")
        exit(1)
    sys.exit(app.exec_())
# /author/ - /title/
