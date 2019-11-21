from pymysql import connect
from random import randint
import datetime

def add_data():
    # 连接数据库
    client =  connect(host='localhost',port=3306,user='root',passwd='123',charset='utf8',db='flask_tree')
    # 获取游标
    cursor = client.cursor()
    # 编写SQL
    sql = 'insert into t_qd values (0,%s,%s,%s,%s,%s,%s,%s,%s)'
    # 生成参数
    '''
    dc : 3
    cc : 5
    '''
    stage = 1 
    progress = 3
    bug_num = 0
    remarks = '无'
    qd_time= datetime.datetime(2019,10,10)
    code_num =0
    cid =3

    for i in range(100):
        progress += randint(0,8)
        bug_num = randint(0,3)
        qd_time = qd_time + datetime.timedelta(days=1)
        create_time = qd_time.strftime('%Y-%m-%d')
        code_num = randint(100,250)
        args =[5,stage,progress,bug_num,remarks+str(i),create_time,code_num,cid]
        # 执行SQL
        cursor.execute(sql,args)
        # 提交事物
        client.commit()

    # 关闭连接
    try:
        if cursor:
            cursor.close()
        if client:
            client.close()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    add_data()
