from MySQLConnector import Connection
import sys
import getopt
import time
import argparse

def get_timestamp():
    date_string = time.strftime("%Y-%m-%d - %H:%M")
    return date_string

cursor, conn = Connection()


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--program", required=True, help="type string script name")
    parser.add_argument("-e", "--entry", required=False, help="type string entry description")
    parser.add_argument("-r", "--error", required=False, help="type string error")

    args = parser.parse_args()

    print("Program {} Entry {} Error {} ".format(
        args.program,
        args.entry,
        args.error
    ))
    
    return args.program, args.entry, args.error


def get_id_update():


    sql_get_idUpdates = """SELECT idUPDATES FROM UPDATES WHERE LAST_UPDATE_END IS NULL ORDER BY idUPDATES DESC LIMIT 1;"""
    print(sql_get_idUpdates)
    cursor.execute(sql_get_idUpdates)
    id = cursor.fetchone()
    conn.commit()
    return id[0]

def write_log(idupdates, program, timestamp, entry, er):
    timestamp = timestamp
    idupdates = idupdates
    program = program
    entry = entry
    er = er

    sql_insert_logs = """INSERT INTO contaminated_geoindex_xyz.LOGGER (idLOGS, idUpdate, PROGRAM, ENTRY, ERROR) VALUES (default, %s, '%s', '%s: %s', '%s:%s')""" % (idupdates, program, timestamp, entry, timestamp,er)
    print("DEBUG::WRITE_LOG:sql_insert_logs " + sql_insert_logs)
    print ("DEBUG::WRITE_LOG:entry " + entry)
    print ("DEBUG::WRITE_LOG:error " + er + "\n")
    
    cursor.execute(sql_insert_logs)
    conn.commit()


idupdates = get_id_update()
timestamp = get_timestamp()
program, entry, er = main()

print ("DEBUG::NML:entry " + entry)
print ("DEBUG::NML:er " + er)
write_log(idupdates, program, timestamp, entry, er)
conn.close()

if __name__ == "__main__":
    main()

