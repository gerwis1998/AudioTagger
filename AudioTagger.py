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
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        temp = QFileDialog.getOpenFileNames(self, "Select Files", "",
                                            "Mp3 Files (*.mp3);;All Files (*)", options=options)
        if len(temp[0]) != 0 and temp is not None:
            for file in temp:
                files.append(file)
            self.openRegexDialog()
        else:
            exit(0)

    def openRegexDialog(self):
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.title = 'Type in your regex'
        self.setWindowTitle(self.title)
        self.resize(400, 120)
        self.textbox.resize(280, 40)
        self.button = QPushButton('Confirm', self)
        self.button.move(20, 80)
        self.button.clicked.connect(self.on_click)
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
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
        for file in files[0]:
            temp = file.split('/')
            filename = temp[len(temp) - 1]
            if len(re.findall(regexbefore, filename)) == 0:
                continue
            start = re.findall(regexbefore, filename)[0]
            if len(re.findall(regexmid, filename)) == 0:
                continue
            mid = re.findall(regexmid, filename)[0]
            if len(re.findall(regexafter, filename)) == 0:
                continue
            end = re.findall(regexafter, filename)[0]
            if len(mid) != 0:
                if len(start) != 0:
                    author = filename.split(start)[1].split(mid)[0]
                else:
                    author = filename.split(mid)[0]
                if len(end) != 0:
                    title = filename.split(mid)[1].split(end)[0]
                else:
                    title = filename.split(mid)[1]
            else:
                continue
            if first == "title":
                temp = title
                title = author
                author = temp
            os.system('id3v2 -t "' + title + '" -a "' + author + '" "' + file + '"')
        exit(0)


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
    os.chdir(directory)
    print("Songs tagged:")
    size = len(glob.glob("*"))
    for file in glob.glob("*"):

        if len(re.findall(regexbefore, file)) == 0:
            continue
        start = re.findall(regexbefore, file)[0]
        if len(re.findall(regexmid, file)) == 0:
            continue
        mid = re.findall(regexmid, file)[0]
        if len(re.findall(regexafter, file)) == 0:
            continue
        end = re.findall(regexafter, file)[0]
        print(file)
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
    files = []
    app = QApplication(sys.argv)
    directory = os.getcwd()
    if len(sys.argv) == 1:
        ex = App()
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
