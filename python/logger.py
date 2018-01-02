from MySQLConnector import Connection
import sys
import getopt
import time

def get_timestamp():
    date_string = time.strftime("%Y-%m-%d - %H:%M")
    return date_string

cursor, conn = Connection()


def main(argv):
    program = ''
    entry = ''
    try:
        opts, args = getopt.getopt(argv, "h:p:e:", ["program=", "entry="])
    except getopt.GetoptError:
        print('logger.py -p program -e entry')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('logger.py -p program -e entry')
            sys.exit()
        elif opt in ("-p", "--program"):
            program = arg
        elif opt in ("-e", "--entry"):
            entry = arg
    return  program, entry


def get_id_update():


    sql_get_idUpdates = """SELECT idUPDATES FROM UPDATES WHERE LAST_UPDATE_END IS NULL ORDER BY idUPDATES DESC LIMIT 1;"""
    print(sql_get_idUpdates)
    cursor.execute(sql_get_idUpdates)
    id = cursor.fetchone()
    conn.commit()
    return id[0]

def write_log(idupdates, program, timestamp, entry):
    timestamp = timestamp
    idupdates = idupdates
    program = program
    entry = entry

    sql_insert_logs = """INSERT INTO contaminated_geoindex_xyz.LOGGER (idLOGS, idUpdate, PROGRAM, ENTRY) VALUES (default, %s, '%s', '%s: %s')""" % (idupdates, program, timestamp, entry)
    print(sql_insert_logs)
    print (entry)
    cursor.execute(sql_insert_logs)
    conn.commit()


idupdates = get_id_update()
timestamp = get_timestamp()
program, entry = main(sys.argv[1:])
write_log(idupdates, program, timestamp, entry)
conn.close()

if __name__ == "__main__":
    main(sys.argv[1:])

