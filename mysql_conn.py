import configparser as cp
import pymysql


def conn():
    config = cp.ConfigParser()
    config.read('./mysql.conf')
    host = config.get('mysql', 'host')
    port = config.get('mysql', 'port')
    user = config.get('mysql', 'user')
    passwd = config.get('mysql', 'passwd')
    conn = pymysql.connect(host=str(host),
                           port=3306,
                           user=str(user),
                           passwd=str(passwd), db='quantify_data')
    return conn
