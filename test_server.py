import time
import sys
import cv2
import numpy as np
import threading
import json
from util import *
import random
class test_server():
    def __init__(self):
        address = ('127.0.0.1', 8002)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(address)
        self.s.listen(5)
        while True:
            client, add = self.s.accept()
            print(add)# 阻塞，等待客户端连接
            # 加入连接池
            # 给每个客户端创建一个独立的线程进行管理
            thread =threading.Thread(target=client_handle, args=(client,))
            # 设置成守护线程
            thread.setDaemon(True)
            thread.start()


def client_handle(client):
    receive = client.recv(1024)
    type=str(receive, encoding='utf-8')
    if type=='Message':
        while 1:
            res={'key':'State3DCamera','value':random.sample(range(0,2),1)[0]}
            res = json.dumps(res)
            client.send(res.encode('utf-8'))
            client_ack = client.recv(1024)
            res={'key':'State2DCamera','value':random.sample(range(0,2),1)[0]}
            res = json.dumps(res)
            client.send(res.encode('utf-8'))
            client_ack = client.recv(1024)
            res={'key':'Sucker','x':random.sample(range(0,2),1)[0],'y':random.sample(range(0,2),1)[0],'z':random.sample(range(0,2),1)[0]}
            res = json.dumps(res)
            client.send(res.encode('utf-8'))
            client_ack = client.recv(1024)
            res={'key':'StateTongs','x':random.sample(range(0,100),1)[0],'y':random.sample(range(0,100),1)[0],'z':random.sample(range(0,100),1)[0],'a':random.sample(range(0,100),1)[0],'b':random.sample(range(0,100),1)[0],'c':random.sample(range(0,100),1)[0]}
            res = json.dumps(res)
            client.send(res.encode('utf-8'))
            client_ack = client.recv(1024)
            res={'key':'NumFinish','value':random.sample(range(0,100),1)[0]}
            res = json.dumps(res)
            client.send(res.encode('utf-8'))
            client_ack = client.recv(1024)
            res={'key':'NumUnsuccessful','value':random.sample(range(0,100),1)[0]}
            res = json.dumps(res)
            client.send(res.encode('utf-8'))
            client_ack = client.recv(1024)
            res = {'key': 'StateRobot', 'value': random.sample(['正常','不正常','非常不正常'], 1)[0]}
            res = json.dumps(res)
            client.send(res.encode('utf-8'))
            client_ack = client.recv(1024)
            res = {'key': 'Code', 'value': random.sample(['正常', '不正常', '非常不正常'], 1)[0]}
            res = json.dumps(res)
            client.send(res.encode('utf-8'))
            client_ack = client.recv(1024)
            time.sleep(1)
    elif type=='Picture':
        capture = cv2.VideoCapture('aiqing.mp4')  #
        ret, frame = capture.read()
        while ret:
            time.sleep(0.01)
            img_str = cv2.imencode('.png', frame)[1].tostring()
            sendDataLenAndContent(client, len(img_str), img_str)
            ret, frame = capture.read()
    else:
        print('未识别消息客户端类型')

test_server()
