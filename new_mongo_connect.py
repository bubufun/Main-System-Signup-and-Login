import pymongo

def mongo_connect_members():
    client = pymongo.MongoClient("mongodb+srv://url")
    mydb = client.wow
    mycol = mydb['members']
    return mycol

def mongo_connect_logs():
    client = pymongo.MongoClient("mongodb+srv://url")
    mydb = client.wow
    mycol = mydb['logs']
    return mycol

def mongo_connect_Transaction():
    client = pymongo.MongoClient("mongodb+srv://url")
    mydb = client.wow
    mycol = mydb['Transaction']
    return mycol

def signup(id_num,memberid, model_name):
    signup_data ={
        "id":id_num,
        "Name":memberid,
        "Model":model_name
    }
    mycol = mongo_connect_members()
    mycol.insert_many([signup_data])

def login(id_num, memberid,savetime):
    login_data = {
        "id":id_num,
        "Name":memberid,
        "type":'login',
        "Time":savetime
    }
    mycol = mongo_connect_logs()
    mycol.insert_many([login_data])

def logout(id_num,memberid,savetime):
    logout_data = {
        "id": id_num,
        "Name": memberid,
        "type":'logout',
        "Time": savetime
    }
    mycol = mongo_connect_logs()
    mycol.insert_many([logout_data])

def Transaction(id,memberid,size,item,price):
    member = {
        "id": id,
        "Name": memberid,
        "size": size,
        "item": item,
        "price": price
    }
    mycol = mongo_connect_Transaction()
    mycol.insert_many([member])

if __name__ == '__main__':
    # Transaction(2501,'test','test','test',1500)
    # myclientdata = pymongo.MongoClient(
    #     "mongodb+srv://peter:0987602620@cluster0.0qqo9.mongodb.net/ceb101?retryWrites=true&w=majority")
    # mydbdata = myclientdata['wow']
    # mycoldata = mydbdata['logs']
    # results = mycoldata.find({}, sort=[('_id', -1)]).limit(1)
    # for result in results:
    #     Name = result['Name']
    #     type = result['type']
    #     print(result)
    from datetime import datetime
    id_num = 2504
    memberid = 'Elsie'
    savetime = datetime.now()
    logout(id_num, memberid, savetime)



