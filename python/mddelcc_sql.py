import csv
import time
# import logging
from bs4 import BeautifulSoup
import requests
import re
import datetime
import os
from MySQLConnector import Connection

# logging.basicConfig(level=logging.INFO)


def open_csv(date_string):

    try:
        # logging.info("Opening file MDDELCC_%s.csv") % (date_string)
        file = open('MDDELCC_' + date_string + ".csv", newline='', encoding='utf-8')
        # TODO line count CSV
        reader = csv.reader(file, delimiter='|')
        return reader
    except NameError:
        #print("File name error. Check that file was downloaded")
        os.system(log("\"MDDELCC_SQL.PY:OPEN_CSV\"", "\"File name error. Check that file was downloaded\""))
    except FileNotFoundError as fnf:
        #print("File not found error.")
        os.system(log("\"MDDELCC_SQL.PY:OPEN_CSV\"", "\"File not found error.\""))


def list_builder(file, date_string):

    # Build a list from csv file
    data = []
    # logging.info('Creating list from', "%s") % file
    for row in file:
        try:
            fiche = row[0]
            nom = row[1].replace('"', '')
            adresse = row[2].replace('"', '')
            mrc = row[3]
            latitude = row[4].replace(',', '.')
            longitude = row[5].replace(',', '.')
            eau = row[6]
            sol = row[7]
            rehab = row[8]
            date_maj = row[9]
            note = ""
            date_entree = date_string
            data.append([fiche, nom, adresse, mrc, latitude, longitude, eau, sol, rehab, date_maj, note, date_entree])

        except IndexError:
            entry = "Index error on row: " + row
            print(entry)
            os.system(log("\"MDDELCC_SQL.PY:LIST_BUILDER\"", "\"%s\"")) % entry

    return data

def record_count():
    
    conn, cursor = Connection()
    url = r'http://www.mddelcc.gouv.qc.ca/sol/terrains/terrains-contamines/resultats.asp?nom_region=*'
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'xml')

    data = soup.findAll("p")

    text = []
    for string in data[1]:
        text.append(string)

    count_str = str(text[0])
    count_int = [(int(re.search(r'\d+', count_str).group()))]

    source_count = [count_int]

    sql_query_record_count = """SELECT * FROM contaminated_geoindex_xyz.MDDELCC"""
    cursor.execute(sql_query_record_count)
    rowcount_mddelcc = (cursor.rowcount)

    sql_insert_record_count = """UPDATE SOURCES SET RECORD_COUNT = %s WHERE idSOURCES LIKE '1'""" % rowcount_mddelcc
    cursor.execute(sql_insert_record_count)
    conn.commit()

    sql_insert_source_count = """UPDATE SOURCES SET SOURCE_RECORD_COUNT = %s WHERE idSOURCES LIKE '1'""" % (
    source_count[0][0])
    cursor.execute(sql_insert_source_count)
    conn.commit()

    today = datetime.date.today()

    sql_last_update = """UPDATE SOURCES SET LAST_UPDATE=\"%s\" WHERE idSOURCES LIKE '1'""" % (today)
    cursor.execute(sql_last_update)
    conn.commit()
    return rowcount_mddelcc


# Check if database is empty
def is_database_empty(cursor, conn):
    sql_query_empty = """SELECT * FROM contaminated_geoindex_xyz.MDDELCC"""
    cursor.execute(sql_query_empty)
    conn.commit()
    return cursor.rowcount


# If record exists validate idMDDELCC and FICHE
def is_record_duplicate(item, cursor, conn):

    fiche = item[0]
    sql_query_duplicate = """SELECT * FROM contaminated_geoindex_xyz.MDDELCC
                    WHERE FICHE LIKE %s""" % fiche
    cursor.execute(sql_query_duplicate)
    duplicate = cursor.fetchone()
    conn.commit()
    return cursor.rowcount, duplicate

# Check if identical record exists
def is_record_identical(item, cursor, conn):

    fiche = item[0]
    nom = item[1]
    adresse = item[2]
    mrc = item[3]
    latitude = item[4]
    longitude = item[5]
    eau = item[6]
    sol = item[7]
    rehab = item[8]
    date_maj = item[9]

    sql_query_identical = """SELECT * FROM contaminated_geoindex_xyz.MDDELCC
                            WHERE FICHE LIKE "%s"
                            AND NOM LIKE \"%s\"
                            AND ADRESSE LIKE \"%s\"
                            AND MRC LIKE \"%s\"
                            AND LATITUDE LIKE \"%s\"
                            AND LONGITUDE LIKE \"%s\"
                            AND EAU LIKE \"%s\"
                            AND SOL LIKE \"%s\"
                            AND REHAB LIKE \"%s\"
                            AND DATE_MAJ LIKE \"%s\" """ % (
                                                            fiche,
                                                            nom,
                                                            adresse,
                                                            mrc,
                                                            latitude,
                                                            longitude,
                                                            eau,
                                                            sol,
                                                            rehab,
                                                            date_maj
                                                        )
    cursor.execute(sql_query_identical)
    conn.commit()
    return cursor.rowcount


# Add a note to indicate that a duplicate record exists in MDDELCC
def update_record_note(item, cursor, conn, duplicate):
    note = "Valider la fiche: %s a l'address %s dans la MRC %s" % (item[0], item[2], item[3])

    # print(note)

    sql_update_note = """UPDATE MDDELCC SET NOTES=\"%s\"
                        WHERE idMDDELCC=%s""" % (note, duplicate[0])
    cursor.execute(sql_update_note)
    conn.commit()


# Update existing item if it has changed
def update_record(item, cursor, conn):
    blah = item[0]
    sql_update_record = """%s""" % blah
    cursor.execute(sql_update_record)
    conn.commit()


# If database is empty we need to inject data into it
def insert_record(item, cursor, conn, rowcount_mddelcc):

    def insert():
        sql_insert_mddelcc = """INSERT INTO MDDELCC (
                                                    idMDDELCC,
                                                    FICHE,
                                                    NOM,
                                                    ADRESSE,
                                                    MRC,
                                                    LATITUDE,
                                                    LONGITUDE,
                                                    EAU,
                                                    SOL,
                                                    REHAB,
                                                    DATE_MAJ,
                                                    NOTES,
                                                    TIMESTAMP
                                                    )
                                VALUES (default,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        # print(item)
        cursor.execute(sql_insert_mddelcc, item)
        conn.commit()

    if rowcount_mddelcc == -1:
        insert()
    else:
        found_dup, duplicate = is_record_duplicate(item, cursor, conn)
        found_ident = is_record_identical(item, cursor, conn)
        # if duplicate but not identical
        if found_dup >= 1 and found_ident != 1:
            #update_record_note(item, cursor, conn, duplicate)
            entry = "Valider la fiche: %s a l'address %s dans la MRC %s" % (item[0], item[2], item[3])
            os.system(log("\"MDDELCC_SQL.PY:INSERT_RECORD\"", "\"%s\"")) % entry
        elif found_ident == 1:
            #print("Record", item[0], "already in database")
            entry = "Record " + item[0] + " already in database...skipping"
            os.system(log("\"MDDELCC_SQL.PY:INSERT_RECORD\"", "\"Record " + item[0] + " already in database...skipping\""))
        else:
            insert()
def log(program, entry):
    program = program
    entry = entry
    command = "python3 logger.py -p %s -e %s" % (program,entry)
    return command


def updateSourceResult(strUpdateResult,cursor,conn):
    sqlUpdate = "UPDATE SOURCES SET LAST_UPDATE_RESULT=\""+ strUpdateResult +"\" WHERE NAME LIKE \"MDDELCC\""
    cursor.execute(sqlUpdate)
    conn.commit()

def main():

    # Connect to database
    cursor, conn = Connection()

    # Generate a date in string format
    date_string = time.strftime("%Y%m%d")

    # 
    
    os.system(log("\"MDDELCC_SQL.PY:MAIN\"", "\"Opening csv file\""))
    file = open_csv(date_string)

    # Build the list
    
    os.system(log("\"MDDELCC_SQL.PY:MAIN\"", "\"Generating array list\""))
    mddelcc = list_builder(file, date_string)

    # Check if DB is empty
    rowcount_mddelcc = is_database_empty(cursor, conn)

    
        # logging.info("MDDELCC database has", "%s", "records. Looking for updates...") % rowcount_mddelcc

        # Download new data
        # Do a diff with older file
        # Append new data to DB
        # Remove subtracted records from DB
    
    os.system(log("\"MDDELCC_SQL.PY:MAIN\"", "\"Interating...\""))
    insertCount = 0     
    for item in mddelcc:
        insert_record(item, cursor, conn, rowcount_mddelcc)
        insertCount += 1
    recordCount = record_count()
    
    os.system(log("\"MDDELCC_SQL.PY:MAIN\"", "\"done\""))
    strUpdateResult = "Inserted " + insertCount + " records. Source contains " + recordCount + " records" 

    os.system(log("\"MDDELCC_SQL.PY:MAIN\"", "\"Updating table SOURCES with update result\"")) % entry
    updateSourceResult(strUpdateResult,cursor,conn)

    conn.close()
    # logging.info("Done!")
    exit(0)


if __name__ == '__main__':
    main()
