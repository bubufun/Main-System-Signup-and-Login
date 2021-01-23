# 訓練人臉識別資料

import cv2
import numpy as np
import os


def training_data(memberid):
    images = []
    labels = []

    for index in range(100):
        filename = 'images/{}/{:02d}.pgm'.format(memberid,index)
        # print('read ' + filename)
        # 讀取 images/memberid/index.pgm
        img = cv2.imread(filename, cv2.COLOR_BGR2GRAY)
        # 加入至 image list
        images.append(img)
        # 給一個編號
        labels.append(0)

    # 訓練開始
    print('註冊中...')
    # 建立 人臉識別器物件
    model = cv2.face.LBPHFaceRecognizer_create()
    # 訓練識別器
    model.train(np.asarray(images), np.asarray(labels))
    # 儲存識別器

    if not os.path.exists('./model'):
        os.mkdir('./model')
    model.save('./model/%s.data' % memberid)
    # 訓練結束
    print('註冊完畢!!')

if __name__ == '__main__':
    memberid = input('請輸入id:')
    training_data(memberid)
