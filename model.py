import datetime
# import MySQLdb
import pymysql.cursors
import pymysql


def get_conn():
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            db='ShortUrl',
            charset='utf8')  # here need to change database to 'UTF-8' charset.
    except pymysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
    return conn


def db_add(url1, url2, a):
    conn = get_conn()
    cursor = conn.cursor()
    dt = datetime.datetime.now()
    dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    ct = int(1)

    sql_insert = ("INSERT INTO shorturls(longurl,shorturl,IsSelf,insertDate,count) VALUE('%s','%s',%s,'%s','%d');") % (
        url1, url2, a, dt, ct)

    try:
        # print(sql_insert)
        cursor.execute(sql_insert)
        conn.commit()
    except Exception as e:
        # 错误回滚
        print("something wrong:%s" % e)
        conn.rollback()
    finally:
        conn.close()


def update_in_query(conn, cursor, id, ct):
    try:
        ct = int(ct) + 1  # 访问数+1
        sql = "UPDATE shorturls set count={0} WHERE id={1}".format(ct, id)
        # print(sql)
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        # 错误回滚
        print("something wrong:%s" % e)
        conn.rollback()


def db_query_longurl(url1):
    conn = get_conn()
    cursor = conn.cursor()
    sql = "SELECT * FROM shorturls WHERE longurl = '%s'" % (url1)

    try:
        # print(sql)
        rest = cursor.execute(sql)
        print(rest)
        x = ''
        if rest != 0:
            row = cursor.fetchone()
            # print(row)
            id = row[0]
            x = row[2]
            ct = row[5]
            update_in_query(conn, cursor, id, ct)
            print(row[2])
        return rest, x
    except Exception as e:
        # 错误回滚
        print("something wrong:%s" % e)
        conn.rollback()
    finally:
        conn.close()


def db_query_shorturl(url2):
    conn = get_conn()
    cursor = conn.cursor()
    sql = "SELECT * FROM shorturls WHERE shorturl = '%s'" % (url2)

    try:
        # print(sql)
        rest = cursor.execute(sql)
        print(rest)
        x = ''
        if rest != 0:
            row = cursor.fetchone()
            id = row[0]
            x = row[1]
            ct = row[5]
            update_in_query(conn, cursor, id, ct)
            print(row[1])
        return rest, x
    except Exception as e:
        # 错误回滚
        print("something wrong:%s" % e)
        conn.rollback()
    finally:
        conn.close()

# db_add('https://www.cnblogs.com/gavinyyb/p/6413467.html','https://yun.io/VfIazv',1)
# db_query_longurl('https://www.cnblogs.com/gavinyyb/p/6413467.html')
