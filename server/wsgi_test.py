from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask_cors import CORS
import pymysql
from dbconn import DBPrinter
from sqlcreator import SqlCreator
import json
import base64
import xlrd
from flask import Blueprint
from openpyxl import load_workbook
from importdatafile import FileImportTool


app = Flask(__name__)
CORS(app)
db_config = {
    "ip" : "",
    "port" : 99999,
    "database" : "mysql",
    "username" : "",
    "password" : ""
}
FileImportTool.init_config(db_config)
sc = FileImportTool()

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
        db_config['ip'] = containt['IP']
        db_config['port'] = int(containt['port'])
        db_config['username'] = containt['username']
        db_config['password'] = containt['password']
        sc.ip = containt['IP']
        sc.port = int(containt['port'])
        sc.username = containt['username']
        sc.password = containt['password']
        try:
            sc.connect_db()
            response.data = "登陆成功"
            response.status_code = 200
        except Exception as error_info:
            print(error_info)
            response.data = "登录失败"
            response.status_code = 201
        
        return response

    else:
        return 'way -> OPTIONS'

# 需要统一
@app.route('/main_page/select-database',methods=['GET'])
def get_database_list():
    database_list = json.loads(sc.print_databases())
    result = [{'database_name': item} for item in database_list['Database']]
    return jsonify(result)

# 需要统一
@app.route('/data_home',methods=['GET'])
def get_tables():
    if request.method == 'GET' and request.args.get('name','FLASK') != 'FLASK':
        name_selected = request.args.get('name')
        table_list = json.loads(sc.print_tables(name_selected))
        if not table_list:
            result = []
        else:
            result = [item for item in table_list['Tables_in_%s' % name_selected]]

        return jsonify(result)

@app.route('/data_home/data_query', methods=['GET'])
def get_tables_details():
    if(request.method == 'GET' and request.args.get('db_selected', 'FLASK') != 'FLASK' and request.args.get('table_selected', 'FLASK') != 'FLASK'):
        db_selected = request.args.get('db_selected')
        table_selected = request.args.get('table_selected')
        descriptions = json.loads(sc.print_columns(db_selected, table_selected))
        data = json.loads(sc.print_table(db_selected, table_selected))
        cols = []
        for item in descriptions['Fields']:
            cols.append({"prop" : item, "label" : item})
        tableData = []
        for key in data:
            tableData.append(data[key])
        fields = []
        for item in descriptions['Fields']:
            fields.append({item : item})
        ret = {}
        ret['cols'] = cols
        ret['tableData'] = tableData
        ret['fields'] = fields
        print(ret)
        
        return jsonify(ret)

@app.route('/data_update',methods=['POST','OPTIONS'])    
def update():        # 视图函数 从request中接收到的值是bytes 字节码，需要decode('utf8')用utf-8解码
    response = Response()
    if request.method == 'POST':
        containt = request.data.decode('utf8')
        containt = eval(containt)
        print(json.dumps(containt['json']))
        print(sc.update_object_sql(json.dumps(containt['json']), containt['info']['db'], containt['info']['table']))
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
        print(json.dumps(containt['json']))
        print(sc.create_object_sql(json.dumps(containt['json']), containt['info']['db'], containt['info']['table']))
        print(sc.commit_all())
        response.data = "成功"
        response.status_code = 200
        return response

    else:
        return 'way -> OPTIONS'

@app.route('/create_table_sql',methods=['POST','OPTIONS'])   
def create_table_sql():
    response = Response()
    if request.method == 'POST':
        containt = request.data.decode('utf8')
        containt = eval(containt)
        database_name = containt['db']
        table_name = containt['tb']
        attr_list = containt['attr']
        json_template = {}
        json_attr_template = {}
        num = 0
        for attr in attr_list:
            json_attr_template['%d' % num] = attr
            num = num + 1
        json_template[table_name] = json_attr_template
        json_template = json.dumps(json_template)
        sql = sc.create_table_sql(json_template, database_name)
        print(sql)
        return sc.commit_all()
    else:
        return 'way -> OPTIONS'

@app.route('/delete_table_sql',methods=['POST','OPTIONS'])   
def delete_table_sql():
    response = Response()
    if request.method == 'POST':
        containt = request.data.decode('utf8')
        containt = eval(containt)
        print(containt)
        tb = {"table" : {"0" : containt["tb"]}}
        db = containt["db"]
        print(tb)
        sql = sc.delete_table_sql(json.dumps(tb), db)
        code = sc.commit_all()
        return code
    else:
        return 'way -> OPTIONS'
    
@app.route('/create_database_sql',methods=['POST','OPTIONS'])   
def create_database_sql():
    response = Response()
    if request.method == 'POST':
        containt = request.data.decode('utf8')
        containt = eval(containt)
        if containt['tb'] == '':
            tb = {'database': containt['db']}
        else:
            tb = {'database' : containt['db'], 'charset' : containt['tb']}
        print(tb)
        sql = sc.create_database_sql(json.dumps(tb))
        return sc.commit_all()
    else:
        return 'way -> OPTIONS'
        
@app.route('/delete_database_sql',methods=['POST','OPTIONS'])   
def delete_database_sql():
    response = Response()
    if request.method == 'POST':
        containt = request.data.decode('utf8')
        containt = eval(containt)
        print(containt)
        tb = {"database" : [containt["db"]]}
        print(tb)
        sql = sc.delete_database_sql(json.dumps(tb))
        return sc.commit_all()
    else:
        return 'way -> OPTIONS'

@app.route('/upload_xlsx',methods=['POST','OPTIONS']) 
def upload_xlsx():
    response = Response()
    if request.method == 'POST':
        containt = request.data.decode('utf8')
        
        print(containt)
    #     file_data = request.files.get('file_data')
    #     	# 这是将文件转为流，在xlrd中打开
    # f = file_data.read()
    # clinic_file = xlrd.open_workbook(file_contents=f)
    # # sheet1
    # table = clinic_file.sheet_by_index(0)
    # # 输出每一行的内容
    # # table.nrows获取该sheet中的有效行数
    # for row_num in range(0, table.nrows):
    #     print(table.row_values(row_num))
        return 'Hello'
    else:
        return 'way -> OPTIONS'

@app.route('/input_table_data',methods=['POST'])
def input_data():
    response = Response()
    if(request.method == 'POST'):
        containt = request.data.decode('utf8')
        containt = eval(containt)
        database_name = containt['db']
        table_name    = containt['tb']
        data_form = containt['data_form']
        # print(data_form)
        data_new_form = []
        name_list = [key for key in data_form[0]]
        data_new_form.append(name_list)
        # print(name_list)
        for item in data_form:
            obj = [value for value in item.values()]
            data_new_form.append(obj)
        # print(data_new_form)
        try:
            sc.insert_value_row(data_new_form, database_name, table_name)
            return '添加数据成功'
        except Exception as error_info:
            print(error_info)
            response.status_code = 201


        
        

if __name__ == '__main__' :
    app.run(host="127.0.0.1",port= 8080,debug=True)
