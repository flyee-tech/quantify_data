# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
import mysql_conn


def resetColor(b):
    w = b.get_width()
    if w < 100:
        b.set_color(r'#76C7DB')
    if 100 <= w < 200:
        b.set_color(r'#AA6ED0')
    if 200 <= w < 300:
        b.set_color(r'#DF29D3')
    if w >= 300:
        b.set_color(r'#CAAE7C')


def resetWidth(b):
    w = b.get_width()
    if 100 < w <= 200:
        b.set_width(w - 100)
    if 200 < w <= 300:
        b.set_width(w - 200)
    if w > 300:
        b.set_width(w - 300)


fmt = '%.2f%%'
conn = mysql_conn.conn()
sql = '''
    SELECT CONCAT(s.belong, ':', s.name) AS name,
           s.`total`,
           cc.number,
           cc.times
    FROM subject AS s
    LEFT JOIN
      (SELECT bb.`subject_id`,
              bb.`number`,
              bb.`times`
       FROM
         (SELECT max(id) AS id
          FROM `subject_progress`
          GROUP BY `subject_id`) AS aa
       INNER JOIN `subject_progress` AS bb ON bb.id = aa.id) AS cc ON cc.subject_id = s.id
    WHERE cc.`subject_id` IS NOT NULL;
    '''
df = pd.read_sql(sql=sql, con=conn)
df.loc[:, 'progress'] = df.apply(lambda x: (x.number * x.times / x.total * 100), axis=1)

y = list(df['name'])
width = list(df['progress'])
plt.figure(num=1, figsize=(8, 2))
bar_list = plt.barh(y, width, height=0.7, color='b')
for bar in bar_list:
    resetColor(bar)
    resetWidth(bar)
    plt.text(bar.get_width() + 1,
             bar.get_y() + 0.3,
             fmt % bar.get_width(),
             horizontalalignment='left',
             verticalalignment='center',
             weight='bold')

ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
xticks = mtick.FormatStrFormatter(fmt)
ax.xaxis.set_major_formatter(xticks)

plt.xlim(0, 100)
plt.title('进度')
plt.rcParams['savefig.dpi'] = 120  # 图片像素
plt.rcParams['figure.dpi'] = 120  # 分辨率
plt.show()
