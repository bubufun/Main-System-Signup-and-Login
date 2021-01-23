import cv2
from datetime import datetime
import db_created
import new_recognition
import new_mongo_connect
import new_kafka_producer

def member_login():

    while True:

        memberid = input('進入商店前，請輸入您帳號 (直接按「Enter」則回到上一選單)：')

        conn = db_created.db_connect_host()
        cursor = conn.cursor()

        sql = 'SELECT * FROM login_check where memberid = "%s"' % memberid
        cursor.execute(sql)
        login_check = cursor.fetchall()

        sql2 = 'SELECT * FROM member_signup where memberid = "%s"' % memberid
        cursor.execute(sql2)
        info = cursor.fetchall()

        if memberid == '':  # 未輸入帳號就結束
            cursor.close()
            conn.close()
            break

        elif login_check:  # 帳號已存在
            cursor.close()
            conn.close()
            print('已重複登入系統！，若要結帳請直接按「Enter」則回到上一選單，並選取結帳謝謝')

        elif not info:# 帳號不存在
            cursor.close()
            conn.close()
            print('您資料未在系統系統中！，若要註冊請按「Enter」則回到上一選單，並選取註冊謝謝')

        elif new_recognition.recognition(memberid) > 70 :
            print('登入失敗！請試著正面對著鏡頭不晃動或脫下口罩再辨識一次')

        elif new_recognition.recognition(memberid) < 20:
            print('登入成功！歡迎 ' + memberid + '！' )
            print('您現在可進入商店購物!!')

            cv2.destroyAllWindows()

            id_num = int(info[0][0])

            savetime = datetime.now()

            msg = {
                "id": id_num,
                "Name": memberid,
                "type": 'login',
                "Time": savetime
            }
            db_created.login(id_num,memberid,savetime)
            new_mongo_connect.login(id_num,memberid,savetime)
            new_kafka_producer.kafka_producer('logs',msg, 'login')

            break
        else:
            cv2.destroyAllWindows()
            print('登入失敗')

if __name__ == '__main__':
    member_login()