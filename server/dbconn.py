"""
Interface for basic reading database request
"""
#    Author: Wang Chuhan(wchwzhsgdx@gmail.com)
#    Time: 2021.03.14
#    for Data Manage Platform(TJU CS2018-3)
import pymysql
import logging
import json
logger = logging.getLogger()


class DBConnector:
    """ Create a basic connection to MySQL database

    Connect to database
    The interface of running SQL script is provided
    Returns cursor of connection

    Attributions:
    _config: a dictionary stores ip, port, username, password and current database
    _conn: connection to database which is a python object

    """
    _config = None
    _conn = None

    @classmethod
    def init_config(cls, config):
        """ set elements of DBConnector._config as a class method

        please call this function before instantiate a DBConnector object

        Parameters
        ----------
        config: dict
            dict should have correct key/value pairs for "ip": String, "port": Number,
            "database": String, "username": String, "password": String

        Examples
        --------
        >>> dictionary = {"ip": 127.0.0.1, "port": 3306, "database": "test", "username": "root", "password": "123"}
        >>> DBConnector.init_config(dictionary)

        Notes
        -----
        Please call this function before instantiate a DBConnector object

        """
        cls._config = config

    def __init__(self):
        """ initialization function

        Save the basic value of the database connection

        """
        if not self._config:
            raise ReferenceError('DBConn._config should be initialized first!')
        self.ip = self._config['ip']
        self.port = self._config['port']
        self.database = self._config['database']
        self.username = self._config['username']
        self.password = self._config['password']

    def connect_db(self):
        """ establish a connection to the database

        establish a connection to the database and returns a cursor of sql: "SHOW DATABASES"

        Returns
        -------
        cursor: pymysql.cursor.DictCursor
            a cursor object of sql "SHOW DATABASES"

        Examples
        --------
        >>> db = DBConnector()
        >>> cur = db.connect_db()
        >>> cur.fetchall()
        >>> ...

        """
        if self._conn is None:
            self._conn = pymysql.connect(
                host=self.ip,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password
            )
        sql = 'SHOW DATABASES;'
        return self.execute_sql(sql)

    def tables_db(self, database_name):
        """ change current database

        change current database and return a cursor of sql: "SHOW TABLES"

        Parameters
        ----------
        database_name: String
            name of an existed database

        Returns
        -------
        cursor: pymysql.cursor.DictCursor
            a cursor of sql: "SHOW TABLES"

        """
        if self._conn is None:
            raise ReferenceError('Database has not been connected!')
        if self.database != database_name:
            sql = 'use %s' % database_name
            self.database = database_name
            self.execute_sql(sql)
        sql = 'SHOW TABLES;'
        return self.execute_sql(sql)

    def table_columns(self, database_name, table_name):
        """ read the attribute details of a table in the database

        Parameters
        ----------
        database_name: String
            name of an existed database
        table_name: String
            name of an existed table of above database

        Returns
        -------
        cursor: pymysql.cursor.DictCursor
            a cursor of sql: "DESC 'database_name'.'table_name'"

        """
        if self._conn is None:
            raise ReferenceError('Database has not been connected!')
        sql = 'DESC %s.%s' % (database_name, table_name)
        return self.execute_sql(sql)

    def table_rows(self, database_name, table_name):
        """ read the all records of a table in the database

        Parameters
        ----------
        database_name: String
            name of an existed database
        table_name: String
            name of an existed table of above database

        Returns
        -------
        cursor: pymysql.cursor.DictCursor
            a cursor of sql: "SELECT * FROM 'database_name'.'table_name'"

        """
        if self._conn is None:
            raise ReferenceError('Database has not been connected!')
        sql = 'SELECT * FROM %s.%s' % (database_name, table_name)
        return self.execute_sql(sql)

    def execute_sql(self, sql):
        """ execute an input sql

        Parameters
        ----------
        sql: String
            a correct sql script

        Returns
        -------
        cursor: pymysql.cursor.DictCursor
            a cursor of input sql

        Examples
        --------
        >>> db = DBConnector()
        >>> sql = 'DROP DATABASE test'
        >>> db.execute_sql(sql)

        """
        if self._conn is None:
            raise ReferenceError('Database has not been connected!')
        logger.debug('ExecuteSQL: %s' % sql)
        cur = self._conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql)
        return cur

    def commit_sql(self, sql):
        """ commit sql in an affair

        Parameters
        ----------
        sql: String
            a correct sql script

        """
        self.execute_sql(sql)
        self._conn.commit()


class DBPrinter(DBConnector):
    """ print data of database by json, subclass of DBConnector

    Interface for reading database names
    Interface for reading table names of an existed database
    Interface for reading records in an existed table

    """
    def print_databases(self):
        """ Interface for reading database names

        Returns
        -------
        json.dumps(): String
            a string of json

        Notes
        -----
        json: {"Database": ["information_schema", "mysql", "performance_schema", "test"]}

        """
        databases = []
        database_list = self.connect_db().fetchall()
        for database in database_list:
            databases.append(database['Database'])
        database_list = {'Database': databases}
        return json.dumps(database_list)

    def print_tables(self, database_name):
        """ Interface for reading table names of an existed database

        Parameters
        ----------
        database_name: String
            name of an existed database

        Returns
        -------
        json.dumps(): String
            a string of json

        Notes
        -----
        json: {"Tables_in_'database_name'": ["table1", "table2"]}

        """
        table_list = self.tables_db(database_name).fetchall()
        if not table_list:
            table_list = {}
        else:
            tables = []
            key = 'Tables_in_' + database_name
            for table in table_list:
                tables.append(table[key])
            table_list = {key: tables}
        return json.dumps(table_list)

    def print_table(self, database_name, table_name):
        """ Interface for reading records in an existed table

        Parameters
        ----------
        database_name: String
            name of an existed database
        table_name: String
            name of an existed table of above database

        Returns
        -------
        json.dumps(): String
            a string of json

        Notes
        -----
        json: {"0": {"id": 1, "name": "Jason", "password": 123456}, "1": {"id": 2, "name": "Asuka", "password": 1234},
                "2": {"id": 3, "name": "Wang", "password": 123456}}

        """
        objects = self.table_rows(database_name, table_name).fetchall()
        if objects is None:
            object_list = {}
        else:
            list1 = []
            for i in range(len(objects)):
                list1.append(i)
            object_list = dict(zip(list1, objects))
        return json.dumps(object_list)


# # 测试用代码，取消注释使用
# if __name__ == '__main__':
#     text = open('DBData.json')
#     json_dict = json.load(text)
#     DBConnector.init_config(json_dict)
#     db = DBPrinter()
#     print(db.print_databases())
#     print(db.print_tables('mysql'))
#     print(db.print_tables('test'))
#     print(db.print_table('test', 'table2'))
#     print(db.print_table('mysql', 'db'))
