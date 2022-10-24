import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

import components.log_writer as log_py
import components.read_config_file as read_config

mysql_host = read_config.ReadConfig().get_one_option("DATABASE", "host")
mysql_database = read_config.ReadConfig().get_one_option("DATABASE", "database")
mysql_user = read_config.ReadConfig().get_one_option("DATABASE", "user")
mysql_password = read_config.ReadConfig().get_one_option("DATABASE", "password")
# mysql_host = 'localhost'
# mysql_database = "abcfinance"
# mysql_user = "root"
# mysql_password = "nimz@12345"
connection = ''


def connect_db():

    global mysql_host, mysql_database, mysql_user, mysql_password, connection

    try:
        connection = mysql.connector.connect(host=mysql_host,
                                 database=mysql_database,
                                 user=mysql_user,
                                 password=mysql_password)

        return connection

    except mysql.connector.Error as error :
        connection.rollback()   # rollback if any exception occured
        log_py.error("Fail to connect database {} with error {}".format(mysql_database, error))


def close_connection(connect):

    cursor = connect.cursor()

    if connection.is_connected():
        connection.close()
        log_py.info("MySQL connection is closed")


def insert_query(iquery, connect):

    sql_insert_query = iquery

    try:
        cursor = connect.cursor()
        result = cursor.execute(sql_insert_query)
        connect.commit()
        cursor.close()
        log_py.info("Record inserted successfully into table")

    except mysql.connector.IntegrityError as e:
        log_py.warn("Trying to enter duplicate entry. {}".format(e))
    except mysql.connector.IdentationError as e:
        log_py.warn("Trying to enter duplicate entry. {}".format(e))
    except mysql.connector.Error as error:
        connect.rollback()  #   rollback if any exception occured
        log_py.error("Failed inserting record. {}".format(error))
        log_py.error("Query executed: {}".format(iquery))


def select_query(iquery, connect):

    sql_select_Query = iquery

    try:
        cursor = connect.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        log_py.info("Salary details selected from {} employees ".format(cursor.rowcount))
        # print("Salary details selected from {} employees ".format(cursor.rowcount))
        cursor.close()
        return records

    except mysql.connector.Error as error:
        connect.rollback()  # rollback if any exception occured
        log_py.error("Failed inserting record. {}".format(error))
        log_py.error("Query executed: {}".format(iquery))
        # print("Fail executing select query. {}".format(error))


# connection = connect_db()
# # create table
# query = "CREATE TABLE EMPLOYEE_SALARY(USER_NAME VARCHAR (255) NOT NULL, EMAIL VARCHAR (255) NOT NULL, " \
#         "FULL_NAME VARCHAR (255) NOT NULL, OT_HOURS INTEGER DEFAULT 0, ONCALL_HOURS INTEGER DEFAULT 0, " \
#         "ALLOWANCE DOUBLE, TOTAL DOUBLE, MONTH INTEGER, PRIMARY KEY (USER_NAME, MONTH)) ENGINE INNODB;"
# insert_query(query, connection)
#
# close_connection(connection)
