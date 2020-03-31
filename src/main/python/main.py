import sys

from audio_batcher.MainWindow import Window
from fbs_runtime.application_context.PyQt5 import ApplicationContext

if __name__ == '__main__':
    appctxt = ApplicationContext()
    window = Window(flags=None)
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
