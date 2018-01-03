import datetime
import time
from MySQLConnector import Connection

#second version of log function
def insertLog(cursor, conn, program, entry, er):
    timestamp = time.strftime("%Y-%m-%d - %H:%M")

    #get current update
    sql_get_idUpdates = """SELECT idUPDATES FROM UPDATES WHERE LAST_UPDATE_END IS NULL ORDER BY idUPDATES DESC LIMIT 1;"""
    print("DEBUG:LOG:sql_get_idUpdates: " + sql_get_idUpdates)
    cursor.execute(sql_get_idUpdates)
    id = cursor.fetchone()
    print("DEBUG:LOG:id: " + str(id) ) 
    conn.commit()
    idUpdates = id[0]

    sql_insert_logs = """INSERT INTO contaminated_geoindex_xyz.LOGGER (idLOGS, idUpdate, TIMESTAMP,PROGRAM, ENTRY, ERROR) VALUES (default, %s, '%s','%s', '%s', '%s')""" % (idUpdates, timestamp, program, entry,er)
    print("DEBUG:LOG:sql_insert_logs: " + sql_insert_logs)
    cursor.execute(sql_insert_logs)
    conn.commit()
