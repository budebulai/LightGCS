# -*- coding:utf-8 -*-

import os
import sqlite3
from functools import wraps

"""
待优化：
1、字符串拼接时保留引号
    劣法：参数填充时字符串值使用单双引号两层包裹
    最优：
        values = [str(tuple(item)) for item in values]
        values = ",".join(values)

    较优：对需要保留引号的字符串检出并更改为"'xxx'"形式，怎么实现呢？
        def str_convert(s):
            return "'" + s + "'"

        # for i in range(len(values)):
        #     for j in range(len(values[i])):
        #         if isinstance(values[i][j],str):
        #             values[i][j] = '"' + values[i][j] + '"'

    次优：替换法，在字符串值的前后增加特殊字符，待拼接完成后再替换为引号
2、
"""

"""
SQL:结构化查询语言
1、DDL语言（数据定义语言）
用来定义数据库、数据表、视图、索引、触发器
create   alter   drop
2、DML语言（数据操纵语言）
用于插入、更新、删除数据
insert   update  delete  truncate
3、DQL语言（数据查询语言）
查询数据库中的数据
select
4、DCL语言（数据控制语言）
用来控制用户的访问权限
grant   revoke

MySQL数据类型：
数值：TINYINT SMALLINT MEDIUMINT INT BIGINT FLOAT DOUBLE DECIMAL
字符串: CHAR VARCHAR TINYTEXT TEXT
日期、时间: DATE TIME DATETIME TIMESTAMP YEAR
NULL

注：
int(4)，显示长度4位，zerofill填充0，99 --> 0099。 int(4) zerofill
float(5,2)，总长度为5，小数2位

sqlite数据类型


ALTER TABLE XXX AUTO_INCREMENT=10;

"""

# 电机数据库文件
motor_db = os.path.split(os.path.realpath(__file__))[0] + "\\rotor_db\\motors.db"

def connect(db):
    """
    sqlite3装饰器
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            try:
                # 获取SQL语句
                sql = func(*args, **kwargs)
                # 执行语句
                cur.execute(sql)
                # 未设置自动提交，此时手动提交。
                conn.commit()
                # 获取查询结果集
                ret = cur.fetchall()
            except Exception as e:
                # 封装调试用
                print str(e)
                return None
            finally:
                # 关闭指针、连接
                cur.close()
                conn.close()
            # 返回查询内容，SELECT时有意义
            return ret
        return wrapper
    return decorator

"""
DDL
"""
@connect(motor_db)
def drop_db(params):
    """
    params = {"database":database}
    """
    return "DROP DATABASE IF EXISTS {};".format(params["database"])

@connect(motor_db)
def drop_table(params):
    """
    params = {"table":tablename}
    """
    return "DROP TABLE IF EXISTS {};".format(params["table"])

@connect(motor_db)
def create_table(params):
    """
    params = {"table":tablename, "fields":["ID int AUTO_INCREMENT PRIMARY KEY NOT NULL COMMENT XXX","name text DEFAULT XXX",...]}
    """
    table = params["table"]
    fields = ",".join(params["fields"])

    return "CREATE TABLE IF NOT EXISTS {}({});".format(table,fields)

@connect(motor_db)
def alter_table(params):
    """
    params = {"table":tablename,
              "action":["CHANGE", "MODIFY", "RENAME AS", "ADD", "DROP"], #列表之一，字符串
              "fields":["AUTO_INCREMENT=10", "new tablename"]}  #列表之一，字符串
    调节序号：auto_increment=10
    修改表名：rename as 新表名
    添加字段：add 字段名 列类型
    修改字段：modify 字段名 列类型
             change 旧字段名 新字段名 列类型
    删除字段：drop 字段名
    """
    table = params["table"]
    action = params.get("action","")
    fields = params["fields"]
    return "ALTER TABLE {} {} {};".format(table,action,fields)

"""
DML
"""
@connect(motor_db)
def insert_items(params):
    """
    params = {"table":tablename, "fields":["ID","name",...], "values":[[],[],...]}
    不带字段名：  insert into tablename values (...),(...),... 全字段填充
    插入多行数据：insert into tablename (xx, xx, ...) values(xx,xx,...),(xx,xx,...)
    """
    table = params["table"]
    fields = params.get("fields","")
    values = params["values"]

    if fields:
        fields = "(" + ",".join(fields) + ")"

    values = [str(tuple(item)) for item in values]
    values = ",".join(values)

    return "INSERT INTO {} {} VALUES{};".format(table,fields,values)

@connect(motor_db)
def update_table(params):
    """
    params = {"table":tablename,"fields":{"col1":value,"col2":value,...}, "condition": "where ..."}
    update tablename set column1_name = value [, column2_name=value,...] [where condition];
    修改表数据
    """
    table = params["table"]
    fields = params["fields"]
    condition = params.get("condition","")

    temp = []
    for key,value in fields.items():
        if isinstance(value,str):
            value = '"' + value + '"'
        temp.append("{}={}".format(key,value))
    values = ",".join(temp)

    if condition:
        condition = "WHERE " + condition

    return "UPDATE {} SET {} {};".format(table,values,condition)

@connect(motor_db)
def delete_items(params):
    """
    params = {"table":tablename,"condition":xxx}
    delete from tablename where condition;
    """
    condition = params.get("condition","")
    if condition:
        condition = "WHERE " + condition

    return "DELETE FROM {} {};".format(params["table"],condition)

@connect(motor_db)
def truncate_table(params):
    """
    params = {"table":tablename}
    truncate [table] tablename;
    用于完全清空表数据，但表结构、索引、约束等不变。
    区别于DELETE命令：
        同：都删除数据，不删除表结构，但TRUNCATE更快
        不同：1、使用TRUNCATE重新设置AUTO_INCREMENT计数器
             2、使用TRUNCATE不会对事务有影响
    """
    return "TRUNCATE {};".format(params["table"])


"""
DQL
"""
@connect(motor_db)
def db_query(params):
    """
    params = {"table":tablename, "fields":["ID","name",...], "conditions":xxx}
    """
    table = params["table"]
    fields = params.get("fields","")
    condition = params.get("condition","")

    if not fields:
        fields = "*"

    fields = ",".join(fields)

    if condition:
        condition = "WHERE " + condition

    return "SELECT {} FROM {} {};".format(table, fields, condition)

@connect(motor_db)
def head_query(params):
    """
    params = {"table":tablename}
    查询表字段
    """
    # sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = {};".format(params["table"])
    return "PRAGMA table_info({});".format(params["table"])
