import time
from MySQLConnector import Connection

cursor, conn = Connection()

date_string = time.strftime("%Y-%m-%d - %H:%M")

# sql_select_updates = """SELECT idUPDATES FROM UPDATES ORDER BY idUPDATES DESC LIMIT 1;"""
sql_select_updates = """SELECT idUPDATES FROM UPDATES WHERE LAST_UPDATE_END IS NULL ORDER BY idUPDATES DESC LIMIT 1;"""
cursor.execute(sql_select_updates)
idUPDATES = cursor.fetchone()

sql_update_updates = """UPDATE UPDATES SET LAST_UPDATE_END=("%s") WHERE idUPDATES LIKE %s;""" % (date_string,idUPDATES[0])
cursor.execute(sql_update_updates)
conn.commit()
conn.close()

sql_select_updates = """SELECT idUPDATES FROM UPDATES WHERE LAST_UPDATE_END IS NULL order BY idUPDATES DESC LIMIT 1;"""
