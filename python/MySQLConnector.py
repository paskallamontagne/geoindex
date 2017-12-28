import MySQLdb


def Connection():
    conn = MySQLdb.connect(
        host='',
        user='',
        passwd='',
        db=''
    )
    cursor = conn.cursor()
    return cursor, conn


if __name__ == '__main__':
    cursor, conn = connection()
    print('connection successful')

