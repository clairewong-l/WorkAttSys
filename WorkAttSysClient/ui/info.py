# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'info.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_info(object):
    def setupUi(self, info):
        info.setObjectName("info")
        info.resize(1043, 772)
        info.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(info)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_4 = QtWidgets.QFrame(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.faceCollectionButton = QtWidgets.QPushButton(self.frame_4)
        self.faceCollectionButton.setGeometry(QtCore.QRect(20, 130, 93, 28))
        self.faceCollectionButton.setObjectName("faceCollectionButton")
        self.StaffImglabel = QtWidgets.QLabel(self.frame_4)
        self.StaffImglabel.setGeometry(QtCore.QRect(10, 10, 111, 111))
        self.StaffImglabel.setObjectName("StaffImglabel")
        self.horizontalLayout.addWidget(self.frame_4)
        self.frame_info = QtWidgets.QFrame(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_info.sizePolicy().hasHeightForWidth())
        self.frame_info.setSizePolicy(sizePolicy)
        self.frame_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_info.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_info.setObjectName("frame_info")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_info)
        self.gridLayout.setObjectName("gridLayout")
        self.Label3 = QtWidgets.QLabel(self.frame_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label3.sizePolicy().hasHeightForWidth())
        self.Label3.setSizePolicy(sizePolicy)
        self.Label3.setObjectName("Label3")
        self.gridLayout.addWidget(self.Label3, 2, 0, 1, 1)
        self.Label2 = QtWidgets.QLabel(self.frame_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label2.sizePolicy().hasHeightForWidth())
        self.Label2.setSizePolicy(sizePolicy)
        self.Label2.setObjectName("Label2")
        self.gridLayout.addWidget(self.Label2, 1, 0, 1, 1)
        self.staffNameLabel = QtWidgets.QLabel(self.frame_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.staffNameLabel.sizePolicy().hasHeightForWidth())
        self.staffNameLabel.setSizePolicy(sizePolicy)
        self.staffNameLabel.setObjectName("staffNameLabel")
        self.gridLayout.addWidget(self.staffNameLabel, 1, 1, 1, 1)
        self.staffCompanyLabel = QtWidgets.QLabel(self.frame_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.staffCompanyLabel.sizePolicy().hasHeightForWidth())
        self.staffCompanyLabel.setSizePolicy(sizePolicy)
        self.staffCompanyLabel.setObjectName("staffCompanyLabel")
        self.gridLayout.addWidget(self.staffCompanyLabel, 2, 1, 1, 1)
        self.staffIdLabel = QtWidgets.QLabel(self.frame_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.staffIdLabel.sizePolicy().hasHeightForWidth())
        self.staffIdLabel.setSizePolicy(sizePolicy)
        self.staffIdLabel.setObjectName("staffIdLabel")
        self.gridLayout.addWidget(self.staffIdLabel, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.frame_info)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.departmentLabel = QtWidgets.QLabel(self.frame_info)
        self.departmentLabel.setObjectName("departmentLabel")
        self.gridLayout.addWidget(self.departmentLabel, 3, 1, 1, 1)
        self.label1 = QtWidgets.QLabel(self.frame_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label1.sizePolicy().hasHeightForWidth())
        self.label1.setSizePolicy(sizePolicy)
        self.label1.setObjectName("label1")
        self.gridLayout.addWidget(self.label1, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_info)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.leavedaysLabel = QtWidgets.QLabel(self.frame_info)
        self.leavedaysLabel.setObjectName("leavedaysLabel")
        self.gridLayout.addWidget(self.leavedaysLabel, 4, 1, 1, 1)
        self.horizontalLayout.addWidget(self.frame_info)
        self.frame_2 = QtWidgets.QFrame(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.changepwdButton = QtWidgets.QPushButton(self.frame_2)
        self.changepwdButton.setGeometry(QtCore.QRect(12, 27, 93, 28))
        self.changepwdButton.setObjectName("changepwdButton")
        self.applicationButton = QtWidgets.QPushButton(self.frame_2)
        self.applicationButton.setGeometry(QtCore.QRect(12, 77, 93, 28))
        self.applicationButton.setObjectName("applicationButton")
        self.attButton = QtWidgets.QPushButton(self.frame_2)
        self.attButton.setGeometry(QtCore.QRect(12, 127, 93, 28))
        self.attButton.setObjectName("attButton")
        self.horizontalLayout.addWidget(self.frame_2)
        self.verticalLayout_2.addWidget(self.widget)
        self.infoWidget = QtWidgets.QTabWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.infoWidget.sizePolicy().hasHeightForWidth())
        self.infoWidget.setSizePolicy(sizePolicy)
        self.infoWidget.setObjectName("infoWidget")
        self.recordTab = QtWidgets.QWidget()
        self.recordTab.setBaseSize(QtCore.QSize(100, 100))
        self.recordTab.setObjectName("recordTab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.recordTab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.staffcalendar = QtWidgets.QCalendarWidget(self.recordTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(7)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.staffcalendar.sizePolicy().hasHeightForWidth())
        self.staffcalendar.setSizePolicy(sizePolicy)
        self.staffcalendar.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.staffcalendar.setNavigationBarVisible(True)
        self.staffcalendar.setObjectName("staffcalendar")
        self.horizontalLayout_2.addWidget(self.staffcalendar)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.frame_3 = QtWidgets.QFrame(self.recordTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.dateLabel = QtWidgets.QLabel(self.frame_3)
        self.dateLabel.setObjectName("dateLabel")
        self.verticalLayout_4.addWidget(self.dateLabel)
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_4.addWidget(self.label_9)
        self.onAttLabel = QtWidgets.QLabel(self.frame_3)
        self.onAttLabel.setObjectName("onAttLabel")
        self.verticalLayout_4.addWidget(self.onAttLabel)
        self.label_10 = QtWidgets.QLabel(self.frame_3)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_4.addWidget(self.label_10)
        self.offAttLabel = QtWidgets.QLabel(self.frame_3)
        self.offAttLabel.setObjectName("offAttLabel")
        self.verticalLayout_4.addWidget(self.offAttLabel)
        self.horizontalLayout_2.addWidget(self.frame_3)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 17)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 7)
        self.horizontalLayout_2.setStretch(4, 1)
        self.infoWidget.addTab(self.recordTab, "")
        self.applicationTab = QtWidgets.QWidget()
        self.applicationTab.setObjectName("applicationTab")
        self.appWidget = QtWidgets.QTabWidget(self.applicationTab)
        self.appWidget.setGeometry(QtCore.QRect(0, 0, 1001, 491))
        self.appWidget.setObjectName("appWidget")
        self.allApplicationTab = QtWidgets.QWidget()
        self.allApplicationTab.setObjectName("allApplicationTab")
        self.appWidget.addTab(self.allApplicationTab, "")
        self.attApplicationTab = QtWidgets.QWidget()
        self.attApplicationTab.setObjectName("attApplicationTab")
        self.appWidget.addTab(self.attApplicationTab, "")
        self.outApplicationTab = QtWidgets.QWidget()
        self.outApplicationTab.setObjectName("outApplicationTab")
        self.appWidget.addTab(self.outApplicationTab, "")
        self.vacationApplicationTab = QtWidgets.QWidget()
        self.vacationApplicationTab.setObjectName("vacationApplicationTab")
        self.appWidget.addTab(self.vacationApplicationTab, "")
        self.backApplicationTab = QtWidgets.QWidget()
        self.backApplicationTab.setObjectName("backApplicationTab")
        self.appWidget.addTab(self.backApplicationTab, "")
        self.entryQuitTab = QtWidgets.QWidget()
        self.entryQuitTab.setObjectName("entryQuitTab")
        self.appWidget.addTab(self.entryQuitTab, "")
        self.infoWidget.addTab(self.applicationTab, "")
        self.verticalLayout_2.addWidget(self.infoWidget)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(info)
        self.infoWidget.setCurrentIndex(1)
        self.appWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(info)

    def retranslateUi(self, info):
        _translate = QtCore.QCoreApplication.translate
        info.setWindowTitle(_translate("info", "个人主页"))
        self.faceCollectionButton.setText(_translate("info", "人脸录入"))
        self.StaffImglabel.setText(_translate("info", "图片"))
        self.Label3.setText(_translate("info", "公司"))
        self.Label2.setText(_translate("info", "姓名"))
        self.staffNameLabel.setText(_translate("info", "杨"))
        self.staffCompanyLabel.setText(_translate("info", "无"))
        self.staffIdLabel.setText(_translate("info", "2018"))
        self.label.setText(_translate("info", "部门"))
        self.departmentLabel.setText(_translate("info", "无"))
        self.label1.setText(_translate("info", "工号"))
        self.label_3.setText(_translate("info", "剩余年假天数"))
        self.leavedaysLabel.setText(_translate("info", "0"))
        self.changepwdButton.setText(_translate("info", "修改密码"))
        self.applicationButton.setText(_translate("info", "申请"))
        self.attButton.setText(_translate("info", "打卡"))
        self.dateLabel.setText(_translate("info", "日期"))
        self.label_9.setText(_translate("info", "上班打卡"))
        self.onAttLabel.setText(_translate("info", "打卡时间，状态"))
        self.label_10.setText(_translate("info", "下班打卡"))
        self.offAttLabel.setText(_translate("info", "打卡时间、状态"))
        self.infoWidget.setTabText(self.infoWidget.indexOf(self.recordTab), _translate("info", "打卡记录"))
        self.appWidget.setTabText(self.appWidget.indexOf(self.allApplicationTab), _translate("info", "全部申请"))
        self.appWidget.setTabText(self.appWidget.indexOf(self.attApplicationTab), _translate("info", "补签改签申请"))
        self.appWidget.setTabText(self.appWidget.indexOf(self.outApplicationTab), _translate("info", "外派申请"))
        self.appWidget.setTabText(self.appWidget.indexOf(self.vacationApplicationTab), _translate("info", "请假申请"))
        self.appWidget.setTabText(self.appWidget.indexOf(self.backApplicationTab), _translate("info", "销假申请"))
        self.appWidget.setTabText(self.appWidget.indexOf(self.entryQuitTab), _translate("info", "入职离职申请"))
        self.infoWidget.setTabText(self.infoWidget.indexOf(self.applicationTab), _translate("info", "申请记录"))
