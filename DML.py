# This file is to add changes to a database

import mysql.connector
from config import db_config, database_name


def add_customer(customer_id, name):
    """Add a new customer to the database"""
    conn = None
    cur = None
    try:
        conn = mysql.connector.connect(**db_config, database=database_name)
        cur = conn.cursor()
        SQL_Query = "INSERT INTO CUSTOMER (ID,NAME) VALUES (%s,%s);"
        cur.execute(SQL_Query, (customer_id, name))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error adding customer: {err}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def add_customer_black_list(customer_id, time, stage=1, don='false'):
    """Add or update a customer in the black list"""
    conn = None
    cur = None
    try:
        conn = mysql.connector.connect(**db_config, database=database_name)
        cur = conn.cursor()
        cur.execute("SELECT * FROM BLACK_LIST WHERE CUSTOMER_ID=%s", (customer_id,))
        user = cur.fetchone()
        if user == None:
            SQL_Query = "INSERT INTO BLACK_LIST (customer_id,STATUS,STAGE,DON,TIME) VALUES (%s,%s,%s,%s,%s);"
            cur.execute(SQL_Query, (customer_id, 'true', stage, don, time))
            conn.commit()
        else:
            SQL_Query = "UPDATE BLACK_LIST SET STATUS=%s,STAGE=%s,DON=%s,TIME=%s WHERE CUSTOMER_ID=%s;"
            cur.execute(SQL_Query, ('true', stage, don, time, customer_id))
            conn.commit()
    except mysql.connector.Error as err:
        print(f"Error adding customer to black list: {err}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def came_customer_black_list(customer_id):
    """Update customer status in black list (mark as came/verified)"""
    conn = None
    cur = None
    try:
        conn = mysql.connector.connect(**db_config, database=database_name)
        cur = conn.cursor()
        SQL_Query = "UPDATE BLACK_LIST SET STATUS=%s,DON=%s WHERE CUSTOMER_ID=%s;"
        cur.execute(SQL_Query, ('false', 'true', customer_id))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error updating customer black list: {err}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()