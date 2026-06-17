# to create database
import mysql.connector
from config import db_config, database_name


def create_n_drop_database(database_name):
    """Create a new database"""
    conn = None
    cur = None
    try:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {database_name};")
        cur.execute(f"CREATE database {database_name} ;")
        conn.commit()
        print(f'database {database_name} created successfully')
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def create_table_customer(database_name):
    """Create CUSTOMER table"""
    conn = None
    cur = None
    try:
        conn = mysql.connector.connection.MySQLConnection(**db_config, database=database_name)
        cur = conn.cursor()
        SQL_Query = """
    CREATE TABLE CUSTOMER(
    `ID`                BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `NAME`              VARCHAR(20) ,
    `REGISTER_DATE`     DATETIME DEFAULT CURRENT_TIMESTAMP,
    `LAST_UPDATE`       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """
        cur.execute(SQL_Query)
        conn.commit()
        print(f'table customer created successfully')
    except mysql.connector.Error as err:
        print(f"Error creating customer table: {err}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def create_table_black_list(database_name):
    """Create BLACK_LIST table"""
    conn = None
    cur = None
    try:
        conn = mysql.connector.connection.MySQLConnection(**db_config, database=database_name)
        cur = conn.cursor()
        SQL_Query = """
    CREATE TABLE BLACK_LIST(
    `CUSTOMER_ID`       BIGINT UNSIGNED NOT NULL,
    `STATUS`            VARCHAR(5),
    `STAGE`             INT,
    `TIME`              INT,
    `DON`               VARCHAR(5),
    `REGISTER_DATE`     DATETIME DEFAULT CURRENT_TIMESTAMP,
    `LAST_UPDATE`       DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMER(ID)
    );
    """
        cur.execute(SQL_Query)
        conn.commit()
        print(f'table black_list created successfully')
    except mysql.connector.Error as err:
        print(f"Error creating black_list table: {err}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    create_n_drop_database(database_name)
    create_table_customer(database_name)
    create_table_black_list(database_name)