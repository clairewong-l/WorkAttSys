import datetime
import sys
import os
import requests
import json
import cv2
from cv2 import dnn
import imutils
import numpy as np
import chinese_calendar as ch_cal

# 导入界面处理包
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# 导入全局变量
from util.GlobalVar import LOGIN_STATUS, LOCAL_USER, BTN_FONT, NEW_APP, APP_ID, CHECK_IN_NOTE, rootdir
# 导入界面文件
from ui import mainwindow as MainWindowUI
from util.ApplicationDialog import ApplicationDialog
from util.FaceCollectingDialog import FaceCollectingDialog
from util.InformationDialog import InformationDialog
from util.LoginDialog import LoginDialog
from util.RegisterDialog import RegisterDialog
from util.ChangepwdDialog import ChangepwdDialog
from util.MsgBoxDialog import QMsgBox
# 导入眨眼检测类
from util.BlinksDetectThread import BlinksDetectThread
# from backports.datetime_fromisoformat import MonkeyPatch
from threading import Thread

# 添加当前路径到环境变量
from util.faceDataUtil import updateFaceData, localSaveMatrix, getFacePosition, getFaceData, localReadMatrix, \
    getSimilarity, recognizeExpression

sys.path.append(os.getcwd())


class MainWindow(QtWidgets.QMainWindow):
    # 类构造函数
    def __init__(self):
        # super()构造器方法返回父级的对象。__init__()方法是构造器的一个方法。
        super().__init__()

        self.startThread = BlinksDetectThread()
        self.ui = MainWindowUI.Ui_MainWindow()
        self.ui.setupUi(self)
        # self.initCalender()

        # ###################### 相对路径 ######################
        # 初始化label显示的(deep grey)背景
        self.bkg_camera = QPixmap('./imgs/camera_bkg.png')
        # 设置主窗口的logo
        self.logo = QIcon('./imgs/icon_app.jpg')
        # OpenCV深度学习人脸检测器的路径
        self.detector_path = "./model_face_detector"
        # OpenCV深度学习面部嵌入模型的路径
        # self.embedding_model = "./model_facenet/openface_nn4.small2.v1.t7"
        # 训练模型以识别面部的路径
        # self.recognizer_path = "./saved_weights/recognizer.pickle"

        # ###################### 窗口初始化 ######################
        # 设置窗口名称和图标
        self.setWindowTitle('智慧考勤系统')
        self.setWindowIcon(self.logo)
        self.ui.staffcalendar.setLocale(QLocale(QLocale.Chinese))
        # 设置初识背景图片
        # self.ui.label_staff_img.setPixmap(self.bkg_camera.scaled(
        # self.ui.label_staff_img.height(), self.ui.label_staff_img.height()))
        # 设定按钮字体
        fonID = QtGui.QFontDatabase.addApplicationFont(BTN_FONT)
        loadedFontFamilies = QFontDatabase.applicationFontFamilies(fonID)
        self.ui.bt_checkin.setFont(QFont(loadedFontFamilies[0], 26))
        self.ui.bt_change_pwd.setFont(QFont(loadedFontFamilies[0], 15))
        self.ui.bt_open_checkin.setFont(QFont(loadedFontFamilies[0], 15))
        self.ui.bt_open_application.setFont(QFont(loadedFontFamilies[0], 15))
        self.ui.bt_open_face_collecting.setFont(QFont(loadedFontFamilies[0], 20))

        self.ui.bt_checkin.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.bt_exception.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.bt_change_pwd.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.bt_open_checkin.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.bt_open_application.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.bt_open_face_collecting.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.bt_staffInformation.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.bt_open_camera.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.bt_staffInformation_box_2.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.bt_checkin_box.setCursor(Qt.CursorShape.PointingHandCursor)
        # # 初始化日期显示
        # self.ui.label_selected_data.setText(self.ui.staffcalendar.selectedDate().toString('yyyy-MM-dd'))

        # ###################### 摄像头初始化 ######################
        # 初始化摄像头，默认调用系统自带摄像头
        self.url = 0
        # self.url = 1 # 如果要调用摄像头1，则设置为1，适用于：笔记本外接USB摄像头
        self.cap = cv2.VideoCapture()
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
        # self.cap.set(cv2.CAP_PROP_FPS, 20)

        # ###################### 按键的槽函数 ######################
        # 打卡页面-摄像头按键连接函数
        self.ui.bt_open_camera.clicked.connect(self.open_camera)
        # 打卡页面-打卡按键连接函数，自动开始人脸检测和活体检测
        self.ui.bt_checkin.clicked.connect(self.auto_control)
        # self.ui.bt_checkin.clicked.connect(self.post_check)
        # self.ui.bt_checkin.clicked.connect(self.blinks_thread)
        # 打卡页面-个人信息按键连接函数
        self.ui.bt_staffInformation.clicked.connect(self.show_staff_information)
        self.ui.bt_staffInformation.clicked.connect(self.showCalenderColor)
        # 个人信息页面-打卡按键连接函数
        self.ui.bt_open_checkin.clicked.connect(self.show_checkin)
        # 查看打卡记录页面-显示日期
        self.ui.staffcalendar.selectionChanged.connect(self.show_date_att)
        self.ui.staffcalendar.currentPageChanged.connect(self.showCalenderColor)
        # 查看公告及消息记录
        self.ui.appWidget.currentChanged.connect(self.show_msg_rec)

        # （toolBar功能）
        # 登出
        self.ui.logout.triggered.connect(self.close)
        # 查看信息
        self.ui.information.triggered.connect(self.information_triggered)
        # 刷新
        self.ui.actionrefresh.triggered.connect(lambda: self.handle_click(1))

        # 修改密码
        self.ui.bt_change_pwd.clicked.connect(self.change_pwd_clicked)
        # 人脸采集
        self.ui.bt_open_face_collecting.clicked.connect(self.open_facecollecting_clicked)
        # 提交申请
        self.ui.bt_open_application.clicked.connect(lambda: self.open_application_clicked(1))
        self.ui.bt_exception.clicked.connect(lambda: self.open_application_clicked(2))

        # 设置区分打开摄像头还是人脸识别的标识符
        self.switch_bt = 0

        # 右击实现上传或更换头像
        self.ui.label_staff_img.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.label_staff_img.customContextMenuRequested.connect(self.rightMenuShow)

    # 添加右键菜单
    def rightMenuShow(self, pos):
        menu = QMenu(self)
        menu.addAction(QAction('更换头像', menu))
        menu.triggered.connect(self.menuSlot)
        menu.exec_(QCursor.pos())

    def menuSlot(self, act):
        if act.text() == "更换头像":  # 更换头像
            imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
            jpg = QtGui.QPixmap(imgName).scaled(self.ui.label_staff_img.width(), self.ui.label_staff_img.height())
            self.ui.label_staff_img.setPixmap(jpg)
            self.ui.label_staff_img.setScaledContents(True)
            # 头像存入本地
            imgpath = "./headimgs/" + LOCAL_USER['id']
            if (not os.path.isdir(imgpath)):
                os.makedirs(imgpath)
            jpg.save(imgpath + "/head_img.png")

    # 修改日历显示 使所有日期均为黑色
    def initCalender(self):
        first_day = QtCore.QDate()
        first_day.setDate(self.ui.staffcalendar.yearShown() - 10, self.ui.staffcalendar.monthShown(), 1)
        days = 50000
        cmd_fmt = QtGui.QTextCharFormat()
        brush = QtGui.QBrush()
        for i in range(days):
            brush.setColor(QtGui.QColor('Black'))
            cmd_fmt.setForeground(brush)
            self.ui.staffcalendar.setDateTextFormat(first_day.addDays(i), cmd_fmt)

    # 根据打卡记录显示颜色
    def showCalenderColor(self):
        month = self.ui.staffcalendar.monthShown()
        year = self.ui.staffcalendar.yearShown()
        print(month)
        staff_id = LOCAL_USER['id']
        form_data = {
            "staff_id": staff_id,
            "month": month,
            "year": year
        }
        response = requests.post("http://127.0.0.1:5000/user/staffDetail/showCalenderColor", data=form_data)
        c = response.json()
        data = c["data"]
        deduct_pay = c["deduct_pay"]
        absent_day = c["absent_day"]
        self.ui.label_deduct_pay.setText('-'+deduct_pay+' 元')
        self.ui.label_absent_day.setText(str(absent_day)+' 天')
        for i in range(c["num"]):
            status = data[f"{i}"]["status"]
            # MonkeyPatch.patch_fromisoformat()
            date = datetime.date.fromisoformat(data[f"{i}"]["date"])
            if status == 1:
                cmd_fmt = QtGui.QTextCharFormat()
                brush1 = QtGui.QBrush()
                brush1.setColor(QtGui.QColor('#9DFACB'))
                cmd_fmt.setForeground(brush1)
                cmd_fmt.setFontUnderline(True)
                self.ui.staffcalendar.setDateTextFormat(date, cmd_fmt)
            elif status == 0:
                cmd_fmt = QtGui.QTextCharFormat()
                brush1 = QtGui.QBrush()
                brush1.setColor(QtGui.QColor('#FA8678'))
                cmd_fmt.setForeground(brush1)
                cmd_fmt.setFontUnderline(True)
                self.ui.staffcalendar.setDateTextFormat(date, cmd_fmt)
        '''
        if c['status'] == 1:
            list = c['data']['recs']
            for i in list:

                y = int((i['check_time'])[0:4])
                if (i['check_time'])[5:6] == '0':
                    m = int((i['check_time'])[6:7])
                else:
                    m = int((i['check_time'])[5:7])
                if (i['check_time'])[8:9] == '0':
                    d = int((i['check_time'])[9:10])
                else:
                    d = int((i['check_time'])[8:10])
                date = QtCore.QDate()
                date.setDate(y, m, d)
                if i['status'] == 1 and i['status'] == 5:  # 设置为绿色
                    cmd_fmt = QtGui.QTextCharFormat()
                    brush = QtGui.QBrush()
                    brush.setColor(QtGui.QColor('Green'))
                    brush1 = QtGui.QBrush()
                    brush1.setColor(QtGui.QColor('Black'))
                    cmd_fmt.setForeground(brush1)
                    cmd_fmt.setBackground(brush)
                    self.ui.staffcalendar.setDateTextFormat(date, cmd_fmt)
                else:  # 设置为红色
                    cmd_fmt = QtGui.QTextCharFormat()
                    brush = QtGui.QBrush()
                    brush.setColor(QtGui.QColor('Red'))
                    brush1 = QtGui.QBrush()
                    brush1.setColor(QtGui.QColor('Black'))
                    cmd_fmt.setForeground(brush1)
                    cmd_fmt.setBackground(brush)
                    self.ui.staffcalendar.setDateTextFormat(date, cmd_fmt)

        else:
            print(c['msg'])
        '''

    def handle_click(self, if_refresh):
        page1, page2, page3 = 0, 0, 0
        if if_refresh == 1:
            page1 = self.ui.stackedWidget.currentIndex()
            page2 = self.ui.infoWidget.currentIndex()
            page3 = self.ui.appWidget.currentIndex()
        if LOGIN_STATUS[0] == 1:
            self.handle_login_click()
            if if_refresh==1:
                self.ui.stackedWidget.setCurrentIndex(page1)
                self.ui.infoWidget.setCurrentIndex(page2)
                self.ui.appWidget.setCurrentIndex(page3)
        if not self.isVisible():
            self.show()

    def handle_login_click(self):
        if LOGIN_STATUS[0] == 1:
            # 清空所有申请
            while self.ui.verticalLayout_9.count() > 1:
                item = self.ui.verticalLayout_9.takeAt(0)
                widget = item.widget()
                widget.deleteLater()
            while self.ui.verticalLayout_11.count() > 1:
                item = self.ui.verticalLayout_11.takeAt(0)
                widget = item.widget()
                widget.deleteLater()
            while self.ui.verticalLayout_13.count() > 1:
                item = self.ui.verticalLayout_13.takeAt(0)
                widget = item.widget()
                widget.deleteLater()
            while self.ui.verticalLayout_15.count() > 1:
                item = self.ui.verticalLayout_15.takeAt(0)
                widget = item.widget()
                widget.deleteLater()
            while self.ui.verticalLayout_17.count() > 1:
                item = self.ui.verticalLayout_17.takeAt(0)
                widget = item.widget()
                widget.deleteLater()

            # 无入职公司时，隐藏异常申请按钮
            if LOCAL_USER['company'] == '\\':
                self.ui.bt_exception.hide()
            else:
                self.ui.bt_exception.show()

            self.user_init()

            # 设置主窗口首页为打卡页
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.infoWidget.setCurrentIndex(0)
            self.ui.appWidget.setCurrentIndex(0)
            # 设置主窗口首页为个人信息：无入职部门、节假日时
            if LOCAL_USER['department'] == '\\' \
                    or ch_cal.is_holiday(datetime.datetime.today()):
                self.ui.stackedWidget.setCurrentIndex(1)
            self.show_date_att()
            # 初始化日历
            self.initCalender()

    # 用户信息初始化
    def user_init(self):
        # 填入用户基本信息
        self.ui.staffIdLabel.setText(LOCAL_USER['id'])
        self.ui.staffNameLabel.setText(LOCAL_USER['name'])
        self.ui.phonelabel.setText(LOCAL_USER['phone'])
        self.ui.staffCompanyLabel.setText(LOCAL_USER['company'])
        self.ui.departmentlabel.setText(LOCAL_USER['department'])
        self.ui.freedayslabel.setText(str(LOCAL_USER['annual_freedays']))

        # 该用户是否已采集人脸
        LOCAL_USER['if_face'] = self.checkFaceData()

        # 获取公司公告
        self.notice()
        self.get_all_application()
        # 初始化头像
        jpg = QPixmap(LOCAL_USER['head_img'])
        self.ui.label_staff_img.setPixmap(jpg)
        self.ui.label_staff_img.setScaledContents(True)

    # 申请信息生成widget在前端显示
    def handle_application(self):
        tab_id = APP_ID[0]
        if_app_right = APP_ID[1]
        if if_app_right == 1:
            if tab_id == 1:
                self.ui.label_new = QtWidgets.QLabel(self.ui.layouts_status_change)
                self.ui.label_new.setObjectName("label_new")
                self.ui.label_new.setText(NEW_APP['app_str'])
                self.ui.verticalLayout_9.insertWidget(0, self.ui.label_new)
                self.ui.infoWidget.setCurrentIndex(1)
                self.ui.appWidget.setCurrentIndex(tab_id)
            elif tab_id == 2:
                self.ui.label_new = QtWidgets.QLabel(self.ui.layouts_out)
                self.ui.label_new.setObjectName("label_new")
                self.ui.label_new.setText(NEW_APP['app_str'])
                self.ui.verticalLayout_11.insertWidget(0, self.ui.label_new)
                self.ui.infoWidget.setCurrentIndex(1)
                self.ui.appWidget.setCurrentIndex(tab_id)
            elif tab_id == 3:
                self.ui.label_new = QtWidgets.QLabel(self.ui.layouts_vaca)
                self.ui.label_new.setObjectName("label_new")
                self.ui.label_new.setText(NEW_APP['app_str'])
                self.ui.verticalLayout_13.insertWidget(0, self.ui.label_new)
                self.ui.infoWidget.setCurrentIndex(1)
                self.ui.appWidget.setCurrentIndex(tab_id)
            elif tab_id == 4:
                self.ui.label_new = QtWidgets.QLabel(self.ui.layouts_back)
                self.ui.label_new.setObjectName("label_new")
                self.ui.label_new.setText(NEW_APP['app_str'])
                self.ui.verticalLayout_15.insertWidget(0, self.ui.label_new)
                self.ui.infoWidget.setCurrentIndex(1)
                self.ui.appWidget.setCurrentIndex(tab_id)
            elif tab_id == 5:
                self.ui.label_new = QtWidgets.QLabel(self.ui.layouts_comp)
                self.ui.label_new.setObjectName("label_new")
                self.ui.label_new.setText(NEW_APP['app_str'])
                self.ui.verticalLayout_17.insertWidget(0, self.ui.label_new)
                self.ui.infoWidget.setCurrentIndex(1)
                self.ui.appWidget.setCurrentIndex(tab_id)
        APP_ID[0] = 0
        APP_ID[1] = 0

    def show_staff_information(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    # 显示对应日历控件的日期 以及对应日期的打卡记录
    def show_date_att(self):
        self.ui.label_selected_data.setText(self.ui.staffcalendar.selectedDate().toString('yyyy-MM-dd'))
        date = self.ui.label_selected_data.text()
        NEW_APP['app_date'] = date
        staff_id = LOCAL_USER['id']

        form_data = {
            "date": date,
            "staff_id": staff_id
        }
        response = requests.post("http://127.0.0.1:5000/user/staffDetail/showAttRec", data=form_data)
        c = response.json()
        if c['status'] == 1:
            self.ui.label_status_on.setText(c['data']['type1'])
            self.ui.label_status_off.setText(c['data']['type2'])
        elif c['status'] == 0:
            self.ui.label_status_on.setText(c['msg'])
            self.ui.label_status_off.setText(c['msg'])

    # 查看公告及申请记录
    def show_msg_rec(self):
        if self.ui.appWidget.currentIndex() == 0:
            self.notice()

    # 查看公告
    def notice(self):
        self.ui.textEdit.clear()
        company = LOCAL_USER['company']
        if company == '\\':
            self.ui.textEdit.setText("未加入公司，无公告记录")
        else:
            form_data = {
                'company': company,
            }
            response = requests.post("http://127.0.0.1:5000/user/staffDetail/showNotice", data=form_data)
            c = response.json()
            if c['status'] == 1:
                list = c['data']['notice']
                for i in list:
                    self.ui.textEdit.append(i['datetime'] + "日公告：\n" + i['info'] + "\n" + "----------")
            if c['status'] == 0:
                self.ui.textEdit.setText(c['msg'])

    # 登录后获取该用户所有申请信息
    def get_all_application(self):
        user_data = {
            'id': f'{LOCAL_USER["id"]}'}
        response = requests.get("http://127.0.0.1:5000/user/getUserApplicationMsg", params=user_data)
        c = response.json()
        for key in c["appNum"]:
            print(c["appNum"][key])
        for key in c["results"]:
            APP_ID[1] = 1
            app_type = c["results"][key]["type"]
            record_time = c["results"][key]["record_time"]
            record_status = c["results"][key]["record_status"]
            if app_type == "签到":
                APP_ID[0] = 1
                date = c["results"][key]["date"]
                worktype = c["results"][key]["worktype"]
                new_att_status = c["results"][key]["new_att_status"]
                app_str = f"申请修改{date} {worktype} 打卡状态为：{new_att_status}   \n申请时间：{record_time} " \
                          f"\n申请状态：{record_status} "
                NEW_APP['app_str'] = app_str
            elif app_type == "入职" or app_type == "离职":
                APP_ID[0] = 5
                company = c["results"][key]["company"]
                app_str = f"申请{app_type}：{company}   \n申请时间：{record_time} \n申请状态：{record_status}"
                NEW_APP['app_str'] = app_str
            elif app_type == "请假":
                APP_ID[0] = 3
                s_date = c["results"][key]["s_date"]
                e_date = c["results"][key]["e_date"]
                days = c["results"][key]["days"]
                app_str = f"申请于{s_date}至{e_date}请假{int(days)}天    \n申请时间：{record_time} \n申请状态：{record_status}"
                NEW_APP['app_str'] = app_str
            elif app_type == "销假":
                APP_ID[0] = 4
                e_date = c["results"][key]["e_date"]
                app_str = f"申请于{e_date}销假    \n申请时间：{record_time}\n申请状态：{record_status}"
                NEW_APP['app_str'] = app_str
            elif app_type == "外派":
                APP_ID[0] = 2
                s_date = c["results"][key]["s_date"]
                e_date = c["results"][key]["e_date"]
                place = c["results"][key]["place"]
                app_str = f"申请于{s_date}至{e_date}外派，地点：{place}  \n申请时间：{record_time}\n申请状态：{record_status} "
                NEW_APP['app_str'] = app_str
            else:
                continue
            self.handle_application()
        self.ui.infoWidget.setCurrentIndex(0)
        self.ui.appWidget.setCurrentIndex(0)

    def open_camera(self):
        # 判断摄像头是否打开
        if not self.cap.isOpened():
            # self.ui.label_logo.clear()
            # 默认打开Windows系统笔记本自带的摄像头，如果是外接USB，可将0改成1
            # self.cap.set(3, 480)
            self.cap.open(self.url)
            self.ui.label_checkin_note.setText("")
            self.show_camera()
        else:
            self.cap.release()
            cv2.destroyAllWindows()
            self.ui.label_camera_layout.clear()
            # self.startThread.terminate()
            print("self.startThread.terminate()")
            self.ui.label_checkin_note.setText("请打开摄像头！")
            # self.ui.label_logo.clear()
            # self.ui.bt_open_camera.setText(u'打开相机')

    def show_camera(self):
        # 如果按键按下
        global embedded, le, recognizer
        if self.switch_bt == 0:
            while self.cap.isOpened():
                # if CHECK_IN_NOTE['ifstop']:return
                # 以BGR格式读取图像
                ret, self.image = self.cap.read()
                # 告诉QT处理来处理任何没有被处理的事件，并且将控制权返回给调用者，让代码变的没有那么卡
                QApplication.processEvents()
                # 将图像转换为RGB格式
                show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # 这里指的是显示原图
                # opencv 读取图片的样式，不能通过Qlabel进行显示，需要转换为Qimage QImage(uchar * data, int width,
                self.showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
                # self.ui.label_camera_layout_2.setPixmap(QPixmap.fromImage(self.showImage))
                self.ui.label_camera_layout.setPixmap(
                    QPixmap.fromImage(self.showImage).scaled(self.ui.label_camera_layout.width(),
                                                             self.ui.label_camera_layout.height()))
            # 因为最后会存留一张图像在lable上，需要对lable进行清理
            self.ui.label_camera_layout.clear()
            # self.ui.bt_open_camera.setText(u'打开相机')
            self.ui.bt_checkin.setText(u'打 卡')
            # self.ui.label_checkin_note.setText('请打开摄像头')
            # 设置单张图片背景
            self.ui.label_camera_layout.setPixmap(
                self.bkg_camera.scaled(self.ui.label_camera_layout.width(), self.ui.label_camera_layout.height()))
        elif self.switch_bt == 1:
            CHECK_IN_NOTE['if_blink'] = 0
            self.startThread.Resume()
            self.startThread.start()  # 启动线程
            print("thread-start")
            self.ui.bt_checkin.setText(u'停 止')
            # 人脸检测的置信度
            confidence_default = 0.5
            # 从磁盘加载序列化面部检测器
            proto_path = os.path.sep.join([self.detector_path, "deploy.prototxt"])
            model_path = os.path.sep.join([self.detector_path, "res10_300x300_ssd_iter_140000.caffemodel"])
            detector = cv2.dnn.readNetFromCaffe(proto_path, model_path)

            # 读取判别数据和标准
            localData = open('local.json', 'r')
            content = localData.read()
            _accuracy = 0
            if content != '':
                _accuracy = json.loads(content)['accuracy']
            localData.close()
            face_features = localReadMatrix('face_features.npz')
            # 这里写读取失败的操作
            # 如: if _accuracy == 0 or face_features is None:
            #     return

            # 循环来自视频文件流的帧
            while self.cap.isOpened():
                # if CHECK_IN_NOTE['ifstop']: return
                ret, frame = self.cap.read()
                # 识别逻辑先写在界面同一线程

                # if len(faceRects) > 0:  # 允许检测多个人
                #     # 需要达到高度相似的面部数据数量 有1次匹配就算成功
                #     matNum = 0
                #     for faceRect in faceRects:
                #         face_feature = getFaceData(frame, faceRect)
                #         for i in range(len(face_features)):
                #             if getSimilarity(face_features[i], face_feature) > _accuracy:
                #                 matNum += 1
                #     if matNum >= 1:
                #         break   # 这里写识别成功的其他操作

                QApplication.processEvents()
                if ret:
                    # 调整框架的大小以使其宽度为900像素（同时保持纵横比），然后抓取图像尺寸
                    frame = imutils.resize(frame, width=500)
                    faceRects = getFacePosition(frame)
                    (h, w) = frame.shape[:2]
                    # 从图像构造一个blob, 缩放为 300 x 300 x 3 像素的图像，为了符合ResNet-SSD的输入尺寸 OpenCV
                    image_blob = cv2.dnn.blobFromImage(
                        cv2.resize(frame, (300, 300)), 1.0, (300, 300),
                        (104.0, 177.0, 123.0), swapRB=False, crop=False)
                    detector.setInput(image_blob)
                    detections = detector.forward()
                    # 在“detections”中进行循环，检测图像中什么位置有什么样的目标：
                    for i in np.arange(0, detections.shape[2]):
                        # 提取与预测相关的置信度（即概率），detections的第3维
                        confidence = detections[0, 0, i, 2]

                        # 用于更新相机开关按键信息
                        if not self.cap.isOpened():
                            self.ui.bt_checkin.setText(u'打 卡')
                        else:
                            self.ui.bt_checkin.setText(u'停 止')

                        if confidence > confidence_default:
                            # 计算面部边界框的（x，y）坐标， 对应detections的4,5,6,7维（索引为3-7），含义分别代表：
                            # x_left_bottom, y_left_bottom, x_right_top, y_right_top
                            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                            (startX, startY, endX, endY) = box.astype("int")
                            # 提取面部ROI
                            # 提取人脸的长和宽，本例中为 397 x 289
                            face = frame[startY:endY, startX:endX]
                            (fH, fW) = face.shape[:2]

                            # 确保面部宽度和高度足够大，以过滤掉小人脸(较远)，防止远处人员签到，以及过滤误检测
                            if fW < 100 or fH < 100:
                                continue
                            # idx = int(detections[0, 0, i, 1])
                            # 绘制面部的边界框以及相关的概率
                            # text = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)

                            # 表情检测
                            expression = 'normal'
                            for faceRect in faceRects:
                                expression = recognizeExpression(frame, faceRect)  # 检测表情
                                # print(expression)

                            y = startY - 10 if startY - 10 > 10 else startY + 10
                            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                            frame = cv2.putText(frame, expression, (startX, y),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                            # frame = cv2.putText(frame, f"Blink:{CHECK_IN_NOTE['if_blink']}", (startX, y),
                            #                     cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255),
                            #                     2)

                            # 显示输出框架
                            show_video = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 这里指的是显示原图
                            # opencv读取图片的样式，不能通过Qlabel进行显示，需要转换为Qimage。
                            # QImage(uchar * data, int width, int height, int bytesPerLine, Format format)
                            self.showImage = QImage(show_video.data,
                                                    show_video.shape[1],
                                                    show_video.shape[0],
                                                    QImage.Format_RGB888)
                            self.ui.label_camera_layout.setPixmap(QPixmap.fromImage(self.showImage))

                            if CHECK_IN_NOTE['if_blink'] == 1:
                                # self.startThread.terminate()
                                self.ui.label_checkin_note.setText("眨眼检测成功！")
                                # CHECK_IN_NOTE['if_blink'] = 0
                                if len(faceRects) > 0:  # 允许检测多个人
                                    # 需要达到高度相似的面部数据数量 有1次匹配就算成功
                                    matNum = 0
                                    for faceRect in faceRects:
                                        face_feature = getFaceData(frame, faceRect)
                                        for i in range(len(face_features)):
                                            if getSimilarity(face_features[i], face_feature) > _accuracy:
                                                matNum += 1
                                    if matNum >= 1:
                                        self.post_check(mood=expression)  # 这里写识别成功的其他操作
                else:
                    self.cap.release()

            # 因为最后一张画面会显示在GUI中，此处实现清除。
            self.ui.label_camera_layout.clear()

    def auto_control(self):
        if self.cap.isOpened():
            if self.switch_bt == 0:
                # 检查是否有人脸数据
                if not LOCAL_USER['if_face']:
                    QMsgBox.showMsg("未录入人脸，请先在个人信息页面进行人脸采集～")
                    self.open_camera()
                    self.ui.stackedWidget.setCurrentIndex(1)
                    return
                self.switch_bt = 1
                self.ui.bt_checkin.setText(u'停 止')
                self.ui.label_checkin_note.setText(u'请眨眨眼睛')
                self.show_camera()
            elif self.switch_bt == 1:
                self.switch_bt = 0
                self.ui.bt_checkin.setText(u'打 卡')
                self.ui.label_checkin_note.setText(u'')
                self.show_camera()
        else:
            self.ui.label_checkin_note.setText("请打开摄像头！")

    def post_check(self, mood='normal'):
        self.switch_bt = 0
        self.cap.release()
        if CHECK_IN_NOTE['check_status']:
            form_data = {
                'staff_id': LOCAL_USER['id'],
                'company_name': LOCAL_USER['company'],
                'department': LOCAL_USER['department'],
                'check_time': datetime.datetime.today().isoformat(' ', timespec='seconds'),
                'mood': mood
            }
            print('post time: ', form_data['check_time'])
            response = requests.post("http://127.0.0.1:5000/user/checkin", data=form_data)
            c = response.json()
            QMessageBox.information(self, '服务器数据提示', c['msg'], QMessageBox.Ok)

            '''待完成：根据返回结果改变控件'''
            if c['status'] == 1:
                self.showCalenderColor()
                self.show_date_att()
                print("self.showCalenderColor()")
                self.ui.stackedWidget.setCurrentIndex(1)

    def closeEvent(self, event):
        result = QMsgBox.showMsg('确定要退出程序吗？')
        event.ignore()
        if result == 1:
            LOGIN_STATUS[0] = 0
            self.cap.release()  # Destroy the camera if it is not already
            self.startThread.terminate()
            event.accept()

    def face_checkin(self):
        if self.cap.isOpened():
            self.ui.bt_checkin.setText(u'停 止')
            self.ui.label_checkin_note.setText(u'请眨眨眼睛')
        else:
            QMessageBox.about(self, "提示", "请打开摄像头！")

    def checkFaceData(self):
        # 读取local文件
        local = open('local.json', 'r')
        content = local.read()
        if content != '':
            local_status = json.loads(content)
        else:
            local_status = {}
        local.close()
        # 写入文件
        if content != '':
            # 先删除人脸文件
            if os.path.exists(f"{rootdir}/face_features.npz"):  # 如果文件存在
                os.remove(f"{rootdir}/face_features.npz")
            checkResponse = updateFaceData(LOCAL_USER['id'], LOCAL_USER['flag'])
            if checkResponse[0] == 1:  # 需要更新且带回了数据和附加信息 accuracy、flag_id
                _dict = {
                    'accuracy': checkResponse[2],
                    'flag_id': checkResponse[3],
                }
                local = open('local.json', 'w')
                local_status['accuracy'] = _dict['accuracy']
                local_status['flag_id'] = _dict['flag_id']
                print("check", local_status)
                b = json.dumps(local_status)
                local.write(b)
                local.close()
                localSaveMatrix('face_features.npz', checkResponse[1])
            elif checkResponse[0] == -1:
                return False
                # 这里是数据缺失，需要提示用户重新上传数据

        return True

    def blinks_thread(self):
        if self.cap.isOpened():
            # 初始化眨眼检测线程
            print("blinks_thread   1")
            self.startThread = BlinksDetectThread()
            self.startThread.start()  # 启动线程
        else:
            print("blinks_thread   0")
            self.ui.label_checkin_note.setText("请打开摄像头！")

    # 主页面调用其他页面
    windowList = []

    # ToolBar点击logo显示团队信息
    def information_triggered(self):
        information = InformationDialog()
        self.windowList.append(information)
        information.show()

    # 修改密码
    def change_pwd_clicked(self):
        mychangepwd = ChangepwdDialog()
        self.windowList.append(mychangepwd)
        mychangepwd.handle_click()

    # 人脸采集页面
    def open_facecollecting_clicked(self):
        myFaceCollectingDialog = FaceCollectingDialog()
        self.windowList.append(myFaceCollectingDialog)
        myFaceCollectingDialog.handle_click()

    # 申请界面
    def open_application_clicked(self, n):
        myApplicationDialog = ApplicationDialog()
        self.windowList.append(myApplicationDialog)
        myApplicationDialog.submitButton.clicked.connect(self.handle_application)
        if n == 1:
            myApplicationDialog.handle_click()
        elif n == 2:
            # myApplicationDialog.handle_click()
            myApplicationDialog.att_excep()

    # 打卡界面
    def show_checkin(self):
        if ch_cal.is_holiday(datetime.datetime.today()):
            QMsgBox.showMsg("今日为假期，无需打卡")
        elif not LOCAL_USER['if_face']:
            QMsgBox.showMsg("还未录入人脸，请先进行人脸采集！")
        elif LOCAL_USER['department'] == '\\':
            QMsgBox.showMsg("还未加入部门，无需打卡")
        else:
            self.ui.stackedWidget.setCurrentIndex(0)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mymainwindow = MainWindow()
#     myapplication = ApplicationDialog()
#     myfacecollecting = FaceCollectingDialog()
#     mylogin = LoginDialog()
#     myregister = RegisterDialog()
#     mychangepwd = ChangepwdDialog()
#
#     mymainwindow.ui.bt_open_application.clicked.connect(myapplication.handle_click)
#     mymainwindow.ui.bt_open_face_collecting.clicked.connect(myfacecollecting.handle_click)
#     mymainwindow.ui.bt_change_pwd.clicked.connect(mychangepwd.handle_click)
#     mymainwindow.ui.bt_exception.clicked.connect(myapplication.att_excep)
#     # 登录页面跳转
#     mylogin.register_Button.clicked.connect(myregister.handle_click)
#     mylogin.login_Button.clicked.connect(mymainwindow.handle_login_click)
#     mylogin.key.activated.connect(mymainwindow.handle_login_click)
#     # 注册页面
#     myregister.Dialog.bt_open_facecollecting.clicked.connect(myfacecollecting.handle_click)
#     myregister.Dialog.register_Button.clicked.connect(mylogin.load)
#     myregister.key.activated.connect(mylogin.load)
#     # 申请提交
#     myapplication.submitButton.clicked.connect(mymainwindow.handle_application)
#     mymainwindow.ui.logout.triggered.connect(mylogin.handle_click)
#     mylogin.show()
#
#     sys.exit(app.exec_())
