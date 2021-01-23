import cv2
import db_created
import new_capture
import new_training
import new_recognition
import new_mongo_connect
import new_kafka_producer
import tkinter as tk
import tkinter.messagebox
from datetime import datetime
import new_logout


def main():
    def confirm_to_quit():
        if tk.messagebox.askokcancel('溫馨提示', '确定要退出嗎'):
            window.quit()

    # def not_work():
    #     respond = ''
    #     tmp_respond.configure(text=respond)

    def member_signup():

        def quit_from_frame():
            signup_frame.destroy()

        def signup_check():

            memberid = str(memberid_entry.get())
            conn = db_created.db_connect_host()
            cursor = conn.cursor()
            sql = 'SELECT * FROM member_signup where memberid = "%s"' % memberid
            cursor.execute(sql)
            info = cursor.fetchall()

            if memberid == '':  # 未輸入帳號就結束
                cursor.close()
                conn.close()
                signup_respond = '請輸入帳號'
                signup_respond_label.configure(text=signup_respond)
                new_logout.logout_check()

            elif info:  # 帳號已存在
                cursor.close()
                conn.close()
                signup_respond = '此帳號已被人使用，請換一個id，註冊謝謝！'
                signup_respond_label.configure(text=signup_respond)
                new_logout.logout_check()

            elif not info:  # 獲取人臉資料並建立帳號

                sql2 = 'SELECT MAX(id) FROM member_signup;'
                cursor.execute(sql2)
                id_num_temp = cursor.fetchall()

                id_num = 0
                if id_num_temp[0][0] == None:
                    id_num = 2501
                elif id_num_temp:
                    id_num = id_num_temp[0][0] + 1

                new_capture.data_capture(memberid)
                cv2.destroyAllWindows()
                new_training.training_data(memberid)
                model_name = memberid + '.data'

                msg = {
                    "id": id_num,
                    "Name": memberid,
                    "Model": model_name
                }

                db_created.signup(id_num, memberid, model_name)
                new_mongo_connect.signup(id_num, memberid, model_name)
                new_kafka_producer.kafka_producer('members', msg, 'signup')

                signup_respond = '註冊成功!！'
                signup_respond_label.configure(text=signup_respond)

                end_respond = '已可退出此頁面！'
                end_respond_label.configure(text=end_respond)

                cursor.close()
                conn.close()
                new_logout.logout_check()

        #signup frame
        signup_frame = tk.Toplevel(window)
        signup_frame.geometry('400x300')

        signup_frame.iconbitmap('./wurenicon.ico')

        label_title_signup = tk.Label(signup_frame, text='請輸入您想註冊的帳號 \n(備註:請以數字 + 英文字母大小組合輸入)')
        label_title_signup.pack()

        memberid_entry = tk.Entry(signup_frame)
        memberid_entry.pack()

        signup_respond_label = tk.Label(signup_frame)
        signup_respond_label.pack()

        end_respond_label =tk.Label(signup_frame)
        end_respond_label.pack()

        signup_btn =tk.Button(signup_frame,text='註冊',command=signup_check)
        signup_btn.pack()
        signup_btn.place()

        quit_button = tk.Button(signup_frame, text='退出',command=quit_from_frame)
        quit_button.pack(side = 'bottom')

    def member_login():

        def quit_from_frame():
            login_frame.destroy()

        def login_check():

            memberid = str(memberid_entry.get())

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
                login_respond = '請輸入帳號'
                respond_label.configure(text=login_respond)
                new_logout.logout_check()

            elif login_check:  # 帳號已存在
                cursor.close()
                conn.close()
                login_respond = '已重複登入系統！ \n 若要結帳請先退出，回到上一選單並選取結帳謝謝'
                respond_label.configure(text=login_respond)
                new_logout.logout_check()

            elif not info:  # 帳號不存在
                cursor.close()
                conn.close()
                login_respond ='您資料未在系統系統中！\n 若要註冊請先退出，回到上一選單，並選取註冊謝謝'
                respond_label.configure(text=login_respond)
                new_logout.logout_check()

            elif new_recognition.recognition(memberid) > 70:
                login_respond = '登入失敗！請試著正面對著鏡頭不晃動或脫下口罩再辨識一次'
                respond_label.configure(text=login_respond)
                new_logout.logout_check()

            elif new_recognition.recognition(memberid) < 30:
                login_respond = '登入成功！歡迎 ' + memberid + '！'+'\n歡迎光臨，您現在可進入商店購物!! '
                respond_label.configure(text=login_respond)

                cv2.destroyAllWindows()

                id_num = int(info[0][0])

                savetime = datetime.now()

                msg = {
                    "id": id_num,
                    "Name": memberid,
                    "type": 'login',
                    "Time": savetime
                }
                db_created.login(id_num, memberid, savetime)
                new_mongo_connect.login(id_num, memberid, savetime)
                new_kafka_producer.kafka_producer('logs',msg, 'login')
                new_logout.logout_check()


            else:
                cv2.destroyAllWindows()
                login_respond ='登入失敗'
                respond_label.configure(text=login_respond)
                new_logout.logout_check()

        # login frame
        login_frame = tk.Toplevel(window)
        login_frame.geometry('400x300')
        login_frame.iconbitmap('./wurenicon.ico')
        label_title_login = tk.Label(login_frame, text='進入商店前，請輸入您帳號')
        label_title_login.pack()

        memberid_entry = tk.Entry(login_frame)
        memberid_entry.pack()

        respond_label = tk.Label(login_frame)
        respond_label.pack()

        login_btn =tk.Button(login_frame,text='人臉辨識登入',command=login_check)
        login_btn.pack()
        login_btn.place()

        quit_button = tk.Button(login_frame, text='退出', command=quit_from_frame)
        quit_button.pack(side='bottom')

    #window frame setting

    window = tk.Tk()
    window.geometry('400x300')
    window.title('吾人商店系統')
    # window.tk.call('wm', 'iconphoto', window._w, tk.PhotoImage(file='./wurenicon.ico'))
    window.iconbitmap('./wurenicon.ico')

    #signup

    label_signup = tk.Button(window,text='會員註冊', font = 'Arial -16', fg = 'red',command=member_signup)
    label_signup.pack(expand=1)

    #login

    label_login = tk.Button(window,text='會員登入', font = 'Arial -16', fg = 'blue',command=member_login)
    label_login.pack(expand=1)

    #checkout

    # label_checkout = tk.Button(window,text='會員結帳', font = 'Arial -16', fg = 'green',command=not_work)
    # label_checkout.pack(expand=1)

    # tmp_respond = tk.Label(window)
    # tmp_respond.pack()

    #quit windows
    quit_frame = tk.Frame(window)

    quit_button = tk.Button(window,text = '退出', command = confirm_to_quit)
    quit_button.pack()

    quit_frame.pack(side = 'bottom')

    window.mainloop()

if __name__ == '__main__':
    main()

