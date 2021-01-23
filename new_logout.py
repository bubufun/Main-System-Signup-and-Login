import pymongo
import db_created
from datetime import datetime

def logout_check():

    myclientdata = pymongo.MongoClient(
            "mongodb+srv://url")
    mydbdata = myclientdata['wow']
    mycoldata = mydbdata['logs']
    results = mycoldata.find({}, sort=[('_id', -1)]).limit(1)

    log_check = ()

    for result in results:
        Name = result['Name']
        type = result['type']
        time = result['Time']
        log_check = (Name,type,time)

    if log_check[1] == 'logout':
        conn = db_created.db_connect_host()
        cursor = conn.cursor()
        sql = 'SELECT * FROM login_check where memberid = "%s"' % log_check[0]
        cursor.execute(sql)
        info = cursor.fetchall()
        savetime =datetime.strptime(log_check[2].replace('/','-'), "%Y-%m-%d %H:%M:%S")

        if info:
            cursor.close()
            conn.close()
            db_created.logout(info[0][0],log_check[0],savetime)

            return 1

        elif not info:

            return 0

if __name__ == '__main__':
    a=logout_check()
    print(a)