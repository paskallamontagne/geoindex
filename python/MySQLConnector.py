import MySQLdb


def Connection():
    conn = MySQLdb.connect(
        host='mysql.geoindex.xyz',
        user='geoindex_sqladm',
        passwd='6aTF5i4NR3nxuqJ95',
        db='contaminated_geoindex_xyz'
    )
    cursor = conn.cursor()
    return cursor, conn


if __name__ == '__main__':
    cursor, conn = connection()
    print('connection successful')

