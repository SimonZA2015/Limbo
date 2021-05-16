from PySide2.QtCore import Signal, Slot

from Limbo.style import *

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import traceback
import time
import sys


class QCustomQWidget(QWidget):
    def __init__(self, parent=None, ):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.textUpQLabel = QLabel()
        self.textDownQLabel = QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QHBoxLayout()
        self.iconQLabel = QPushButton(QIcon(""), "")
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')
        self.setStyleSheet(styleItemList)

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.textDownQLabel.setText(text[0:10] + "...")

    def setIcon(self, imagePath):
        self.iconQLabel.setIcon(QIcon(imagePath))
        self.iconQLabel.setStyleSheet(styleIconQLabel)


class backgroundView(QGraphicsView):
    def __init__(self, movie):
        super(backgroundView, self).__init__()
        self.movie = movie
        self.display_pixmap = movie.currentPixmap()
        self.setStyleSheet('QGraphicsView {background-color: rgb(0,0,0);}')

    def paintEvent(self, event):
        self.display_pixmap = self.movie.currentPixmap().scaled(self.my_size)
        painter = QPainter()
        painter.begin(self.viewport())
        painter.fillRect(event.rect(), self.palette().color(QPalette.Window))
        x = (self.width() - self.display_pixmap.width()) / 2
        y = (self.height() - self.display_pixmap.height()) / 2
        painter.drawPixmap(x, y, self.display_pixmap)
        painter.end()

    def resizeEvent(self, event):
        self.my_size = event.size()


class QLabelScroll(QScrollArea):  # contructor
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        # making widget resizable
        self.setWidgetResizable(True)

        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QVBoxLayout(content)

        # creating label
        self.label = QLabel(content)

        # setting alignment to the text
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # making label multi-line
        self.label.setWordWrap(True)

        self.label.setStyleSheet("QLabel{background-color: white;  border: 0px white;" "border-radius: 10px;}")
        # adding label to the layout
        lay.addWidget(self.label)
        self.setStyleSheet(styleScroll)

        # the setText method

    def setText(self, text):
        # setting text to the label
        self.label.setText(text)


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)


class Potoki(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Potoki, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


def getPath(relative_path):
    import os, sys

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.getcwd()
    return os.path.join(base_path, relative_path)
