import pymysql
import datetime
from collections import namedtuple

HOST = '192.168.0.41'
PORT = 3306
USER = 'kgm'
PASSWORD = '123123'
DATABASE = 'o2'
TABLENAME   = 'rwrist_test'

Point = namedtuple('Point', 'x y')

def SQL_EXECUTE(query_string, tablename = TABLENAME) : 
    try :
        conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE)
        if conn.open :
            with conn.cursor() as curs:             
                curs.execute(query_string)
                rows = curs.fetchall()
            conn.commit()
        else :
            assert (not conn.open)
    finally :
        conn.close()
    return rows

def SQL_SELECT(tablename = TABLENAME) :
    query_string = ("select RWRIST_X from %s" %tablename)
    RWRIST_X = SQL_EXECUTE(query_string, tablename)
    query_string = ("select RWRIST_Y from %s" %tablename)
    RWRIST_Y = SQL_EXECUTE(query_string, tablename)
    query_string = ("select RWRIST_Z from %s" %tablename)
    RWRIST_Z = SQL_EXECUTE(query_string, tablename)
    return RWRIST_X, RWRIST_Y, RWRIST_Z

def SQL_CREATETABLE(tablename = TABLENAME) :
        # distance values call (humans list length = people).
        # NOSE = 0
        # NECK = 1
        # RSHOULDER = 2
        # RELBOW = 3
        # RWRIST = 4
        # LSHOULDER = 5
        # LELBOW = 6
        # LWRIST = 7
        # RHIP = 8
        # RKNEE = 9
        # WRIST = 18
    query_string = ('create table ' + tablename + '('  
                ' ID varchar(30),'  
                ' NOSE_X float,        NOSE_Y float,      NOSE_Z float,'
                ' NECK_X float,        NECK_Y float,      NECK_Z float,'
                ' RSHOULDER_X float,   RSHOULDER_Y float, RSHOULDER_Z float,'
                ' RELBOW_X float,      RELBOW_Y float,    RELBOW_Z float,'
                ' RWRIST_X float,      RWRIST_Y float,    RWRIST_Z float,'
                ' LSHOULDER_X float,   LSHOULDER_Y float, LSHOULDER_Z  float,'
                ' LELBOW_X float,      LELBOW_Y float,    LELBOW_Z float,'
                ' LWRIST_X float,      LWRIST_Y float,    LWRIST_Z float,'
                ' RHIP_X float,        RHIP_Y float,      RHIP_Z float,'
                ' RKNEE_X float,       RKNEE_Y float,      RKNEE_Z float,'
                ' WRIST_X float,       WRIST_Y float,     WRIST_Z float,'
                ' PRIMARY KEY (id)'
                ')')
    SQL_EXECUTE(query_string, tablename)

SQL_SELECT()