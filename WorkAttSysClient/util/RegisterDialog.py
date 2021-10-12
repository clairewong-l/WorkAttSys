# encoding:utf-8
# coding: UTF-8
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui import register as RegisterUI
from util.MsgBoxDialog import QMsgBox
from util.FaceCollectingDialog import FaceCollectingDialog
import requests
import json

from util.GlobalVar import LOCAL_USER


class RegisterDialog(QWidget,RegisterUI.Ui_Register_Form):
    def __init__(self, parent=None):
        # super()构造器方法返回父级的对象。__init__()方法是构造器的一个方法。
        super().__init__()

        self.Dialog = RegisterUI.Ui_Register_Form()
        self.Dialog.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)

        # self.register_Button.clicked.connect(self.on_button_register)
        self.logo = QIcon('./imgs/icon_app.jpg')
        self.setWindowTitle('智慧考勤系统')
        self.setWindowIcon(self.logo)
        # 按键槽函数
        self.Dialog.register_Button.clicked.connect(self.post_register)
        self.Dialog.register_Button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.Dialog.bt_open_facecollecting.setCursor(Qt.CursorShape.PointingHandCursor)
        # 人脸采集
        self.Dialog.bt_open_facecollecting.clicked.connect(self.open_facecollecting_clicked)
        # 回车快捷键
        self.key = QShortcut(QKeySequence(Qt.Key_Return), self)
        self.key.activated.connect(self.post_register)
        # 设置密码不显示
        self.Dialog.pwd_lineEdit.setEchoMode(QLineEdit.Password)
        self.Dialog.pwd_2_lineEdit.setEchoMode(QLineEdit.Password)



    def handle_click(self):
        if not self.isVisible():
            print("register!!!")
            self.show()

    # 注册按钮的槽函数
    def post_register(self):
        # global LOGIN_STATUS

        user_id = self.Dialog.user_lineEdit.text()
        pwd = self.Dialog.pwd_lineEdit.text()
        pwd_2 = self.Dialog.pwd_2_lineEdit.text()
        name = self.Dialog.name_lineEdit.text()
        phone = self.Dialog.phone_lineEdit.text()
        sex = self.Dialog.sex_comboBox.currentText()
        form_data = {
            'id': user_id,
            'pwd': pwd,
            'pwd_2': pwd_2,
            'name': name,
            'phone': phone,
            'sex': sex
        }
        response = requests.post("http://127.0.0.1:5000/user/register", data=form_data)
        c = response.json()
        if c['status'] == 0:
            self.Dialog.label_register_msg.setText(c['msg'])
        elif c['status'] == 1:
            QMsgBox.showMsg(c['msg'])
            #QMessageBox.information(self, '服务器数据提示', c['msg'], QMessageBox.Ok)
            local = open('local.json', 'w')
            a = {
                'id': user_id,
                'password': pwd
            }
            b = json.dumps(a)
            local.write(b)
            local.close()
            self.close()

    windowList = []
    def open_facecollecting_clicked(self):
        LOCAL_USER['id'] = self.Dialog.user_lineEdit.text()
        print(LOCAL_USER['id'])
        myFaceCollectingDialog = FaceCollectingDialog()
        self.windowList.append(myFaceCollectingDialog)
        myFaceCollectingDialog.handle_click()