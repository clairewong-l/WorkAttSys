# 导入界面处理包
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# 导入登录界面
from ui import information


class InformationDialog(QWidget, information.Ui_information):
    def __init__(self, parent=None):
        super(InformationDialog, self).__init__(parent)
        self.setupUi(self)
        # self.logo = QIcon('./imgs/icon_app.jpg')
        self.setWindowTitle(' ')
        # self.setWindowIcon(self.logo)
