# This file is for getting database data

import mysql.connector
from config import db_config, database_name


def get_black_list_list():
    """Get list of all customer IDs in black list"""
    conn = None
    cur = None
    try:
        conn = mysql.connector.connect(**db_config, database=database_name)
        cur = conn.cursor(dictionary=True)
        SQL_QUERY = "SELECT * FROM BLACK_LIST;"
        cur.execute(SQL_QUERY)
        data = cur.fetchall()
        return [row['CUSTOMER_ID'] for row in data]
    except mysql.connector.Error as err:
        print(f"Error getting black list: {err}")
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def get_customer_black(customer_id):
    """Get specific customer's black list data"""
    conn = None
    cur = None
    try:
        conn = mysql.connector.connect(**db_config, database=database_name)
        cur = conn.cursor(dictionary=True)
        SQL_QUERY = "SELECT * FROM BLACK_LIST WHERE CUSTOMER_ID=%s;"
        cur.execute(SQL_QUERY, (customer_id,))
        data = cur.fetchone()
        return data
    except mysql.connector.Error as err:
        print(f"Error getting customer black data: {err}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def check_black_list(customer_id):
    """Check if customer is in black list and active"""
    conn = None
    cur = None
    try:
        conn = mysql.connector.connect(**db_config, database=database_name)
        cur = conn.cursor(dictionary=True)
        SQL_Query = "SELECT STATUS FROM BLACK_LIST WHERE CUSTOMER_ID=%s;"
        cur.execute(SQL_Query, (customer_id,))
        data = cur.fetchone()
        
        if data == None:
            return False
        if data['STATUS'] == 'true':
            return True
        return False
    except mysql.connector.Error as err:
        print(f"Error checking black list: {err}")
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()