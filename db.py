import cx_Oracle as oracle
import os
import logging
"""
Module is used for connecting to database
Ensure following environment variables are set 
Also this module assumes you are connecting to Oracle Database 
"""
def get_connection():
    try:
        DB_SERVER = os.environ.get('DB_SERVER')
        DB_PORT = os.environ.get('DB_PORT')
        DB_SID = os.environ.get('DB_SID')
        DB_USERNAME = os.environ.get('DB_USERNAME')
        DB_PASSWORD = os.environ.get('DB_PASSWORD')
        dsn_tns = oracle.makedsn(DB_SERVER, DB_PORT, DB_SID)
        print(dsn_tns)
        connection = oracle.connect(DB_USERNAME, DB_PASSWORD, dsn_tns)
        return connection
    except Exception as ex:
        logging.error(ex)

db_connection = get_connection()

def test_connection(p_conn = db_connection):
    try:
        cur = p_conn.cursor()
        cur.execute('select 1 from dual')
        return 'OK'
    except Exception as ex:
        print(ex)
        return ('FAILED:{}'.format(ex))