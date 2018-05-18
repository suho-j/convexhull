import pymysql
import datetime

HOST = '192.168.0.41'
PORT = 3306
USER = 'kgm'
PASSWORD = '123123'
DATABASE = 'o2'
TABLENAME   = 'jointxyz'


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
    query_string = ("select RWRIST_X from jointxyz")
    RWRIST_X = SQL_EXECUTE(query_string, tablename)
    query_string = ("select RWRIST_Y from jointxyz")
    RWRIST_Y = SQL_EXECUTE(query_string, tablename)
    query_string = ("select RWRIST_Z from jointxyz")
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
                ' NOSE_X varchar(10),        NOSE_Y varchar(10),      NOSE_Z varchar(10),'
                ' NECK_X varchar(10),        NECK_Y varchar(10),      NECK_Z varchar(10),'
                ' RSHOULDER_X varchar(10),   RSHOULDER_Y varchar(10), RSHOULDER_Z varchar(10),'
                ' RELBOW_X varchar(10),      RELBOW_Y varchar(10),    RELBOW_Z varchar(10),'
                ' RWRIST_X varchar(10),      RWRIST_Y varchar(10),    RWRIST_Z varchar(10),'
                ' LSHOULDER_X varchar(10),   LSHOULDER_Y varchar(10), LSHOULDER_Z  varchar(10),'
                ' LELBOW_X varchar(10),      LELBOW_Y varchar(10),    LELBOW_Z varchar(10),'
                ' LWRIST_X varchar(10),      LWRIST_Y varchar(10),    LWRIST_Z varchar(10),'
                ' RHIP_X varchar(10),        RHIP_Y varchar(10),      RHIP_Z varchar(10),'
                ' RKNEE_X varchar(10),       RKNEE_Y varchar(10),      RKNEE_Z varchar(10),'
                ' WRIST_X varchar(10),       WRIST_Y varchar(10),     WRIST_Z varchar(10),'
                ' PRIMARY KEY (id)'
                ')')
    SQL_EXECUTE(query_string, tablename)

# SQL_SELECT()
# SQL_DROPTABLE()
# SQL_CREATETABLE()
