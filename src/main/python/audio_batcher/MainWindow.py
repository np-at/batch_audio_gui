import logging
import os
import re
import shlex
import sys
from subprocess import Popen, PIPE

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QLabel, QComboBox

from . import _utils
from ._utils import ConfirmationDialog, FileDialog

class Window(QWidget):
    def __init__(self, flags, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)
        self.fileoutput_options = ['.mp3', '.aac', '.flac', '.wav']

        self.convert_to_format = self.fileoutput_options[0]
        self.current_arg_list = None
        self.title = "PyQt5 Plain TextEdit"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300

        self.InitWindow()

    def print_to_output(self, output: str = None):
        if output is None:
            self.console_output.appendPlainText("")
        else:
            self.console_output.appendPlainText(output)

    def InitWindow(self):
        # self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        vbox = QVBoxLayout()
        plainText = QPlainTextEdit()
        plainText.setPlaceholderText("")

        plainText.setReadOnly(True)

        text = "Welcome!"

        plainText.appendPlainText(text)

        plainText.setUndoRedoEnabled(False)
        self.console_output = plainText

        self.combo_label = QLabel("Output type")
        combo = QComboBox()
        combo.addItems(self.fileoutput_options)
        combo.move(50, 50)
        combo.activated[str].connect(self.on_combo_activated)
        self.combo = combo
        self.combo_label.move(50, 150)

        btn_run = QtWidgets.QPushButton()
        btn_run.setText("Run")
        # btn_run.setEnabled(False)
        btn_run.setGeometry(QtCore.QRect(150, 100, 75, 23))
        btn_run.setObjectName("btn_run")
        btn_run.clicked.connect(self.start_this)
        self.btnRun = btn_run

        btn_choose_directory = QtWidgets.QPushButton()
        btn_choose_directory.setText("Choose Folder")
        btn_choose_directory.setEnabled(True)
        btn_choose_directory.setGeometry(QtCore.QRect(100, 100, 50, 20))
        btn_choose_directory.clicked.connect(self.openDirDialog)
        self.btn_choose_directory = btn_choose_directory

        vbox.addWidget(self.combo_label)
        vbox.addWidget(self.combo)
        vbox.addWidget(self.btnRun)
        vbox.addWidget(self.btn_choose_directory)
        vbox.addWidget(self.console_output)

        self.setLayout(vbox)

        self.show()


    def on_combo_activated(self, text):
        self.convert_to_format = text

    def openDirDialog(self):
        v = FileDialog(isFolder=True)
        if v == '':
            sys.exit()
        else:
            print(v)
            self.btnRun.setEnabled(True)
            self.target_directory = v

    def start_this(self):
        rl, fl = self.conversion_prep()
        fl_display = '\n'.join(fl)
        ConfirmationDialog(body_text=f'Confirm you would like to convert these: \n' + f' {fl_display}',
                           delegate_fxn=self._run_conversion)

    def _run_conversion(self):
        for i in self.current_arg_list:
            try:
                self.run_ffmpeg(i)
            except Exception as ex:
                logging.exception(ex)

    def conversion_prep(self):
        extension_re = re.compile(r'(?:.+)(\.[a-zA-Z]{3}$)')

        if self.target_directory is None:
            raise
        runlist = list()
        filelist = list()
        for root, dirs, files in os.walk(self.target_directory):
            for file in files:
                f = os.path.join(root, file)
                filelist.append(f)
                m = extension_re.findall(f)
                current_extension = m[0]
                argstring = f'ffmpeg -i {f} {f.replace(current_extension, self.convert_to_format)}'
                runlist.append(argstring)
        self.current_arg_list = runlist
        return runlist, filelist

    def run_ffmpeg(self, arg_string: str):
        args = shlex.split(arg_string)
        p = Popen(args, shell=False, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        self.console_output.appendPlainText(out.decode('utf-8'))
        self.console_output.appendPlainText(err.decode('utf-8'))
        p.wait()