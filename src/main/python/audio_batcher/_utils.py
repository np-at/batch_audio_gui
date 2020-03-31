import os
import subprocess

from PyQt5.QtWidgets import QMessageBox, QFileDialog, QDialog
from PyQt5.uic.properties import QtCore


def FileDialog(directory='', forOpen=True, fmt='', isFolder=False):
    options = QFileDialog.Options()
    # options |= QFileDialog.DontUseNativeDialog
    options |= QFileDialog.DontUseCustomDirectoryIcons
    dialog = QFileDialog()
    dialog.setOptions(options)

    dialog.setFilter(dialog.filter() | QtCore.QDir.Hidden)

    # ARE WE TALKING ABOUT FILES OR FOLDERS
    if isFolder:
        dialog.setFileMode(QFileDialog.DirectoryOnly)
    else:
        dialog.setFileMode(QFileDialog.AnyFile)
    # OPENING OR SAVING
    dialog.setAcceptMode(QFileDialog.AcceptOpen) if forOpen else dialog.setAcceptMode(QFileDialog.AcceptSave)

    # SET FORMAT, IF SPECIFIED
    if fmt != '' and isFolder is False:
        dialog.setDefaultSuffix(fmt)
        dialog.setNameFilters([f'{fmt} (*.{fmt})'])

    # SET THE STARTING DIRECTORY
    if directory != '':
        dialog.setDirectory(str(directory))
    else:
        dialog.setDirectory(os.path.expanduser('~/'))

    if dialog.exec_() == QDialog.Accepted:
        path = dialog.selectedFiles()[0]  # returns a list
        return path
    else:
        return ''


def print_to_output(func):
    def print_helper(self, *args, **kwargs):
        return self.console_output.appendPlainText(func(self, *args, **kwargs))

    return print_helper


def check_presence():
    """
    quick check to see if ffmpeg is installed. Only checks windows/mac
    :return: a tuple: If ffmpeg is available (bool), If chocolatey or homebrew is available (None if neither)
    :rtype: tuple
    """
    ffmpeg_available = subprocess.check_call('ffmpeg')
    avail_package_manager = None
    if os.name == "Darwin":
        if subprocess.check_call('brew'):
            avail_package_manager = 'brew'

    if os.name == "Windows":
        if subprocess.check_call('choco'):
            avail_package_manager = 'choco'

    return ffmpeg_available, avail_package_manager


def ConfirmationDialog(body_text: str, delegate_fxn, confirmation_title: str = "Confirm Action"):
    """
    # Method: exitActionProcedure.
    # Description: The procedure for closing the application and all the opened files.
    """
    # Create a confirmation dialog asking for permission to quit the application:
    box = QMessageBox()
    box.setIcon(QMessageBox.Question)
    # box.setWindowIcon(QIcon('..\\icons\\desktopIcons\\main.png'))
    box.setWindowTitle(confirmation_title)
    box.setText(body_text)
    box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    box.setDefaultButton(QMessageBox.No)
    button_yes = box.button(QMessageBox.Yes)
    button_yes.setText("Continue")
    button_no = box.button(QMessageBox.No)
    button_no.setText("Cancel")
    box.exec_()

    # Execute the delegate function
    if box.clickedButton() == button_yes:
        return delegate_fxn()
