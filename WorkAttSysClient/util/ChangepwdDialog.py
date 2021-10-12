from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui import changepwd as changepwdUi
from util.MsgBoxDialog import QMsgBox

import threading
import cv2
import imutils
import os
import sys
import requests
import json

from util.GlobalVar import LOCAL_USER, BTN_FONT


class ChangepwdDialog(QWidget, changepwdUi.Ui_changepwdForm):
    def __init__(self, parent=None):
        # super()构造器方法返回父级的对象。__init__()方法是构造器的一个方法。
        super(ChangepwdDialog, self).__init__(parent)
        self.setupUi(self)
        self.logo = QIcon('./imgs/icon_app.jpg')
        self.setWindowTitle('智慧考勤系统')
        self.setWindowIcon(self.logo)

        self.setWindowModality(Qt.ApplicationModal)

        self.bt_changepwd.clicked.connect(self.change_password)
        self.bt_cancle.clicked.connect(self.close)
        #密码不显示
        self.newpwdEdit2.setEchoMode(QLineEdit.Password)
        self.newpwdEdit.setEchoMode(QLineEdit.Password)
        self.oldpwdEdit.setEchoMode(QLineEdit.Password)

        self.bt_changepwd.setCursor(Qt.CursorShape.PointingHandCursor)
        self.bt_cancle.setCursor(Qt.CursorShape.PointingHandCursor)

        fonID = QtGui.QFontDatabase.addApplicationFont(BTN_FONT)
        loadedFontFamilies = QFontDatabase.applicationFontFamilies(fonID)
        self.bt_changepwd.setFont(QFont(loadedFontFamilies[0], 13))
        self.bt_cancle.setFont(QFont(loadedFontFamilies[0], 13))

    def handle_click(self):
        if not self.isVisible():
            self.show()

    # 修改密码页面确认按钮的槽函数
    def change_password(self):
        user_id = LOCAL_USER['id']
        psw = LOCAL_USER['pwd']
        old_psw = self.oldpwdEdit.text()
        new_psw = self.newpwdEdit.text()
        new_psw_2 = self.newpwdEdit2.text()
        if old_psw == psw:
            if new_psw == new_psw_2:
                if len(new_psw) == 0:
                    QMsgBox.showMsg('请输入新密码')
                    #QMessageBox.information(self, '提示', "请输入新密码", QMessageBox.Ok)
                else:
                    LOCAL_USER['pwd'] = new_psw
                    form_data = {
                        'id': user_id,
                        'new_psw': new_psw
                    }
                    response = requests.put("http://127.0.0.1:5000/user/staffDetail/changePsw", data=form_data)
                    c = response.text
                    QMsgBox.showMsg(c)
                    #QMessageBox.information(self, '服务器数据提示', c, QMessageBox.Ok)
                    self.close()
            else:
                QMsgBox.showMsg('两次密码输入不同，请检查后重新输入')
                #QMessageBox.information(self, '提示', "两次密码输入不同，请检查后重新输入", QMessageBox.Ok)
        else:
            QMsgBox.showMsg('密码错误，请检查后重新输入')
            #QMessageBox.information(self, '提示', "密码错误，请检查后重新输入", QMessageBox.Ok)
