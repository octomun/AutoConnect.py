import mysql.connector
import pandas as pd

config = {
    'user':'root',
    'password':'@@qazsx852',
    'host':'127.0.0.1',
    'database':'stock',
    'charset':'utf8'
}

def connect_db():
    stock_db = mysql.connector.connect(**config)
    return stock_db
def create_table(db,db_name):
    try:
        cursor = db.cursor( buffered=True)
        sql=f"""
            CREATE TABLE {db_name} (
            dates DATE NOT NULL,
            times CHAR(10) NOT NULL,
            opens FLOAT(20) not null,
            highs FLOAT(20) not null,
            lows  FLOAT(20) not null,
            closes  FLOAT(20) not null,
            vols  FLOAT(20) not null
            );"""
        cursor.execute(sql)
        db.commit()
    finally:
        cursor.close()

def insert_tabel( dates, times, opens, highs, lows, closes, vols, db, db_name):
    try:
        # stock_db.reconnect()
        cursor = db.cursor( buffered=True)
        sql=f"""
            insert into {db_name} (dates, times, opens, highs, lows, closes, vols) values(%s, %s, %s, %s, %s, %s, %s);"""
        cursor.execute(sql,(dates, times, opens, highs, lows, closes, vols))
        db.commit()
    finally:
        cursor.close()

def fetch_all(db,db_name): #전부 출력
    try:
        cursor = db.cursor(raw=True, buffered=True)
        sql = f"""
            select * from {db_name};"""
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()



def drop_table(db,db_name):
    try:
        cursor = db.cursor(raw=True, buffered=True)
        sql = f"""
            drop table {db_name};"""
        cursor.execute(sql)
        db.commit()
    finally:
        cursor.close()



#-------------------------------------------------------------------------------
def create_table_now(db,db_name):
    try:
        cursor = db.cursor(raw=True, buffered=True)
        sql=f"""
            CREATE TABLE {db_name}_now (
            dates DATE NOT NULL,
            times CHAR(10) NOT NULL,
            opens FLOAT(20) not null,
            highs FLOAT(20) not null,
            lows  FLOAT(20) not null,
            closes  FLOAT(20) not null,
            vols  FLOAT(20) not null
            );"""
        cursor.execute(sql)
        db.commit()
    finally:
        cursor.close()

def insert_tabel_now( dates, times, opens, highs, lows, closes, vols, db, db_name):
    try:
        # stock_db.reconnect()
        cursor = db.cursor(raw=True, buffered=True)
        sql=f"""
            insert into {db_name}_now(dates, times, opens, highs, lows, closes, vols) values(%s, %s, %s, %s, %s, %s, %s);"""
        cursor.execute(sql,(dates, times, opens, highs, lows, closes, vols))
        db.commit()
    finally:
        cursor.close()

def fetch_all_now(db,db_name): #전부 출력
    try:
        cursor = db.cursor(raw=True, buffered=True)
        sql = f"""
            select * from {db_name}_now;"""
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()



def drop_table_now(db,db_name):
    try:
        cursor = db.cursor(raw=True, buffered=True)
        sql = f"""
            drop table {db_name}_now;"""
        cursor.execute(sql)
        db.commit()
    finally:
        cursor.close()
#---------------------------------------------------------------
def create_table_stock_code(db):
    try:
        cursor = db.cursor( buffered=True)
        sql=f"""
            CREATE TABLE stock_data_code (
            code char(10) not null,
            now float(20) not null,
            predict FLOAT(20) DEFAULT 0.0,
            pct float(10) DEFAULT 0.0,
            invest_pct float(10) default 0.0
            );"""
        cursor.execute(sql)
        db.commit()
    finally:
        cursor.close()

def insert_table_stock_code(db, code, now):
    try:
        cursor = db.cursor(raw=True, buffered=True)
        sql=f"""
            insert into stock_data_code(code, now) values (%s,%s);"""
        cursor.execute(sql,(code,now))
        db.commit()
    finally:
        cursor.close()




def drop_table_stock_code(db):
    try:
        cursor = db.cursor(raw=True, buffered=True)
        sql = f"""
            drop table stock_data_code;"""
        cursor.execute(sql)
        db.commit()
    finally:
        cursor.close()

def fetch_all_stock_code(db): #전부 출력
    try:
        cursor = db.cursor(dictionary=True, buffered=True)
        sql = f"""
            select * from stock_data_code;"""
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()

def fetch_stock_code_where_code(db,code): #조건 출력
    try:
        cursor = db.cursor(dictionary=True, buffered=True)
        sql = f"""
            select `predict` from `stock`.`stock_data_code` where `code` = '%s';"""
        cursor.execute(sql,code)
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()

def update_stock_code(db,code,data):
    try:
        cursor = db.cursor(raw=True, buffered=True)
        sql=f"""
            UPDATE `stock`.`stock_data_code` SET `invest_pct` = %s WHERE (`code` = %s)"""
        cursor.execute(sql,(data,code))
        db.commit()
    finally:
        cursor.close()
# def stock_code_init():
#     conn = connect_db()
#     try:
#         drop_table_stock_code(conn)
#         create_table_stock_code(conn)
#     except:
#         create_table_stock_code(conn)