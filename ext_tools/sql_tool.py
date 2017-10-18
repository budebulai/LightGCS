# -*- coding:utf-8 -*-

import os
import sqlite3
from functools import wraps
import copy

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
    values = copy.deepcopy(params["values"])

    # for i in range(len(values)):
    #     print values[i]
    #     for j in range(len(values[i])):
    #         if isinstance(values[i][j],str):
    #             values[i][j] = '"' + values[i][j] + '"'
        # temp = ",".join(values[i])
        # values[i] = "({})".format(temp)
    if len(fields) == 1:
        if len(values) == 1:
            if isinstance(values[0],str):
                values[0] = '"' + values[0] + '"'
            values = "({})".format(values[0])
        else:
            values = [value for item in values for value in item]
            for i in range(len(values)):
                if isinstance(values[i],str):
                    values[0] = '"' + values[0] + '"'
                values[i] = "({})".format(values[i])
            values = ",".join(values)

    else:
        values = [str(tuple(item)) for item in values]
        values = ",".join(values)

    if fields:
        fields = "(" + ",".join(fields) + ")"

    # print "INSERT INTO {} {} VALUES{};".format(table,fields,values)
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
    # print "DELETE FROM {} {};".format(params["table"],condition)
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
def show_tables():
    return "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"

@connect(motor_db)
def table_query(params):
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

    return "SELECT {} FROM {} {};".format(fields, table, condition)

@connect(motor_db)
def head_query(params):
    """
    params = {"table":tablename}
    查询表字段
    """
    # sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = {};".format(params["table"])
    return "PRAGMA table_info({});".format(params["table"])

"""
视图
示例：创建master_view
CREATE VIEW master_view
AS
SELECT id,name FROM student;

SELECT * FROM master_view;
DESC master_view;
SHOW CREATE VIEW master_view;

ALTER VIEW master_view
AS
SELECT id,name,email FROM student;

UPDATE master_view SET xx=11 WHERE xx=xxx;

DROP VIEW master_view;

"""

"""
事务
将一组语句SQL放在同一批次内去执行，如果一个SQL语句出错，则该批次内的所有SQL都将被取消执行
如银行转帐，中途出现错误，全部回滚
MySQL事务处理只支持InnoDB和BDB数据表类型
ACID：
原子性(atomic)
一致性(consist)
隔离性(isolated)
持久性(durable)

关闭自动提交
SELECT @@autocommit;
SET autocommit=0;

MySQL事务控制
START TRANSACTION;
语句(组)
COMMIT;
ROLLBACK;
SET autocommit=1;

sqlite3事务控制
使用下面的命令来控制事务：
BEGIN TRANSACTION：开始事务处理。
COMMIT：保存更改，或者可以使用 END TRANSACTION 命令。
ROLLBACK：回滚所做的更改。
事务控制命令只与 DML 命令 INSERT、UPDATE 和 DELETE 一起使用。他们不能在创建表或删除表时使用，因为这些操作在数据库中是自动提交的。
"""

"""
触发器
四要素：
1、监视地点table
2、监视事件insert/update/delete
3、触发时间after/before
4、触发事件insert/update/delete

CREATE TRIGGER triggerName
{BEFORE | AFTER}
{INSERT | UPDATE | DELETE}
ON tablename
FOR EACH ROW
BEGIN
    触发器SQL语句;
END;

DROP TRIGGER triggerName;
"""


def create_table_motorList():
    params = {"table":"motorList"}
    params["fields"] = ["Motor varchar(50) PRIMARY KEY NOT NULL"]
    create_table(params)

def drop_table_motorList():
    params = {"table":"motorList"}
    drop_table(params)


def create_table_motorData():
    params = {"table":"motorData"}
    params["fields"] = ["Motor VARCHAR(50)",\
                        "Voltage FLOAT(5,2)",\
                        "Propeller INT(6)",\
                        "Throttle VARCHAR(4)",\
                        "Amps FLOAT(5,2)",\
                        "Watts INT(6)",\
                        "Thrust FLOAT(8,2)",\
                        "RPM INT(5)",\
                        "Efficiency FLOAT(5,2)"]
    create_table(params)

def drop_table_motorData():
    params = {"table":"motorData"}
    drop_table(params)

def create_table_motorInfo():
    params = {"table":"motorInfo"}
    params["fields"] = ["Motor VARCHAR(50) PRIMARY KEY NOT NULL",\
                        "Producer VARCHAR(50)",\
                        "Type VARCHAR(50)",\
                        "KV VARCHAR(10)",\
                        "Voltage FLOAT(5,2)",\
                        "Amps FLOAT(5,2)",\
                        "Watts INT(6)",\
                        "Resistor FLOAT(4,2)",\
                        "AmpNoLoad FLOAT(4,2)"]
    create_table(params)

def drop_table_motorInfo():
    params = {"table":"motorInfo"}
    drop_table(params)

def create_table_propellerInfo():
    params = {"table":"propellerInfo"}
    params["fields"] = ["Producer VARCHAR(50)",\
                        "Propeller INT(6)",\
                        "Type VARCHAR(50)",\
                        "cT FLOAT(6,2)",\
                        "cM FLOAT(6,2)"]
    create_table(params)

def drop_table_propellerInfo():
    params = {"table":"propellerInfo"}
    drop_table(params)
