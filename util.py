import socket
import cv2
import numpy as np
import time
import sys
from binaryReader import BinaryReader

def buildConn(address):
    try:
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        return sock,None
    except socket.error as msg:
        return None,msg


def recvData(sock, count):
    data = b''
    while len(data) < count:
        packet = sock.recv(count - len(data))
        if not packet:
            return None
        data += packet
    return data

def sendData(sock, data):
    totalsent = 0
    msg_length = len(data)
    while totalsent < msg_length:
        sent = sock.send(data[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connetction broken")
        totalsent = totalsent + sent

def recvDataLenAndContent(sock, unitSize=1):
    sizeDataBytes = recvData(sock, 4)
    reader = BinaryReader()
    size = reader.read(sizeDataBytes, 'int32')[0]
    dataBytes = recvData(sock, size * unitSize)
    return dataBytes

def decodeRgbImgFromBytes(databytes):
    data = np.frombuffer(databytes, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return img

def decodeGrayImgFromBytes(databytes):
    data = np.frombuffer(databytes, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
    return img

def sendDataLenAndContent(sock, num, databytes):
    sizebytes = np.array(num, dtype=np.int32).tobytes()
    sendData(sock, sizebytes)
    sendData(sock, databytes)


from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *






class AeroButton(QPushButton):
    def __init__(self, a, b, c, parent=None):
        super(AeroButton, self).__init__(parent)
        # self.setEnabled(True)
        self.a = a
        self.b = b
        self.c = c
        self.hovered = False
        self.pressed = False
        self.color = QColor(Qt.gray)
        self.hightlight = QColor(Qt.lightGray)
        self.shadow = QColor(Qt.black)
        self.opacity = 1.0
        self.roundness = 0

    def change(self,file):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if (self.isEnabled()):
            if self.hovered:
                self.color = self.hightlight.darker(250)
        else:
            self.color = QColor(50, 50, 50)

        button_rect = QRect(self.geometry())
        painter.setPen(QPen(QBrush(Qt.red), 2.0))
        painter_path = QPainterPath()
        # painter_path.addRoundedRect(1, 1, button_rect.width() - 2, button_rect.height() - 2, self.roundness, self.roundness)
        painter_path.addEllipse(1, 1, button_rect.width() - 2, button_rect.height() - 2)
        painter.setClipPath(painter_path)
        icon_size = self.iconSize()
        icon_position = self.calculateIconPosition(button_rect, icon_size)
        painter.setOpacity(1.0)
        painter.drawPixmap(icon_position, QPixmap(QIcon(file).pixmap(icon_size)))
        painter.end()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if (self.isEnabled()):
            if self.hovered:
                self.color = self.hightlight.darker(250)
        else:
            self.color = QColor(50, 50, 50)

        button_rect = QRect(self.geometry())
        painter.setPen(QPen(QBrush(Qt.red), 2.0))
        painter_path = QPainterPath()
        # painter_path.addRoundedRect(1, 1, button_rect.width() - 2, button_rect.height() - 2, self.roundness, self.roundness)
        painter_path.addEllipse(1, 1, button_rect.width() - 2, button_rect.height() - 2)
        painter.setClipPath(painter_path)
        if self.isEnabled():
            if (self.pressed == False and self.hovered == False):
                icon_size = self.iconSize()
                icon_position = self.calculateIconPosition(button_rect, icon_size)
                painter.setOpacity(1.0)
                painter.drawPixmap(icon_position, QPixmap(QIcon(self.a).pixmap(icon_size)))
            elif (self.hovered == True and self.pressed == False):
                icon_size = self.iconSize()
                icon_position = self.calculateIconPosition(button_rect, icon_size)
                painter.setOpacity(1.0)
                painter.drawPixmap(icon_position, QPixmap(QIcon(self.b).pixmap(icon_size)))
            elif self.pressed == True:
                icon_size = self.iconSize()
                icon_position = self.calculateIconPosition(button_rect, icon_size)
                painter.setOpacity(1.0)
                painter.drawPixmap(icon_position, QPixmap(QIcon(self.c).pixmap(icon_size)))
        else:
            icon_size = self.iconSize()
            icon_position = self.calculateIconPosition(button_rect, icon_size)
            painter.setOpacity(1.0)
            painter.drawPixmap(icon_position, QPixmap(QIcon(self.a).pixmap(icon_size)))

    def enterEvent(self, event):
        self.hovered = True
        self.repaint()
        QPushButton.enterEvent(self, event)

    def leaveEvent(self, event):
        self.hovered = False;
        self.repaint()
        QPushButton.leaveEvent(self, event)

    def mousePressEvent(self, event):
        self.pressed = True
        self.repaint()
        QPushButton.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):

        self.pressed = False
        self.repaint()
        QPushButton.mouseReleaseEvent(self, event)

    def calculateIconPosition(self, button_rect, icon_size):

        x = (button_rect.width() / 2) - (icon_size.width() / 2)
        y = (button_rect.height() / 2) - (icon_size.height() / 2)

        width = icon_size.width()
        height = icon_size.height()

        icon_position = QRect()
        icon_position.setX(x)
        icon_position.setY(y)
        icon_position.setWidth(width)
        icon_position.setHeight(height)

        return icon_position
