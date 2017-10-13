# -*- coding:utf-8 -*-

import os
import sqlite3
from functools import wraps

motor_db = os.path.split(os.path.realpath(__file__))[0] + "\\rotor_db\\motors.db"

def connect(db):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            try:
                sql = func(*args, **kwargs)
                cur.execute(sql)
                conn.commit()
                ret = cur.fetchall()
            except Exception as e:
                print str(e)
                return None
            finally:
                cur.close()
                conn.close()

            return ret
        return wrapper
    return decorator

@connect(motor_db)
def drop_table(params):
    """
    params = {"table":tablename}
    """
    return "DROP TABLE {};".format(params["table"])

@connect(motor_db)
def create_table(params):
    """
    params = {"table":tablename, "fields":["ID int","name text",...]}
    """
    table = params["table"]
    fields = params["fields"]
    sql = "CREATE TABLE IF NOT EXISTS {}(".format(table)

    for i in range(len(fields)):
        sql += "{},".format(fields[i])
    else:
        sql = sql.rstrip(",") + ");"
    return sql

@connect(motor_db)
def insert_items(params):
    """
    params = {"table":tablename, "fields":["ID","name",...], "values":[[],[],...]}
    """
    table = params["table"]
    fields = params["fields"]
    values = params["values"]
    sql = "INSERT INTO {} (".format(table)

    for field in fields:
        sql += "{},".format(field)
    else:
        sql = sql.rstrip(",") + ") VALUES"

    for value in values:
        sql += "("
        for item in value:
            if isinstance(item,str):
                sql += '"{}",'.format(str(item))
            else:
                sql += "{},".format(item)
        else:
            sql = sql.rstrip(",") + "),"
    else:
        sql = sql.rstrip(",") + ";"
    return sql

@connect(motor_db)
def db_query(params):
    """
    params = {"table":tablename, "fields":["ID","name",...], "conditions":xxx}
    """
    table = params["table"]
    fields = params["fields"]
    conditions = params.get("conditions",None)

    sql = "SELECT "
    if fields:
        for field in fields:
            sql += "{},".format(field)
        else:
            sql = sql.rstrip(",") + " FROM {}".format(table)
    else:
        sql += "* FROM {}".format(table)

    return sql


@connect(motor_db)
def table_head_query(params):
    """
    params = {"table":tablename}
    """
    # sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = {};".format(params["table"])
    sql = "PRAGMA table_info({});".format(params["table"])
    return sql
