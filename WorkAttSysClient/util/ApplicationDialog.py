import PyQt5.QtBluetooth
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# 导入信息采集框界面
from ui import application as applicationUi

from util.GlobalVar import LOGIN_STATUS, LOCAL_USER, NEW_APP, APP_ID
from util.MsgBoxDialog import QMsgBox
import requests, datetime
import time
import datetime as dt


class ApplicationDialog(QWidget, applicationUi.Ui_Form):
    def __init__(self, parent = None):
        # super()构造器方法返回父级的对象。__init__()方法是构造器的一个方法。
        super(ApplicationDialog, self).__init__(parent)
        self.setupUi(self)
        self.logo = QIcon('./imgs/icon_app.jpg')
        self.setWindowTitle('智慧考勤系统')
        self.setWindowIcon(self.logo)

        self.setWindowModality(Qt.ApplicationModal)

        self.submitButton.clicked.connect(self.post)
        # self.application_tabWidget.currentChanged.connect(self.tab_change)
        # self.application_tabWidget.currentChanged.connect(self.post_comp_visible)
        self.dateEdit.setDate(QDate.currentDate())
        self.dateEdit.setCalendarPopup(True)
        self.start_dateEdit.setDate(QDate.currentDate())
        self.start_dateEdit.setCalendarPopup(True)
        self.end_dateEdit.setDate(QDate.currentDate())
        self.end_dateEdit.setCalendarPopup(True)
        self.back_dateEdit.setDate(QDate.currentDate())
        self.back_dateEdit.setCalendarPopup(True)
        self.outs_dateEdit.setDate(QDate.currentDate())
        self.outs_dateEdit.setCalendarPopup(True)
        self.oute_dateEdit.setDate(QDate.currentDate())
        self.oute_dateEdit.setCalendarPopup(True)
        self.submitButton.setCursor(Qt.CursorShape.PointingHandCursor)

        self.application_tabWidget.setCurrentIndex(0)

        self.application_tabWidget.setStyleSheet("QTabWidget#tabWidget{background-color:white;}\
                                 QTabBar::tab{background-color:rgb(255,246,234);color:rgb(128,128,128);}\
                                 QTabBar::tab::selected{background-color:rgb(249,179,132);color:white;}")

    '''
    def tab_change(self):
        if self.application_tabWidget.currentIndex() == 1:
            if LOCAL_USER['company'] is None:
                self.type_comboBox_2.addItem("入职")
                self.type_comboBox_2.setCurrentIndex(0)
            else:
                self.type_comboBox_2.addItem("离职")
                self.type_comboBox_2.setCurrentIndex(0)
                self.company_lineEdit.setText(LOCAL_USER['company'])
                self.company_lineEdit.setReadOnly(True)
    '''

    def handle_click(self):
        if not self.isVisible():
            self.application_tabWidget.setTabVisible(0, False)
            self.application_tabWidget.setTabVisible(1, True)
            self.application_tabWidget.setTabVisible(2, True)
            self.application_tabWidget.setTabVisible(3, True)
            self.application_tabWidget.setTabVisible(4, True)
            self.show()
        if LOCAL_USER['company'] == '\\':
            self.type_comboBox_2.clear()
            self.application_tabWidget.setTabVisible(0, False)
            self.application_tabWidget.setTabVisible(1, True)
            self.application_tabWidget.setTabVisible(2, False)
            self.application_tabWidget.setTabVisible(3, False)
            self.application_tabWidget.setTabVisible(4, False)
            self.show()
            self.type_comboBox_2.addItem("入职")
            self.type_comboBox_2.setCurrentIndex(0)
        else:
            self.type_comboBox_2.clear()
            self.type_comboBox_2.addItem("离职")
            self.type_comboBox_2.setCurrentIndex(0)
            self.company_lineEdit.setText(LOCAL_USER['company'])
            self.company_lineEdit.setReadOnly(True)

        app_date = QtCore.QDate.fromString(NEW_APP['app_date'], 'yyyy-MM-dd')
        self.dateEdit.setDate(app_date)
        self.end_dateEdit.setDate(app_date)
        self.back_dateEdit.setDate(app_date)
        self.oute_dateEdit.setDate(app_date)
        self.outs_dateEdit.setDate(app_date)
        self.start_dateEdit.setDate(app_date)

    def att_excep(self):
        if not self.isVisible():
            self.application_tabWidget.setTabVisible(0, True)
            self.application_tabWidget.setTabVisible(1, False)
            self.application_tabWidget.setTabVisible(2, False)
            self.application_tabWidget.setTabVisible(3, False)
            self.application_tabWidget.setTabVisible(4, False)
            self.show()
        app_date = QtCore.QDate.fromString(NEW_APP['app_date'], 'yyyy-MM-dd')
        self.dateEdit.setDate(app_date)
        QApplication.processEvents()

    def post(self):
        if self.application_tabWidget.currentIndex() == 0:
            self.post_att()
        if self.application_tabWidget.currentIndex() == 1:
            self.post_comp()
        if self.application_tabWidget.currentIndex() == 2:
            self.post_vaca()
        if self.application_tabWidget.currentIndex() == 3:
            self.post_back()
        if self.application_tabWidget.currentIndex() == 4:
            self.post_out()

    # 1.提交打卡异常修改申请
    def post_att(self):
        APP_ID[0] = 1
        date = self.dateEdit.date().toString('yyyy-MM-dd')
        # type = self.type_comboBox.currentText()
        worktype = self.comboBox.currentText()  # 上班下班
        new_att_status = self.status_comboBox.currentText()

        staff_comment = self.comment_textEdit.toPlainText()
        staff_id = LOCAL_USER['id']
        company_name = LOCAL_USER['company']
        record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # if type == "补签":
        #     type_id = 1
        # elif type == "改签":
        #     type_id = 2

        if worktype == "上班":
            worktype_id = 1
        elif worktype == "下班":
            worktype_id = 2

        if new_att_status == "出勤":
            new_att_status_id = 1
        elif new_att_status == "迟到":
            new_att_status_id = 2
        elif new_att_status == "早退":
            new_att_status_id = 3
        elif new_att_status == "缺勤":
            new_att_status_id = 4
        elif new_att_status == "请假":
            new_att_status_id = 5

        form_data = {
            "date": date,
            # "type": type_id,
            "worktype": worktype_id,
            "new_att_status": new_att_status_id,
            "staff_comment": staff_comment,
            "staff_id": staff_id,
            "company_name": company_name,
            "record_time": record_time
        }
        response = requests.post("http://127.0.0.1:5000/user/attApplication", data = form_data)
        c = response.json()

        if c['status'] == 1:
            QMsgBox.showMsg(c['msg'])
            # QMessageBox.information(self, '服务器数据提示', c['msg'], QMessageBox.Yes | QMessageBox.No)
            app_str = f"申请修改{date} {worktype} 打卡状态为：{new_att_status}     \n申请时间：{record_time} \n申请状态：待审批"
            NEW_APP['app_str'] = app_str
            APP_ID[1] = 1
            self.close()
        elif c['status'] == 0:
            QMsgBox.showMsg(c['msg'])

    # 2.提交入职/离职申请
    def post_comp(self):
        APP_ID[0] = 5
        entry_quit = self.type_comboBox_2.currentText()
        staff_comment = self.comment_textEdit_2.toPlainText()
        record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        staff_id = LOCAL_USER['id']
        if entry_quit == "入职":
            company = self.company_lineEdit.text()
            form_data = {
                "company": company,
                "staff_comment": staff_comment,
                "staff_id": staff_id,
                "record_time": record_time
            }
            response = requests.post("http://127.0.0.1:5000/user/entryApplication", data = form_data)
            c = response.json()
            if c['status'] == 1:
                QMsgBox.showMsg(c['msg'])
                #QMessageBox.information(self, '服务器数据提示', c['msg'], QMessageBox.Yes | QMessageBox.No)
                app_str = f"申请{entry_quit}：{company}       \n申请时间：{record_time} \n申请状态：待审批"
                NEW_APP['app_str'] = app_str
                APP_ID[1] = 1
                self.close()
            if c['status'] == 0:
                QMsgBox.showMsg(c['msg'])
                #QMessageBox.information(self, '服务器数据提示', c['msg'], QMessageBox.Yes | QMessageBox.No)
            if c['status'] == 2:
                QMsgBox.showMsg(c['msg'])
                #QMessageBox.information(self, '服务器数据提示', c['msg'], QMessageBox.Yes | QMessageBox.No)
        elif entry_quit == "离职":
            company = LOCAL_USER['company']
            form_data = {
                "company": company,
                "staff_comment": staff_comment,
                "staff_id": staff_id,
                "record_time": record_time
            }
            response = requests.post("http://127.0.0.1:5000/user/quitApplication", data = form_data)
            c = response.json()
            if c['status'] == 1:
                QMsgBox.showMsg(c['msg'])
                #QMessageBox.information(self, '服务器数据提示', c['msg'], QMessageBox.Yes | QMessageBox.No)
                app_str = f"申请{entry_quit}：{company}       \n申请时间：{record_time} \n申请状态：待审批"
                NEW_APP['app_str'] = app_str
                APP_ID[1] = 1
                self.close()
            if c['status'] == 0:
                QMsgBox.showMsg(c['msg'])
               #QMessageBox.information(self, '服务器数据提示', c['msg'], QMessageBox.Yes | QMessageBox.No)

    # 3.提交请假申请
    def post_vaca(self):
        APP_ID[0] = 3
        s_date = self.start_dateEdit.date().toString('yyyy-MM-dd')
        e_date = self.end_dateEdit.date().toString('yyyy-MM-dd')
        days = self.time_long(s_date, e_date)

        currentdate = datetime.datetime.now().strftime('%Y-%m-%d')
        s_datedays = self.time_long(currentdate, s_date)
        e_datedays = self.time_long(currentdate, e_date)

        staff_comment = self.comment_textEdit_3.toPlainText()
        staff_id = LOCAL_USER['id']
        if days >= 0:
            if s_datedays >= 0 and e_datedays >= 0:
                staff_id = LOCAL_USER['id']
                company_name = LOCAL_USER['company']
                record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                form_data = {
                    "s_date": s_date,
                    "e_date": e_date,
                    "days": days,
                    "staff_comment": staff_comment,
                    "staff_id": staff_id,
                    "company_name": company_name,
                    "record_time": record_time
                }
                response = requests.post("http://127.0.0.1:5000/user/vacaApplication", data = form_data)
                c = response.json()
                if c['status'] == 1:
                    QMsgBox.showMsg(c['msg'])
                    #QMessageBox.information(self, '服务器数据提示', c['msg'], QMessageBox.Yes | QMessageBox.No)
                    app_str = f"申请于{s_date}至{e_date}请假{int(days)}天            \n申请时间：{record_time}\n申请状态：待审批 "
                    NEW_APP['app_str'] = app_str
                    APP_ID[1] = 1
                    self.close()
                if c['status'] == 0:
                    QMsgBox.showMsg(c['msg'])
                    #QMessageBox.information(self, '服务器数据提示', c['msg'], QMessageBox.Yes | QMessageBox.No)
            else:
                QMsgBox.showMsg('无效申请日期')
                #QMessageBox.information(self, '提示', "无效申请日期", QMessageBox.Ok)
        else:
            QMsgBox.showMsg('结束日期早于开始日期，请重新选择！')
            #QMessageBox.information(self, '提示', "结束日期早于开始日期，请重新选择！", QMessageBox.Ok)

    # 4.提交销假申请
    def post_back(self):
        APP_ID[0] = 4
        e_date = self.back_dateEdit.date().toString('yyyy-MM-dd')

        staff_comment = self.comment_textEdit_4.toPlainText()
        staff_id = LOCAL_USER['id']
        company_name = LOCAL_USER['company']
        record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        form_data = {
            "e_date": e_date,
            "staff_comment": staff_comment,
            "staff_id": staff_id,
            "company_name": company_name,
            "record_time": record_time
        }
        response = requests.post("http://127.0.0.1:5000/user/backApplication", data = form_data)
        c = response.json()
        if c['status'] == 1:
            QMsgBox.showMsg(c['msg'])
            #QMessageBox.information(self, '服务器数据提示', c['msg'], QMessageBox.Yes | QMessageBox.No)
            app_str = f"申请于{e_date}销假            \n申请时间：{record_time}\n申请状态：待审批"
            NEW_APP['app_str'] = app_str
            APP_ID[1] = 1
            self.close()
        if c['status'] == 0:
            QMsgBox.showMsg(c['msg'])
            #QMessageBox.information(self, '服务器数据提示', c['msg'], QMessageBox.Yes | QMessageBox.No)

    # 5.提交外派申请
    def post_out(self):
        APP_ID[0] = 2
        s_date = self.outs_dateEdit.date().toString('yyyy-MM-dd')
        e_date = self.oute_dateEdit.date().toString('yyyy-MM-dd')
        place = self.place_lineEdit.text()
        days = self.time_long(s_date, e_date)

        currentdate = datetime.datetime.now().strftime('%Y-%m-%d')
        s_datedays = self.time_long(currentdate, s_date)
        e_datedays = self.time_long(currentdate, e_date)

        if days >= 0:
            if s_datedays >= 0 and e_datedays >= 0:
                staff_comment = self.comment_textEdit_5.toPlainText()
                staff_id = LOCAL_USER['id']
                company_name = LOCAL_USER['company']
                record_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                form_data = {
                    "s_date": s_date,
                    "e_date": e_date,
                    "place": place,
                    "staff_comment": staff_comment,
                    "staff_id": staff_id,
                    "company_name": company_name,
                    "record_time": record_time
                }
                response = requests.post("http://127.0.0.1:5000/user/outApplication", data = form_data)
                c = response.json()
                if c['status'] == 1:
                    QMsgBox.showMsg(c['msg'])
                    #QMessageBox.information(self, '服务器数据提示', c['msg'], QMessageBox.Yes | QMessageBox.No)
                    app_str = f"申请于{s_date}至{e_date}外派，地点：{place}            \n申请时间：{record_time}\n申请状态：待审批"
                    NEW_APP['app_str'] = app_str
                    APP_ID[1] = 1
                    self.close()
                if c['status'] == 0:
                    QMsgBox.showMsg(c['msg'])
                    #QMessageBox.information(self, '服务器数据提示', c['msg'], QMessageBox.Yes | QMessageBox.No)
            else:
                QMsgBox.showMsg('无效申请日期')
                #QMessageBox.information(self, '提示', "无效申请日期", QMessageBox.Ok)
        else:
            QMsgBox.showMsg('结束日期早于开始日期，请重新选择！')
            #QMessageBox.information(self, '提示', "结束日期早于开始日期，请重新选择！", QMessageBox.Ok)

    # 计算日期
    def time_long(self, time1, time2):
        day1 = dt.datetime.strptime(time1, "%Y-%m-%d").date()
        day2 = dt.datetime.strptime(time2, "%Y-%m-%d").date()
        day_num = (day2 - day1).days
        int(day_num)
        day_num = day_num + 1
        return day_num
