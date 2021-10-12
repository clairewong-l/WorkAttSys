from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QIcon, QPixmap
from PyQt5.QtCore import QCoreApplication, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QInputDialog
from ui import checkpwd as checkpwdUi

import threading
import cv2
import imutils
import os
import sys



class CheckpwdDialog(QWidget,checkpwdUi.Ui_checkpwdForm):
    def __init__(self,parent=None):
        # super()构造器方法返回父级的对象。__init__()方法是构造器的一个方法。
        super(CheckpwdDialog,self).__init__(parent)
        self.setupUi(self)
        self.logo = QIcon('./imgs/icon_app.jpg')
        self.setWindowTitle('智慧考勤系统')
        self.setWindowIcon(self.logo)


    def handle_click(self):
        if not self.isVisible():
            self.show()