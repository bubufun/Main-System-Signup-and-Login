# 獲取人臉資料

import cv2
import os

# 將圖像存在 xxx.pgm檔
def saveImage(image, memberid, index):
    if not os.path.exists('./images'):
        os.mkdir('./images')
    if not os.path.exists('./images/%s' % memberid):
        os.mkdir('./images/%s' % memberid)
    filename = 'images/{}/{:02d}.pgm'.format(memberid,index)
    cv2.imwrite(filename, image)
    print('註冊中，請稍後...')


def data_capture(memberid):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    cap = cv2.VideoCapture(0)

    n = 1
    idx = 0
    max_idx = 100

    while n > 0:

        ret, frame = cap.read()
        frame = cv2.resize(frame, (600, 480))
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 3)


        for (x, y, w, h) in faces:
            # 畫綠框
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            # 準備時間
            if n % 5 == 0:
                # 轉成灰階影像
                face_img = cv2.resize(gray[y: y + h, x: x + w], (400, 400))
                # 存影像
                saveImage(face_img, memberid, idx)
                idx += 1
                # 100 >= 100 存一百張影像
                if idx >= max_idx:
                    # print('get training data done')
                    # 中止 while 循環
                    n = -1
                    # for 循環結束
                    break
            n += 1

        # break後 執行

        cv2.imshow('video', frame)
        cv2.waitKey(1)


    cap.release()  # 關閉cam
    cv2.destroyWindow("video")

if __name__ == '__main__':
    memberid = input('請輸入id:')
    data_capture(memberid)