# -*- coding:utf-8 -*-
import newspaper

# url = 'http://news.10jqka.com.cn/20180329/c13697903.shtml'
# a = newspaper.Article(url, language='zh')
# a.download()
# a.parse()
# print(a.text.replace("\n", ""))

import xlrd
import pymysql
import re

conn = pymysql.connect(host='localhost', port=3306, user='root',
                       passwd='****', db='test', charset='utf8mb4')
p = re.compile(r'\s')
data = xlrd.open_workbook('news.xlsx')
table = data.sheets()[0]
t = table.col_values(1)
nrows = table.nrows
ops = []
for i in range(nrows):
    r1 = table.row_values(i)
    url = r1[3]
    print url
    a = newspaper.Article(url, language='zh')
    a.download()
    a.parse()
    text = a.text.replace("\n", "")
    if len(text)>20000:
        text = text[0:8000]
    cur = conn.cursor()
    try:
        cur.executemany('insert into `baojing` (`title`, `from`, `company`, `URL`, `SECTION`, `text`) \
            values (%s, %s, %s, %s, %s, %s)', ops)
        # cur.execute("UPDATE `baojing` SET `text`='"+text+"' WHERE (`URL`='"+url+"') and (`text`= '1')")
    except Exception as e:
        pass
    conn.commit()
    cur.close()
conn.close()
