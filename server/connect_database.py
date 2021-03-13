import pymysql

class Oprations_of_Database:
    connection = None
    cursor = None
    def __init__(self,username,password,IP,port):
        self.Username = username
        self.Password = password
        self.IP_address = IP
        self.Port = port
        
    def build_connection(self):
        try:
            self.connection = pymysql.connect(
                host = self.IP_address,
                port = self.Port,
                user = self.Username,
                password = self.Password,
                charset = 'utf8'
            ) #创建一个连接
            self.cursor = self.connection.cursor() #创建一个游标，用于操作数据库
            return True
        except  Exception as error_info:
            print(error_info) #打印错误信息
            return False

    def find_all_database(self):
        sql = "show databases;"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result



if __name__ == '__main__':
    op_mysql = Oprations_of_Database("root","123456")
    isLogin = op_mysql.build_connection()
    # res = op_mysql.find_all_database()
    # print(res)
    print(isLogin)
