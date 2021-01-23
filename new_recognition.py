# 動態人臉識別

import cv2

def recognition(memberid):

    # 建立 人臉辨識器物件
    model = cv2.face.LBPHFaceRecognizer_create()
    # 讀取 人臉辨識模型
    model.read('./model/%s.data' % memberid)

    # 建立 人臉分類器物件
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # 打開攝影機
    cap = cv2.VideoCapture(0)
    # 打開視窗
    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        # 讀取影像
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.flip(frame, 1)
        # 轉灰階
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 偵測人臉
        faces = face_cascade.detectMultiScale(gray, 1.1, 3)
        for (x, y, w, h) in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            face_img = cv2.resize(gray[y: y + h, x: x + w], (400, 400))
            try:
                params = model.predict(face_img)
                print('label: {}, confidence: {}'.format(params[0], params[1]))

                if params[1] > 70:
                    cv2.destroyAllWindows()
                    cap.release()
                    return params[1]

                if params[1] < 50:
                    text = ['confirmed']
                    cv2.putText(frame, text[params[0]], (x, y - 10),
                                font, 1, (255,255,0), 3, cv2.LINE_AA)
                    if params[1] < 30:
                        cap.release()
                        return params[1]
            except:
                # 如果不是持續偵測
                continue

        cv2.imshow('video', frame)
        # ESC 結束
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            break
if __name__ == '__main__':
    recognition('bubufun')