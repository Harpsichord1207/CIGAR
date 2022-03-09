# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 11:43:47 2018

@author: Administrator
"""

'''
调用opencv的库实现人脸识别
'''

import cv2
import numpy as np
import os
import shutil

# 创建一个手势识别
from handutil import HandDetector

detector = HandDetector()
# 6张手的图片，分别代表0～5
finger_img_list = [
    'fingers/0.png',
    'fingers/1.png',
    'fingers/2.png',
    'fingers/3.png',
    'fingers/4.png',
    'fingers/5.png',
]
finger_list = []
for fi in finger_img_list:
    i = cv2.imread(fi)
    finger_list.append(i)

# 指尖列表，分别代表大拇指、食指、中指、无名指和小指的指尖
tip_ids = [4, 8, 12, 16, 20]


# 采集自己的人脸数据
def generator(data):
    '''
    打开摄像头，读取帧，检测该帧图像中的人脸，并进行剪切、缩放
    生成图片满足以下格式：
    1.灰度图，后缀为 .png
    2.图像大小相同
    params:
        data:指定生成的人脸数据的保存路径
    '''

    name = input('my name:')
    # 如果路径存在则删除路径
    path = os.path.join(data, name)
    if os.path.isdir(path):
        shutil.rmtree(path)
    # 创建文件夹
    os.mkdir(path)
    # 创建一个级联分类器
    face_casecade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    # 打开摄像头
    camera = cv2.VideoCapture(0)
    cv2.namedWindow('Dynamic')
    # 计数
    count = 1

    while (True):
        # 读取一帧图像
        ret, frame = camera.read()
        if ret:
            # 转换为灰度图
            gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 人脸检测
            face = face_casecade.detectMultiScale(gray_img, 1.3, 5)
            for (x, y, w, h) in face:
                # 在原图上绘制矩形
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # 调整图像大小
                new_frame = cv2.resize(frame[y:y + h, x:x + w], (92, 112))
                # 保存人脸
                cv2.imwrite('%s/%s.png' % (path, str(count)), new_frame)
                count += 1
            cv2.imshow('Dynamic', frame)
            # 按下q键退出
            if cv2.waitKey(100) & 0xff == ord('q'):
                break
    camera.release()
    cv2.destroyAllWindows()


# 载入图像   读取ORL人脸数据库，准备训练数据
def LoadImages(data):
    '''
    加载图片数据用于训练
    params:
        data:训练数据所在的目录，要求图片尺寸一样
    ret:
        images:[m,height,width]  m为样本数，height为高，width为宽
        names：名字的集合
        labels：标签
    '''
    images = []
    names = []
    labels = []

    label = 0

    # 遍历所有文件夹
    for subdir in os.listdir(data):
        subpath = os.path.join(data, subdir)
        # print('path',subpath)
        # 判断文件夹是否存在
        if os.path.isdir(subpath):
            # 在每一个文件夹中存放着一个人的许多照片
            names.append(subdir)
            # 遍历文件夹中的图片文件
            for filename in os.listdir(subpath):
                imgpath = os.path.join(subpath, filename)
                img = cv2.imread(imgpath, cv2.IMREAD_COLOR)
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # cv2.imshow('1',img)
                # cv2.waitKey(0)
                images.append(gray_img)
                labels.append(label)
            label += 1
    images = np.asarray(images)
    # names=np.asarray(names)
    labels = np.asarray(labels)
    return images, labels, names


def get_finger(success, img, name):
    if success:
        # 检测手势
        img = detector.find_hands(img, draw=True)
        # 获取手势数据
        lmslist = detector.find_positions(img)
        if len(lmslist) > 0:
            fingers = []
            for tid in tip_ids:
                # 找到每个指尖的位置
                x, y = lmslist[tid][1], lmslist[tid][2]
                cv2.circle(img, (x, y), 10, (0, 255, 0), cv2.FILLED)
                # 如果是大拇指，如果大拇指指尖x位置大于大拇指第二关节的位置，则认为大拇指打开，否则认为大拇指关闭
                if tid == 4:
                    if lmslist[tid][1] > lmslist[tid - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                # 如果是其他手指，如果这些手指的指尖的y位置大于第二关节的位置，则认为这个手指打开，否则认为这个手指关闭
                else:
                    if lmslist[tid][2] < lmslist[tid - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
            # fingers是这样一个列表，5个数据，0代表一个手指关闭，1代表一个手指打开
            # 判断有几个手指打开
            cnt = fingers.count(1)
            if name != "xufei":
                if cnt == 0:
                    finger_img = finger_list[5]
                elif cnt == 1 or cnt == 2:
                    finger_img = finger_list[0]
                elif cnt == 5:
                    finger_img = finger_list[2]
                else:
                    finger_img = finger_list[cnt]
            else:
                if cnt == 0:
                    finger_img = finger_list[2]
                elif cnt == 1 or cnt == 2:
                    finger_img = finger_list[5]
                elif cnt == 5:
                    finger_img = finger_list[0]
                else:
                    finger_img = finger_list[cnt]
            # 找到对应的手势图片并显示

            # finger_img = finger_list[cnt]
            w, h, c = finger_img.shape
            img[0:w, 0:h] = finger_img
            cv2.rectangle(img, (0, 0), (0, 0), (0, 255, 0), cv2.FILLED)
            if name != "xufei" and cnt in [1, 2, 5, 0]:
                cv2.putText(img, "lose", (200, 100), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 0, 255))

            elif name == "xufei" and cnt in [1, 2, 5, 0]:
                cv2.putText(img, "win", (200, 100), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 0, 255))
            else:
                cv2.putText(img, "X", (200, 100), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 0, 255))

        cv2.imshow('Image', img)


# 检验训练结果
def FaceRec(data):
    # 加载训练的数据
    X, y, names = LoadImages(data)
    # print('x',X)
    model = cv2.face.EigenFaceRecognizer_create()
    model.train(X, y)

    # 打开摄像头
    camera = cv2.VideoCapture(0)
    cv2.namedWindow('Dynamic')

    # 创建级联分类器
    face_casecade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

    while (True):
        # 读取一帧图像
        # ret:图像是否读取成功
        # frame：该帧图像
        ret, frame = camera.read()
        if ret:
            # 转换为灰度图
            gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 利用级联分类器鉴别人脸
            faces = face_casecade.detectMultiScale(gray_img, 1.3, 5)
            # 遍历每一帧图像，画出矩形
            for (x, y, w, h) in faces:
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # 蓝色
                roi_gray = gray_img[y:y + h, x:x + w]
                try:
                    # 将图像转换为宽92 高112的图像
                    # resize（原图像，目标大小，（插值方法）interpolation=，）
                    roi_gray = cv2.resize(roi_gray, (92, 112), interpolation=cv2.INTER_LINEAR)
                    params = model.predict(roi_gray)
                    print(names[params[0]])
                    print('Label:%s,confidence:%.2f' % (params[0], params[1]))
                    get_finger(ret, frame, names[params[0]])
                    '''
                    putText:给照片添加文字
                    putText(输入图像，'所需添加的文字'，左上角的坐标，字体，字体大小，颜色，字体粗细)
                    '''
                    cv2.putText(frame, names[params[0]], (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
                except:
                    continue

            cv2.imshow('Dynamic', frame)

            # 按下q键退出
            if cv2.waitKey(100) & 0xff == ord('q'):
                break
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    data = './face'
    #generator(data)
    FaceRec(data)
