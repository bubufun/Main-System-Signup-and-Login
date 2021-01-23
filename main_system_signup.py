import cv2
import db_created
import new_capture
import new_training
import new_login
import new_mongo_connect
import new_kafka_producer


def member_signup():
    while True:
        memberid = input('請輸入您想註冊的帳號 \n(備註:請以數字 + 英文字母大小組合輸入)\n(直接按「Enter」則回到上一選單)\n 輸入欄位：')

        conn = db_created.db_connect_host()
        cursor = conn.cursor()
        sql = 'SELECT * FROM member_signup where memberid = "%s"' % memberid
        cursor.execute(sql)
        info = cursor.fetchall()

        if memberid == '':  # 未輸入帳號就結束
            cursor.close()
            conn.close()
            break

        elif info:  # 帳號已存在
            print('此帳號已被人使用，請換一個id，註冊謝謝！')

        elif not info :  # 獲取人臉資料並建立帳號
            sql2 = 'SELECT MAX(id) FROM member_signup;'
            cursor.execute(sql2)
            id_num_temp = cursor.fetchall()

            id_num = 0
            if id_num_temp[0][0] ==None :
                id_num = 2501
            elif id_num_temp:
                id_num = id_num_temp[0][0] + 1

            new_capture.data_capture(memberid)
            cv2.destroyAllWindows()
            new_training.training_data(memberid)
            model_name= memberid + '.data'

            msg = {
                "id": id_num,
                "Name": memberid,
                "Model": model_name
            }

            db_created.signup(id_num, memberid, model_name)
            new_mongo_connect.signup(id_num, memberid, model_name)
            print('資料傳輸中...')
            new_kafka_producer.kafka_producer('members',msg,'signup')

            cursor.close()
            conn.close()

            break



if __name__ == '__main__':

    while True:
        choose = input('請輸入你想要的選單系統，1:會員註冊,2:會員登入,3:結帳系統:  (q 退出) ')
        if choose == str(1):
            member_signup()
        elif choose == str(2):
            new_login.member_login()
        elif choose == str(3):
            print('結帳系統尚未完成謝謝')
            continue
        elif choose == 'q':
            print('系統已關閉')
            break
        else:
            print('請輸入正確選號，謝謝')

