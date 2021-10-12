import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui.QMsgBox import Ui_Dialog

PADDING = 4


# 创建静态变量的装饰器
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


class QMsgBox(QDialog, Ui_Dialog):
    def __init__(self, msg: str, parent=None):
        super(QMsgBox, self).__init__(parent)
        self.setupUi(self)
        self.label.setText(msg)
        # 设置背景透明
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_QuitOnClose, True)

        self.pushButton.clicked.connect(self.accept)
        self.pushButton_2.clicked.connect(self.reject)

        self.pushButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pushButton_2.setCursor(Qt.CursorShape.PointingHandCursor)

        # 无边框移动
        self.SHADOW_WIDTH = 0  # 边框距离
        self.isLeftPressDown = False  # 鼠标左键是否按下
        self.dragPosition = 0  # 拖动时坐标
        self.Numbers = self.enum(UP=0, DOWN=1, LEFT=2, RIGHT=3, LEFTTOP=4, LEFTBOTTOM=5,
                                 RIGHTBOTTOM=6, RIGHTTOP=7, NONE=8)  # 枚举参数
        self.dir = self.Numbers.NONE  # 初始鼠标状态
        self.setMouseTracking(True)

    # 静态方法创建消息提示
    @staticmethod
    @static_vars(tip=None)
    def showMsg(msg):
        QMsgBox.showMsg.tip = QMsgBox(msg)
        # QMsgBox.showMsg.tip.exec_()
        if QMsgBox.showMsg.tip.exec_() == 1:
            return 1  # 确定
        else:
            return 0  # 取消

    # 绘制边框阴影
    def drawShadow(self, painter):
        # 绘制左上角、左下角、右上角、右下角、上、下、左、右边框
        painter.drawPixmap(0, 0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, QPixmap(self.pixmaps[0]))  # 左上角
        painter.drawPixmap(self.width() - self.SHADOW_WIDTH, 0, self.SHADOW_WIDTH, self.SHADOW_WIDTH,
                           QPixmap(self.pixmaps[2]))  # 右上角
        painter.drawPixmap(0, self.height() - self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.SHADOW_WIDTH,
                           QPixmap(self.pixmaps[1]))  # 左下角
        painter.drawPixmap(self.width() - self.SHADOW_WIDTH, self.height() - self.SHADOW_WIDTH, self.SHADOW_WIDTH,
                           self.SHADOW_WIDTH, QPixmap(self.pixmaps[3]))  # 右下角
        painter.drawPixmap(0, self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.height() - 2 * self.SHADOW_WIDTH,
                           QPixmap(self.pixmaps[6]).scaled(self.SHADOW_WIDTH,
                                                           self.height() - 2 * self.SHADOW_WIDTH))  # 左
        painter.drawPixmap(self.width() - self.SHADOW_WIDTH, self.SHADOW_WIDTH, self.SHADOW_WIDTH,
                           self.height() - 2 * self.SHADOW_WIDTH, QPixmap(self.pixmaps[7]).scaled(self.SHADOW_WIDTH,
                                                                                                  self.height() - 2 * self.SHADOW_WIDTH))  # 右
        painter.drawPixmap(self.SHADOW_WIDTH, 0, self.width() - 2 * self.SHADOW_WIDTH, self.SHADOW_WIDTH,
                           QPixmap(self.pixmaps[4]).scaled(self.width() - 2 * self.SHADOW_WIDTH,
                                                           self.SHADOW_WIDTH))  # 上
        painter.drawPixmap(self.SHADOW_WIDTH, self.height() - self.SHADOW_WIDTH, self.width() - 2 * self.SHADOW_WIDTH,
                           self.SHADOW_WIDTH, QPixmap(self.pixmaps[5]).scaled(self.width() - 2 * self.SHADOW_WIDTH,
                                                                              self.SHADOW_WIDTH))  # 下

    # 枚举参数
    def enum(self, **enums):
        return type('Enum', (), enums)

    def region(self, cursorGlobalPoint):
        # 获取窗体在屏幕上的位置区域，tl为topleft点，rb为rightbottom点
        rect = self.rect()
        tl = self.mapToGlobal(rect.topLeft())
        rb = self.mapToGlobal(rect.bottomRight())

        x = cursorGlobalPoint.x()
        y = cursorGlobalPoint.y()

        if (tl.x() + PADDING >= x and tl.x() <= x and tl.y() + PADDING >= y and tl.y() <= y):
            # 左上角
            self.dir = self.Numbers.LEFTTOP
            self.setCursor(QCursor(Qt.SizeFDiagCursor))  # 设置鼠标形状
        elif (x >= rb.x() - PADDING and x <= rb.x() and y >= rb.y() - PADDING and y <= rb.y()):
            # 右下角
            self.dir = self.Numbers.RIGHTBOTTOM
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif (x <= tl.x() + PADDING and x >= tl.x() and y >= rb.y() - PADDING and y <= rb.y()):
            # 左下角
            self.dir = self.Numbers.LEFTBOTTOM
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif (x <= rb.x() and x >= rb.x() - PADDING and y >= tl.y() and y <= tl.y() + PADDING):
            # 右上角
            self.dir = self.Numbers.RIGHTTOP
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif (x <= tl.x() + PADDING and x >= tl.x()):
            # 左边
            self.dir = self.Numbers.LEFT
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif (x <= rb.x() and x >= rb.x() - PADDING):
            # 右边

            self.dir = self.Numbers.RIGHT
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif (y >= tl.y() and y <= tl.y() + PADDING):
            # 上边
            self.dir = self.Numbers.UP
            self.setCursor(QCursor(Qt.SizeVerCursor))
        elif (y <= rb.y() and y >= rb.y() - PADDING):
            # 下边
            self.dir = self.Numbers.DOWN
            self.setCursor(QCursor(Qt.SizeVerCursor))
        else:
            # 默认
            self.dir = self.Numbers.NONE
            self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.isLeftPressDown = False
            if (self.dir != self.Numbers.NONE):
                self.releaseMouse()
                self.setCursor(QCursor(Qt.ArrowCursor))

    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.isLeftPressDown = True
            if (self.dir != self.Numbers.NONE):
                self.mouseGrabber()
            else:
                self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        gloPoint = event.globalPos()
        rect = self.rect()
        tl = self.mapToGlobal(rect.topLeft())
        rb = self.mapToGlobal(rect.bottomRight())

        if (not self.isLeftPressDown):
            self.region(gloPoint)
        else:
            if (self.dir != self.Numbers.NONE):
                rmove = QRect(tl, rb)
                if (self.dir == self.Numbers.LEFT):
                    if (rb.x() - gloPoint.x() <= self.minimumWidth()):
                        rmove.setX(tl.x())
                    else:
                        rmove.setX(gloPoint.x())
                elif (self.dir == self.Numbers.RIGHT):
                    print
                    u"youbian"
                    rmove.setWidth(gloPoint.x() - tl.x())
                elif (self.dir == self.Numbers.UP):
                    if (rb.y() - gloPoint.y() <= self.minimumHeight()):
                        rmove.setY(tl.y())
                    else:
                        rmove.setY(gloPoint.y())
                elif (self.dir == self.Numbers.DOWN):
                    rmove.setHeight(gloPoint.y() - tl.y())
                elif (self.dir == self.Numbers.LEFTTOP):
                    if (rb.x() - gloPoint.x() <= self.minimumWidth()):
                        rmove.setX(tl.x())
                    else:
                        rmove.setX(gloPoint.x())
                    if (rb.y() - gloPoint.y() <= self.minimumHeight()):
                        rmove.setY(tl.y())
                    else:
                        rmove.setY(gloPoint.y())
                elif (self.dir == self.Numbers.RIGHTTOP):
                    rmove.setWidth(gloPoint.x() - tl.x())
                    rmove.setY(gloPoint.y())
                elif (self.dir == self.Numbers.LEFTBOTTOM):
                    rmove.setX(gloPoint.x())
                    rmove.setHeight(gloPoint.y() - tl.y())
                elif (self.dir == self.Numbers.RIGHTBOTTOM):
                    rmove.setWidth(gloPoint.x() - tl.x())
                    rmove.setHeight(gloPoint.y() - tl.y())
                else:
                    pass
                self.setGeometry(rmove)
            else:
                self.move(event.globalPos() - self.dragPosition)
                event.accept()
