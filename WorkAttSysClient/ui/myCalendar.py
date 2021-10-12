import typing
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRect, QDate, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QCalendarWidget


class MyCalendarWidget(QCalendarWidget):
    def __init__(self, parent=None):
        super(MyCalendarWidget, self).__init__(parent)

    def paintCell(self, painter: QtGui.QPainter, rect: QtCore.QRect,
                  date: typing.Union[QtCore.QDate, datetime.date]) -> None:
        if date == self.selectedDate():
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(255, 183, 134))
            painter.drawEllipse(QRect(rect.x() + rect.width() / 2 - 10, rect.y() + rect.height() / 2 - 10, 20, 20))
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(rect, Qt.AlignCenter, str(date.day()))
            painter.restore()
        elif date == QDate.currentDate():
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QColor(255, 183, 134))
            painter.drawText(rect, Qt.AlignCenter, str(date.day()))
            painter.restore()
        elif date < self.minimumDate() or date > self.maximumDate():
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)
            # painter.setBrush(QColor(249, 249, 249))
            # painter.drawRect(rect.x(), rect.y() + 3, rect.width(), rect.height() - 6)
            painter.setPen(QColor(0, 0, 0))
            painter.drawText(rect, Qt.AlignCenter, str(date.day()))
            painter.restore()
        else:
            QCalendarWidget.paintCell(self, painter, rect, date)

