import csv
import time
# import logging
import datetime
import re
import requests
from bs4 import BeautifulSoup
from MySQLConnector import Connection
import sys
import codecs
import os
import geocoder

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


# logging.basicConfig(level=logging.INFO)
def open_csv(date_string):

    try:
        # logging.info("Opening file MDDELCC_%s.csv") % (date_string)
        file = open('MDDELCC_RI_' + date_string + '.csv', newline='', encoding='utf-8')
        reader = csv.reader(file, delimiter='|')
        return reader
    except NameError:
        print("File name error. Check that file was downloaded")
    except FileNotFoundError as fnf:
        print(fnf)


def list_builder(file, date_string):

    data = []
    for row in file:
        try:
            nom = row[0]
            adresse = row[1]
            mrc = row[2]
            contaminants = row[3]
            residus = row[4]
            note = ""
            timestamp = date_string
            latitude = ""
            longitude = ""
            data.append([nom, adresse, mrc, contaminants, residus, note, timestamp, latitude, longitude])
        except IndexError:
            print("Index Error")
            exit(1)
    return data


# Check if database is empty
def is_database_empty(cursor, conn):
    sql_query_empty = """SELECT * FROM contaminated_geoindex_xyz.MDDELCCRI"""
    cursor.execute(sql_query_empty)
    conn.commit()
    return cursor.rowcount


def is_record_identical(item, cursor, conn):

    # Check if identical record exists
    nom = item[0]
    adresse = item[1]
    mrc = item[2]
    contaminants = item[3]
    residus = item[4]
    sql_query_identical = """SELECT * FROM contaminated_geoindex_xyz.MDDELCCRI
                            WHERE NOM LIKE BINARY \"%s\"
                            AND ADRESSE LIKE BINARY \"%s\"
                            AND MRC LIKE BINARY \"%s\"
                            AND CONTAMINANTS LIKE BINARY \"%s\"
                            AND RESIDUS LIKE BINARY \"%s\" """ % (
                                                            nom,
                                                            adresse,
                                                            mrc,
                                                            contaminants,
                                                            residus
                                                            )
    cursor.execute(sql_query_identical)
    conn.commit()
    return cursor.rowcount


# Add a note to indicate that a duplicate record exists in MDDELCC
def update_record_note(item, cursor, conn, duplicate):
    note = "Valider la fiche portant le nom %s a l'address %s dans la MRC %s" % (item[0], item[2], item[3])
    print(note)
    sql_update_note = """UPDATE MDDELCCRI SET NOTES=\"%s\" 
                        WHERE idMDDELCCRI=%s""" % (note, duplicate[0])
    cursor.execute(sql_update_note)
    conn.commit()


# Update existing item if it has changed
def update_record(item, cursor, conn):
    blah = item[0]
    sql_update_record = """%s""" % blah
    cursor.execute(sql_update_record)
    conn.commit()


# If database is empty we need to inject data into it
def insert_record(item, cursor, conn, rowcount_mddelcc_ri):

    lenLat, latitude, longitude = geo_referencer(cursor, conn, item)

    item[7] = latitude
    item[8] = longitude

    def insert():
        sql_insert_mddelcc_ri = """INSERT INTO MDDELCCRI (idMDDELCCRI, NOM, ADRESSE, MRC, CONTAMINANTS, RESIDUS, NOTES, TIMESTAMP, LATITUDE, LONGITUDE) 
                                    VALUES (default,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        # print(item)
        cursor.execute(sql_insert_mddelcc_ri, item)
        conn.commit()

    def insert_geo(latitude, longitude):
        sql_insert_mddelcc_ri_geo = """INSERT INTO MDDELCCRI (idMDDELCCRI, NOM, ADRESSE, MRC, CONTAMINANTS, RESIDUS, NOTES, TIMESTAMP, LATITUDE, LONGITUDE) 
                                    VALUES (default,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        print(sql_insert_mddelcc_ri_geo, item)
        cursor.execute(sql_insert_mddelcc_ri_geo, item)
        conn.commit()

    print(lenLat)
    if lenLat > 0:
        insert_geo(latitude, longitude)
    else:
        print("Please create a log of this address:")
        print(item[1])
        # insert()


    # if rowcount_mddelcc_ri == -1:
    #    insert_geo(latitude, longitude)
    # else:
    #    insert_geo(latitude, longitude)
        # found_ident = is_record_identical(item, cursor, conn)
        # if found_ident == 1:
        #    print("Record already in database")
        # print("Record", item[0], "already in database")
        # else:
        #    insert()






def record_count():
    url = r'http://www.mddelcc.gouv.qc.ca/sol/residus_ind/resultats.asp?nom_region=*'
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'xml')

    data = soup.findAll("p")

    text = []
    for string in data[1]:
        text.append(string)

    count_str = str(text[1])
    count_int = [(int(re.search(r'\d+', count_str).group()))]

    source_count = []
    source_count.append(count_int)

    cursor, conn = Connection()

    sql_query_record_count = """SELECT * FROM contaminated_geoindex_xyz.MDDELCCRI"""
    cursor.execute(sql_query_record_count)
    rowcount_mddelccri = cursor.rowcount

    sql_insert_record_count = """UPDATE SOURCES SET RECORD_COUNT = %s WHERE idSOURCES LIKE '2'""" % rowcount_mddelccri
    cursor.execute(sql_insert_record_count)
    conn.commit()

    sql_insert_source_count = """UPDATE SOURCES SET SOURCE_RECORD_COUNT = %s WHERE idSOURCES LIKE '2'""" % \
                              (source_count[0][0])

    cursor.execute(sql_insert_source_count)
    conn.commit()

    today = datetime.date.today()

    sql_last_update = """UPDATE SOURCES SET LAST_UPDATE=\"%s\" WHERE idSOURCES LIKE '2'""" % today
    cursor.execute(sql_last_update)
    conn.commit()


def clear_database(cursor):

    clear_cmd_0 = """UPDATE MDDELCCRI SET SQL_SAFE_UPDATES = 0;"""
    clear_cmd_1 = """DELETE FROM MDDELCCRI; """
    clear_cmd_2 = """UPDATE MDDELCCRI SET SQL_SAFE_UPDATES = 1; """
    # cursor.execute(clear_cmd_0)
    cursor.execute(clear_cmd_1)
    # cursor.execute(clear_cmd_2)

def geo_referencer(cursor, conn, item):

    adresse = item[1]

    sql_query_adresse = "SELECT contaminated_geoindex_xyz.ADRESSES.ADRESSE, " \
                        "contaminated_geoindex_xyz.ADRESSES.LONGITUDE, " \
                        "contaminated_geoindex_xyz.ADRESSES.LATITUDE " \
                        "FROM contaminated_geoindex_xyz.ADRESSES " \
                        "WHERE LENGTH(contaminated_geoindex_xyz.ADRESSES.LONGITUDE) > 0 " \
                        "AND contaminated_geoindex_xyz.ADRESSES.ADRESSE LIKE \"%s\"" % adresse
    print(sql_query_adresse)
    cursor.execute(sql_query_adresse)

    if cursor.rowcount > 0:
        data = cursor.fetchone()
        longitude = data[1]
        latitude = data[2]
        print("FOUND: %s %s" % (longitude, latitude))
    else:
        print("NOT FOUND GEOCODING")
        g = geocoder.google(adresse)
        if g.latlng is not None:
            lat = g.latlng[0]
            lon = g.latlng[1]
            latitude = str(lat)
            longitude = str(lon)
            print("%s %s" % (longitude, latitude))
        else:
            latitude = ""
            longitude = ""
            print("NO ADRESS FOUND...")
        sqlInsertAdresse = "INSERT INTO contaminated_geoindex_xyz.ADRESSES " \
                          "(ADRESSE,LONGITUDE,LATITUDE) VALUES (\"%s\",\"%s\",\"%s\")" % (adresse, longitude, latitude)
        print(sqlInsertAdresse)
        cursor.execute(sqlInsertAdresse)
        conn.commit()

    return len(latitude), latitude, longitude

def main():
    # Connect to database
    cursor, conn = Connection()
    # Generate a date in string format
    date_string = time.strftime("%Y%m%d")
    # Read the CSV file
    file = open_csv(date_string)
    # Build the list
    mddelccri = list_builder(file, date_string)
    # Check if DB is empty
    rowcount_mddelcc_ri = is_database_empty(cursor, conn)

    if rowcount_mddelcc_ri > 0:

        clear_database(cursor)
        # logging.info("MDDELCC database has", "%s", "records. Looking for updates...") % rowcount_mddelcc
        # Download new data
        # Do a diff with older file
        # Append new data to DB
        # Remove subtracted records from DB
        for item in mddelccri:
            insert_record(item, cursor, conn, rowcount_mddelcc_ri)
        record_count()
    else:
        # logging.info("MDDELCC database has no data. Inserting data...")
        for item in mddelccri:
            insert_record(item, cursor, conn, rowcount_mddelcc_ri)
        record_count()
    conn.close()
    # os.remove('MDDELCC_RI_' + date_string + '.csv')
    # logging.info("Done!")


if __name__ == '__main__':
    main()
