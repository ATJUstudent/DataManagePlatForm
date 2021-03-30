from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask_cors import CORS
from connect_database import Oprations_of_Database    #引入我们的数据库操作类
from dbconn import DBConnector
from dbconn import DBPrinter
from sqlcreator import SqlCreator
import json

#创建数据库操作类实例
op_mysql = Oprations_of_Database("***","***","***","***")
db_config = {
    "ip" : "127.0.0.1",
    "port" : 3306,
    "database" : "test",
    "username" : "root",
    "password" : "123456"
}
app = Flask(__name__)
CORS(app)
# 路由
@app.route('/')    
def first():        # 视图函数
    return 'hello world!!!!!!!!!!!!!!!!!!!!'

@app.route('/login',methods=['POST','OPTIONS'])    
def login():        # 视图函数 从request中接收到的值是bytes 字节码，需要decode('utf8')用utf-8解码
    response = Response()
    if request.method == 'POST':
        containt = request.data.decode('utf8')
        containt = eval(containt)
        IP = containt['IP']
        port = int(containt['port'])
        Username = containt['username']
        Password = containt['password']
        op_mysql.IP_address = IP
        op_mysql.Port = port
        op_mysql.Username = Username
        op_mysql.Password = Password
        isLogin = op_mysql.build_connection()
        if isLogin is True:
            response.data = "登陆成功"
            response.status_code = 200
        else:
            response.data = "登录失败"
            response.status_code = 201
        return response

    else:
        return 'way -> OPTIONS'

@app.route('/main_page/select-database',methods=['GET'])
def get_database_list():
    database_list = op_mysql.find_all_database()
    result = [{'database_name': item[0]} for item in database_list]
    return jsonify(result)

@app.route('/data_home',methods=['GET'])
def get_tables():
    if request.method == 'GET' and request.args.get('name','FLASK') != 'FLASK':
        name_selected = request.args.get('name')
        flag_select_db = op_mysql.select_database(name_selected)
        show_tables = op_mysql.get_all_tables()
        result = [item[0] for item in show_tables]

        return jsonify(result)


@app.route('/data_home/data_query', methods=['GET'])
def get_tables_details():
    if(request.method == 'GET' and request.args.get('db_selected', 'FLASK') != 'FLASK' and request.args.get('table_selected', 'FLASK') != 'FLASK'):
        db_selected = request.args.get('db_selected')
        table_selected = request.args.get('table_selected')
        db_config["database"] = db_selected
        DBConnector.init_config(db_config)
        db_printer = DBPrinter()
        db_printer.print_databases()
        descriptions = json.loads(db_printer.print_columns(db_selected, table_selected))
        data = json.loads(db_printer.print_table(db_selected, table_selected))
        cols = []
        for item in descriptions['Fields']:
            cols.append({"prop" : item, "label" : item})
        tableData = []
        for key in data:
            tableData.append(data[key])
        ret = {}
        ret['cols'] = cols
        ret['tableData'] = tableData
        print(ret)
        
        return jsonify(ret)

@app.route('/data_update',methods=['POST','OPTIONS'])    
def update():        # 视图函数 从request中接收到的值是bytes 字节码，需要decode('utf8')用utf-8解码
    response = Response()
    if request.method == 'POST':
        test = {"0": {"author": "hahahaha", "name": "c language", "update": ["author"]}};
        containt = request.data.decode('utf8')
        containt = eval(containt)
        config = {
            "ip" : "127.0.0.1",
            "port" : 3306,
            "database" : "test",
            "username" : "root",
            "password" : "123456"
        }
        SqlCreator.init_config(config)
        sc = SqlCreator()
        sc.connect_db()
        print(json.dumps(containt['json']))
        print(sc.update_object_sql(json.dumps(test), containt['info']['db'], containt['info']['table']))
        print(sc.commit_all())
        response.data = "成功"
        response.status_code = 200
        return response

    else:
        return 'way -> OPTIONS'

@app.route('/data_delete',methods=['POST','OPTIONS'])    
def delete():        # 视图函数 从request中接收到的值是bytes 字节码，需要decode('utf8')用utf-8解码
    response = Response()
    if request.method == 'POST':
        # test = {"0": {"author": "hahahaha", "name": "c language", "update": ["author"]}};
        containt = request.data.decode('utf8')
        containt = eval(containt)
        config = {
            "ip" : "127.0.0.1",
            "port" : 3306,
            "database" : "test",
            "username" : "root",
            "password" : "123456"
        }
        SqlCreator.init_config(config)
        sc = SqlCreator()
        sc.connect_db()
        print(json.dumps(containt['json']))
        print(sc.delete_object_sql(json.dumps(containt['json']), containt['info']['db'], containt['info']['table']))
        print(sc.commit_all())
        response.data = "成功"
        response.status_code = 200
        return response

    else:
        return 'way -> OPTIONS'

@app.route('/data_add',methods=['POST','OPTIONS'])    
def add():        # 视图函数 从request中接收到的值是bytes 字节码，需要decode('utf8')用utf-8解码
    response = Response()
    if request.method == 'POST':
        # test = {"0": {"author": "hahahaha", "name": "c language", "update": ["author"]}};
        containt = request.data.decode('utf8')
        containt = eval(containt)
        config = {
            "ip" : "127.0.0.1",
            "port" : 3306,
            "database" : "test",
            "username" : "root",
            "password" : "123456"
        }
        SqlCreator.init_config(config)
        sc = SqlCreator()
        sc.connect_db()
        print(json.dumps(containt['json']))
        # print(sc.delete_object_sql(json.dumps(containt['json']), containt['info']['db'], containt['info']['table']))
        # print(sc.commit_all())
        response.data = "成功"
        response.status_code = 200
        return response

    else:
        return 'way -> OPTIONS'


if __name__ == '__main__' :
    app.run(host="127.0.0.1",port= 8080,debug=True)