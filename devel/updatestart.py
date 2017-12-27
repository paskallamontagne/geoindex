import time
from MySQLConnector import Connection

cursor, conn = Connection()

date_string = time.strftime("%Y-%m-%d - %H:%M")

#print(date_string)
# IF NOT FOUND USE THIS STATEMENT TO INSERT

def get_id_update():
    sql_get_idUpdates = """SELECT idUPDATES FROM contaminated_geoindex_xyz.UPDATES ORDER BY idUPDATES DESC LIMIT 1;"""
    print(sql_get_idUpdates)
    cursor.execute(sql_get_idUpdates)
    id = cursor.fetchone()
    print(id[0])
    conn.commit()
    return id[0]


def last_update_start():
    sql_insert_updates = """INSERT INTO UPDATES (LAST_UPDATE_START) VALUES ("%s")""" % date_string
    cursor.execute(sql_insert_updates)
    conn.commit()


def main():
    last_update_start()

if __name__ == '__main__':
    main()

