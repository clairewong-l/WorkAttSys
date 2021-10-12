import sys

import requests
import json
# 导入界面处理包
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# 导入全局变量
from util.GlobalVar import LOGIN_STATUS, LOCAL_USER, BTN_FONT
# 导入登录界面
from ui import login as LoginUI
from util.RegisterDialog import RegisterDialog


class LoginDialog(QWidget, LoginUI.Ui_Form):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        self.setupUi(self)
        self.logo = QIcon('./imgs/icon_app.jpg')
        self.setWindowTitle('智慧考勤系统')
        self.setWindowIcon(self.logo)

        fonID = QtGui.QFontDatabase.addApplicationFont(BTN_FONT)
        loadedFontFamilies = QFontDatabase.applicationFontFamilies(fonID)
        self.register_Button.setFont(QFont(loadedFontFamilies[0], 13))
        self.login_Button.setFont(QFont(loadedFontFamilies[0], 13))
        self.cancel_Button.setFont(QFont(loadedFontFamilies[0], 13))
        self.register_Button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_Button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_Button.setCursor(Qt.CursorShape.PointingHandCursor)

        # 设置密码不显示
        self.pwd_lineEdit.setEchoMode(QLineEdit.Password)
        # 登录按钮连接函数
        self.login_Button.clicked.connect(self.post_login)
        self.login_Button.setShortcut(QKeySequence(Qt.Key_Enter))
        # 注册按钮连接函数
        self.register_Button.clicked.connect(self.register_Button_clicked)
        # 回车登录
        # self.pwd_lineEdit.returnPressed.connect(self.post_login)
        # 取消按钮
        self.cancel_Button.clicked.connect(self.close)

        # self.key = QShortcut(QKeySequence(Qt.Key_Return), self)
        # self.key.activated.connect(self.post_login)

        # 初始化填入本地id和密码
        self.load()

    def load(self):
        # 初始化写入id和密码
        f = open('local.json', 'r')
        content = f.read()
        if content != '':
            a = json.loads(content)
            self.user_lineEdit.setText(a['id'])
            self.pwd_lineEdit.setText(a['password'])
            if len(a["password"]) != 0:
                self.chk_psw.setChecked(True)
            else:
                self.chk_psw.setChecked(False)
            QApplication.processEvents()
        f.close()

    def handle_click(self, status):
        # self.load()
        if status == 0:
            if not self.isVisible():
                self.show()
                self.load()

    def post_login(self):
        LOGIN_STATUS[0] = 0
        user_id = self.user_lineEdit.text()
        psw = self.pwd_lineEdit.text()
        form_data = {
            'id': user_id,
            'password': psw
        }
        response = requests.post("http://127.0.0.1:5000/user/login", data=form_data)
        c = response.json()
        LOGIN_STATUS[0] = c['status']
        self.label_login_msg.setText(c['msg'])
        if LOGIN_STATUS[0] == 1:
            for s in (
                    'id', 'name', 'pwd', 'phone', 'sex', 'company', 'head_img', 'department', 'annual_freedays',
                    'flag'):
                if c['data'][s] is None:
                    LOCAL_USER[s] = '\\'
                    print(type(LOCAL_USER[s]), s, LOCAL_USER[s])
                else:
                    LOCAL_USER[s] = c['data'][s]
                    print(type(LOCAL_USER[s]), s, LOCAL_USER[s])
            LOCAL_USER['head_img'] = "./headimgs/" + LOCAL_USER['id'] + "/head_img.png"  # 本地查看头像
            # 读取local文件
            local = open('local.json', 'r')
            content = local.read()
            if content != '':
                local_status = json.loads(content)
            else:
                local_status = {}
            local.close()

            local_status["id"] = form_data["id"]
            # 未勾选记住密码
            if not self.chk_psw.isChecked():
                local_status["password"] = ''
            else:
                local_status["password"] = form_data['password']

            # 写入文件
            print("local_status",local_status)
            local = open('local.json', 'w')
            b = json.dumps(local_status)
            local.write(b)
            local.close()

            self.label_login_msg.setText('')
            self.close()

    windowList = []

    def register_Button_clicked(self):
        myregister = RegisterDialog()
        self.windowList.append(myregister)
        myregister.handle_click()
        myregister.Dialog.register_Button.clicked.connect(self.load)
        myregister.key.activated.connect(self.load)
