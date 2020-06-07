import time
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import cv2
import numpy as np
import threading
import json
from util import *

import myWindow

class MainWindow():
    def __init__(self):
        self.address1=('127.0.0.1',8002)
        self.address2=('127.0.0.1',8002)
        app = QApplication(sys.argv)
        self.mainWindow = QMainWindow()
        self.raw_image = None
        self.ui = myWindow.Ui_MainWindow()
        self.ui.setupUi(self.mainWindow)
        self.action_connect()
        self.mainWindow.show()
        self.running=0
        self.mes_sock=None
        self.pic_sock=None
        self.start_time=0
        sys.exit(app.exec_())

    def action_connect(self):
        self.ui.pushButton_1.clicked.connect(self.start_robot)
        self.ui.pushButton_2.clicked.connect(self.stop_robot)
        # self.ui.pushButton_3.clicked.connect(self.start_robot)
        self.ui.pushButton_4.clicked.connect(self.reset_robot)
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.ui.lcdNumber_7.setDigitCount(8)
        self.ui.lcdNumber_7.setMode(QLCDNumber.Dec)
        self.ui.lcdNumber_8.setDigitCount(8)
        self.ui.lcdNumber_8.setMode(QLCDNumber.Dec)
        self.ui.lcdNumber_9.setDigitCount(8)
        self.ui.lcdNumber_9.setMode(QLCDNumber.Dec)

        self.ui.lineEdit_1.setEnabled(False)
        self.ui.lineEdit_2.setEnabled(False)
        self.ui.label_2.setEnabled(False)
        self.ui.label_3.setEnabled(False)
        # self.ui.label_12.setEnabled(False)
        # self.ui.label_20.setEnabled(False)
        # self.ui.label_21.setEnabled(False)
        self.ui.label_12.stateChanged.connect(self.change_sucker)
        self.ui.label_20.stateChanged.connect(self.change_sucker)
        self.ui.label_21.stateChanged.connect(self.change_sucker)

    def change_sucker(self):
        f1,f2,f3=self.ui.label_12.isChecked(),self.ui.label_20.isChecked(),self.ui.label_21.isChecked()
        if f1:
            f1=1
        else:
            f1=0
        if f2:
            f2=1
        else:
            f2=0
        if f3:
            f3 = 1
        else:
            f3 = 0
        try:
            res = {'key': 'Sucker', 'x':f1,'y':f2,'z':f3}
            res = json.dumps(res)
            self.mes_sock.send(res.encode('utf-8'))
        except:
            print(res)


    def start_robot(self):
        self.mes_sock,flag1=buildConn(self.address1)
        self.pic_sock,flag2=buildConn(self.address2)
        if self.mes_sock and self.pic_sock:
            reply = QMessageBox.about(self.mainWindow,'状态','连接成功')
            self.mes_sock.send(bytes('Message', encoding='utf-8'))
            self.pic_sock.send(bytes('Picture', encoding='utf-8'))
            self.start_timer()
            start_mes = threading.Thread(target=self.mes_reciever)
            start_mes.start()
            start_pic = threading.Thread(target=self.pic_reciever)
            start_pic.start()

        else:
            print(flag2, flag1)
            reply = QMessageBox.about(self.mainWindow, '状态', '连接失败')
    def stop_robot(self):
        self.mes_sock.send(bytes('Stop', encoding='utf-8'))
        self.timer.stop()
    def reset_robot(self):
        self.mes_sock.send(bytes('Reset', encoding='utf-8'))
        self.start_time=time.time()
    def start_timer(self):
        self.start_time=time.time()
        self.timer.start(1000)




    def showTime(self):
        curr_time =time.time()
        duration=round(curr_time-self.start_time)
        duration= str(duration//60)+':'+ str(duration%60)
        self.ui.lcdNumber_9.display(duration)

    def mes_reciever(self):
        while 1:
            try:
                response = self.mes_sock.recv(1024)
                print(response)
                mes = json.loads(response.decode('utf-8'))
                print(mes)
                if mes['key']=='State3DCamera':
                    print('asd')
                    if mes['value'] == 1:
                        self.ui.label_2.setChecked(True)
                    else:
                        self.ui.label_2.setChecked(False)
                    self.mes_sock.send('ack'.encode('utf-8'))
                elif mes['key']=='State2DCamera':
                    if mes['value'] == 1:
                        self.ui.label_3.setChecked(True)
                    else:
                        self.ui.label_3.setChecked(False)
                    self.mes_sock.send('ack'.encode('utf-8'))
                elif mes['key']=='NumFinish':
                    value= mes['value']
                    self.ui.lcdNumber_7.display(str(value))
                    self.mes_sock.send('ack'.encode('utf-8'))
                elif mes['key']=='NumUnsuccessful':
                    value = mes['value']
                    self.ui.lcdNumber_8.display(str(value))
                    self.mes_sock.send('ack'.encode('utf-8'))
                elif mes['key']=='StateTongs':
                    x= mes['x']
                    y= mes['y']
                    z= mes['z']
                    a= mes['a']
                    b= mes['b']
                    c= mes['c']
                    self.ui.lcdNumber_1.display(str(x))
                    self.ui.lcdNumber_2.display(str(y))
                    self.ui.lcdNumber_3.display(str(z))
                    self.ui.lcdNumber_4.display(str(a))
                    self.ui.lcdNumber_5.display(str(b))
                    self.ui.lcdNumber_6.display(str(c))
                    self.mes_sock.send('ack'.encode('utf-8'))
                elif mes['key']=='Sucker':
                    if mes['x'] == 1:
                        # self.ui.label_12.setStyleSheet("image: url(:/light_green.jpg);")
                        self.ui.label_12.setChecked(True)
                    else:
                        # self.ui.label_12.setStyleSheet("image: url(:/light_white.jpg);")
                        self.ui.label_12.setChecked(False)
                    if mes['y'] == 1:
                        self.ui.label_20.setChecked(True)
                    else:
                        self.ui.label_20.setChecked(False)
                    if mes['z'] == 1:
                        self.ui.label_21.setChecked(True)
                    else:
                        self.ui.label_21.setChecked(False)
                    self.mes_sock.send('ack'.encode('utf-8'))
                elif mes['key']=='StateRobot':
                    self.ui.lineEdit_1.setText(mes['value'])
                    self.mes_sock.send('ack'.encode('utf-8'))
                elif mes['key']=='Code':
                    self.ui.lineEdit_2.setText(mes['value'])
                    self.mes_sock.send('ack'.encode('utf-8'))
                else:
                    print('unkown message')
            except:
                print('接收失败',)

    def pic_reciever(self):
        while 1:
            try:
                data = recvDataLenAndContent(self.pic_sock, 1)
                decimg = decodeRgbImgFromBytes(data)
                show = cv2.cvtColor(decimg, cv2.COLOR_BGR2RGB)
                showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
                label=self.ui.label
                img= QPixmap.fromImage(showImage).scaled(label.width(), label.height())
                label.setPixmap(img)
            except:
                print('图像接收失败')

MainWindow()