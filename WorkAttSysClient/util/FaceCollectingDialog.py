import json

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# 导入信息采集框界面
from ui import face_collecting as facecollectingUi

import threading
import cv2
import imutils
import os
import sys
# 导入全局变量，主要包含摄像头ID，默认采集人脸数量等
from util.GlobalVar import CAMERA_ID, COLLENCT_FACE_NUM_DEFAULT, LOOP_FRAME
from util.GlobalVar import add_path_to_sys, LOCAL_USER, backendHost
from util.faceDataUtil import getFacePosition, rectToPosition, getFaceData, commitFaceData, localSaveMatrix
from util.MsgBoxDialog import QMsgBox

rootdir = add_path_to_sys()


class FaceCollectingDialog(QWidget):
    def __init__(self):
        # super()构造器方法返回父级的对象。__init__()方法是构造器的一个方法。
        super().__init__()
        self.Dialog = facecollectingUi.Ui_CheckInUi()
        self.Dialog.setupUi(self)
        self.logo = QIcon('./imgs/icon_app.jpg')
        self.setWindowIcon(self.logo)

        self.setWindowModality(Qt.ApplicationModal)

        # 实现路径错误提示，方便定位错误
        self.current_filename = os.path.basename(__file__)

        try:
            # 设置窗口名称和图标
            self.setWindowTitle('人脸采集')
            # 设置单张图片背景
            pixmap = QPixmap(f'{backendHost}imgs/camera_bkg.png')
            self.Dialog.label_camera_layout.setPixmap(pixmap.scaled(
                self.Dialog.label_camera_layout.width(), self.Dialog.label_camera_layout.height()))
        except FileNotFoundError as e:
            print("[ERROR] UI背景图片路径不正确！(source file: {})".format(self.current_filename), e)

        # 设置"开始采集"按键连接函数
        self.Dialog.bt_face_collecting.clicked.connect(self.open_camera)
        self.Dialog.bt_face_collecting.setCursor(Qt.CursorShape.PointingHandCursor)

        # 页面初始化
        self.Dialog.label_collected_num.setText('0')

        # 初始化摄像头
        self.cap = cv2.VideoCapture()
        # 设置默认采集的照片数量
        self.Dialog.label_collect_sum.setText(f'{COLLENCT_FACE_NUM_DEFAULT}')
        # 初始化已经采集的人脸数目
        self.have_token_photos = 0

    def handle_click(self):
        if not self.isVisible():
            self.show()

    def handle_close(self):
        self.open_camera()
        self.close()

    def open_camera(self):
        # 判断摄像头是否打开，如果打开则为true，反之为false
        if not self.cap.isOpened():
            if LOCAL_USER["id"] != '':
                self.have_token_photos = 0
                self.Dialog.label_camera_layout.clear()
                self.cap.open(CAMERA_ID)
                self.show_capture()
        else:
            self.cap.release()
            # self.Dialog.label_camera_layout.clear()
            self.Dialog.bt_face_collecting.setText(u'开始采集')

    def show_capture(self):
        # 读取当前用户信息
        staff_id = LOCAL_USER["id"]

        self.Dialog.bt_face_collecting.setText(u'停止采集')
        self.Dialog.label_collecting_note.setText('请注视摄像头')
        self.Dialog.label_camera_layout.clear()
        print("[INFO] starting video stream...")
        loop_num = 0
        interval = 30  # 暂用两张图片的间隔代替识别不同面部姿势和表情
        face_features = []  # 人脸面部数据,矩阵
        numNeed = COLLENCT_FACE_NUM_DEFAULT     # 需要的面部数据数量
        # 循环来自视频文件流的帧
        while self.cap.isOpened():
            # 循环自增
            loop_num += 1
            ret, frame = self.cap.read()
            QApplication.processEvents()
            frame = imutils.resize(frame, width=500)
            show_video = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 这里指的是显示原图
            # opencv读取图片的样式，不能通过Qlabel进行显示，需要转换为Qimage。
            self.showImage = QImage(show_video.data,
                                    show_video.shape[1],
                                    show_video.shape[0],
                                    QImage.Format_RGB888)
            self.Dialog.label_camera_layout.setPixmap(
                QPixmap.fromImage(self.showImage))

            # 后期应有其他判断需要计算标准，如姿势符合,这里用的是每300帧只采集一份数据
            if len(face_features) * interval < loop_num:
                faceRects = getFacePosition(frame)
                if len(faceRects) == 1:  # 只在镜头中只有一个人时计算面部数据
                    print(face_features)
                    self.Dialog.label_collected_num.setText(f"{len(face_features)}")
                    face_features.append(getFaceData(frame, faceRects[0]))
                    if numNeed <= len(face_features):
                        break
                        # 这里做数据采集完成的处理
                        # break


        # 因为最后一张画面会显示在GUI中，此处实现清除。
        self.Dialog.label_camera_layout.clear()

        # 采集结束时上传数据
        print("np.mat:", np.array(face_features))
        r = commitFaceData(np.array(face_features), staff_id, LOCAL_USER['flag'])
        if r["status"]==1:
            QMsgBox.showMsg("采集完成")
            LOCAL_USER['if_face'] = True
            # 直接存储采集完成的数据, 数据和其他信息分开写
            localSaveMatrix('face_features.npz', face_features)   # 数据

            # 读取local文件
            local = open('local.json', 'r')
            content = local.read()
            if content != '':
                local_status = json.loads(content)
            else:
                local_status = {}
            local.close()

            local_status["accuracy"] = r['data']["accuracy"]
            local_status["flag_id"] = r['data']["flag_id"]

            # 写入文件
            local = open('local.json', 'w')
            b = json.dumps(local_status)
            local.write(b)
            local.close()

            self.cap.release()
            self.close()

        else:
            QMsgBox.showMsg("采集失败，请重新采集！")


