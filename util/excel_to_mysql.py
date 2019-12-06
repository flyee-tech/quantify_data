import configparser as cp
import json

import pandas as pd
import pymysql

config = cp.ConfigParser()
config.read('../conf/mysql.conf')
host = config.get('mysql', 'host')
port = config.get('mysql', 'port')
user = config.get('mysql', 'user')
passwd = config.get('mysql', 'passwd')
conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db='quantify_data')


def df_insert_to_mysql(conn, df, table_name=None):
    if not table_name:
        return
    column_names = df.columns.values.tolist()
    insert_sql = """
                    insert into #table_name#(""" + ",".join(column_names) + """)
                    values(""" + "%(" + ")s, %(".join(column_names) + ")s" + """)
    """
    insert_sql = insert_sql.replace('#table_name#', table_name)
    data = {}
    for row in df.iterrows():
        for key in column_names:
            tmp_value = row[1][key]
            if str(tmp_value) == "NaN" or str(tmp_value) == "nan" or str(tmp_value) == "Nan":
                tmp_value = None
            data[key] = tmp_value
        execSqlData(conn, insert_sql, data)


def execSqlData(conn, sql, data):
    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
    except Exception as e:
        print("[ Exception: %s\n%s\t%s]" % (str(e), sql, json.dumps(data)))
    finally:
        cursor.close()


colomn = 'geektime:algorithms'
subject_id = 5

df_excel = pd.read_excel('/Users/peiel/PycharmProjects/quantify_data/geektime.xlsx')
df = df_excel[['Unnamed: 0', colomn]][df_excel[colomn].notna()]
df.loc[:, 'Unnamed: 0'] = df.iloc[1:]['Unnamed: 0'].map(lambda x: x.strftime('%Y-%m-%d'))
df.loc[:, 'subject_id'] = subject_id
df = df.rename(columns={'Unnamed: 0': 'data'})
df = df.rename(columns={colomn: 'number'})
df = df[1:]

print(df)
df_insert_to_mysql(conn, df, 'subject_progress')
