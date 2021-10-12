import sys
# 导入界面处理包
from PyQt5.QtWidgets import *

# 导入全局变量
from util.GlobalVar import LOGIN_STATUS, LOCAL_USER, BTN_FONT, NEW_APP, APP_ID, CHECK_IN_NOTE
# 导入界面文件
from MainwindowDialog import MainWindow
from util.ApplicationDialog import ApplicationDialog
from util.FaceCollectingDialog import FaceCollectingDialog
from util.LoginDialog import LoginDialog
from util.RegisterDialog import RegisterDialog
from util.ChangepwdDialog import ChangepwdDialog
from util.MsgBoxDialog import QMsgBox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mymainwindow = MainWindow()
    mylogin = LoginDialog()
    mylogin.login_Button.clicked.connect(mymainwindow.handle_click)
    # mylogin.key.activated.connect(mymainwindow.handle_click)    # 回车登录
    mymainwindow.ui.logout.triggered.connect(lambda: mylogin.handle_click(LOGIN_STATUS[0]))
    mylogin.show()

    # myapplication = ApplicationDialog()
    # myfacecollecting = FaceCollectingDialog()
    # myregister = RegisterDialog()
    # mychangepwd = ChangepwdDialog()

    # mymainwindow.ui.bt_open_application.clicked.connect(myapplication.handle_click)
    # mymainwindow.ui.bt_open_face_collecting.clicked.connect(myfacecollecting.handle_click)
    # mymainwindow.ui.bt_change_pwd.clicked.connect(mychangepwd.handle_click)
    # mymainwindow.ui.bt_exception.clicked.connect(myapplication.att_excep)
    # 登录页面跳转
    # mylogin.register_Button.clicked.connect(myregister.handle_click)

    # 注册页面
    # myregister.Dialog.bt_open_facecollecting.clicked.connect(myfacecollecting.handle_click)
    # myregister.Dialog.register_Button.clicked.connect(mylogin.load)
    # myregister.key.activated.connect(mylogin.load)
    # 申请提交
    # myapplication.submitButton.clicked.connect(mymainwindow.handle_application)

    sys.exit(app.exec_())