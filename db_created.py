import pymysql
from datetime import datetime

def db_connect_host():
    try:
        host = '10.1.0.188'
        port = 3306
        user = 'root'
        passwd = 'DA02008'
        charset = 'utf8mb4'
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, charset=charset)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS member_Info;")
        db='member_Info'
        return pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    except:
        print('Unable to connect to the database. Please check DP host IP setting or DB network')

def tb_create():
    conn = db_connect_host()
    cursor = conn.cursor()

    sql = """CREATE TABLE IF NOT EXISTS member_signup(id int, memberid TEXT, model TEXT, CONSTRAINT member_signup_PK PRIMARY KEY (id))ENGINE = INNODB;"""
    sql2 = """CREATE TABLE IF NOT EXISTS log(id int, memberid TEXT, ltime DATETIME, type VARCHAR(6))ENGINE = INNODB;"""
    sql3 = """CREATE TABLE IF NOT EXISTS login_check(id int, memberid TEXT, ltime DATETIME)ENGINE = INNODB;"""
    sql4 = """CREATE TABLE IF NOT EXISTS transation(id int, memberid TEXT,size int ,item VARCHAR(45), price int, ltime DATETIME)ENGINE = INNODB;"""

    cursor.execute(sql)
    cursor.execute(sql2)
    cursor.execute(sql3)
    cursor.execute(sql4)

    cursor.close()
    conn.close()

    return print('Table Successfully Created')

def signup(id_num,memberid, model_name):
    conn = db_connect_host()
    cursor = conn.cursor()
    sql = 'INSERT INTO member_signup VALUES({},"{}","{}")'.format(id_num, memberid, model_name)  # 將帳號及model name寫入資料表
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

    print('帳號建立成功！')

def login(id_num, memberid,savetime):
    conn = db_connect_host()
    cursor = conn.cursor()
    sql ="""INSERT INTO log VALUES({},"{}","{}",'login')""".format(id_num, memberid, savetime)
    sql2 ="""INSERT INTO login_check VALUES({},"{}","{}")""".format(id_num, memberid, savetime)
    cursor.execute(sql)
    cursor.execute(sql2)
    conn.commit()
    cursor.close()
    conn.close()
    print('歡迎光臨!! 您已登入吾人商店系統中')


def logout(id_num,memberid,savetime):
    conn = db_connect_host()
    cursor = conn.cursor()
    sql = """INSERT INTO log VALUES({},"{}","{}",'logout')""".format(id_num,memberid, savetime)
    sql2 = """DELETE FROM login_check WHERE id = '{}';""".format(id_num)
    cursor.execute(sql)
    cursor.execute(sql2)
    conn.commit()
    cursor.close()
    conn.close()
    print('已登出吾人商店，感謝您的購物!!歡迎下次再來!! ')

def Transaction(id_num,memberid,size,item,price,savetime):
    pass

if __name__ == '__main__':
    # tb_create()
    import new_mongo_connect
    id_num = 2504
    memberid = 'Elsie'
    savetime = datetime.now()
    logout(id_num, memberid, savetime)
    new_mongo_connect.logout(id_num, memberid, savetime)


