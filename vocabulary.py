# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import mysql_conn

conn = mysql_conn.conn()
df = pd.read_sql(sql='select `date`,`total` from `vocabulary`', con=conn)


x = list(df['date'])
y = list(df['total'])
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

plt.figure(num=1)
plt.plot(x, y)

plt.ylabel(u'Vocabulary')

# plt.gca()
# 设置数字标签
for a, b in zip(x, y):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)

plt.show()
