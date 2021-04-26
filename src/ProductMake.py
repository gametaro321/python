# Python 3.5.2 にて動作を確認
# MySQLdb をインポート
import MySQLdb
import csv
import codecs
import json
import pprint
import random
from collections import OrderedDict
import pandas as pd
from pandas.io.json import json_normalize
import logging
import os
import sys

pprint = pprint.PrettyPrinter (indent=4, compact=True)

formats="%(asctime)s [%(filename)s:%(lineno)d] %(levelname)-8s %(message)s"
logging.basicConfig(level=logging.DEBUG, format=formats)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
logger = logging.getLogger(__name__)

# データベース接続とカーソル生成
# 接続情報はダミーです。お手元の環境にあわせてください。
connection = MySQLdb.connect(
    host='localhost', user='root', passwd='20067655h', db='app', charset='utf8')
cursor = connection.cursor(MySQLdb.cursors.DictCursor)

# エラー処理（例外処理）
try:
    cursor.execute("SELECT * FROM PRODUCT WHERE ID = 'SAMPLE'")
    PRODUCT_ALL = cursor.fetchall()
    for PRODUCT_ORG in PRODUCT_ALL :
        pass
    print (PRODUCT_ORG)
    print(list(dict(PRODUCT_ORG).items()))

    print( "insert into PRODUCT (" + ", ".join([str(k) for k in PRODUCT_ORG.keys()]) + ") VALUES (" + ", ".join(["'"+ str(v) +  "'"  for v   in PRODUCT_ORG.values()]) + ")")
    cursor.execute("SELECT * FROM PRODUCT_CATEGORY")
    PCategory = cursor.fetchall()
    print(PCategory)
    cnt = 0
    for category in PCategory :
        ccnt = 0
        for i in range(category["CNT"]):
            cnt = cnt +1
            ccnt = ccnt +1
            ID ='{0:010d}'.format(cnt)
            PRODUCT_ORG["ID"] = ID
            PRODUCT_ORG["NAME"]     = category["NAME"] + "_" + '{0:05d}'.format(ccnt)
            PRODUCT_ORG["PRODUCTID"] = category["ID"]
            PRODUCT_ORG["PRICE"] = random.randint(20, 20000)
            PRODUCT_ORG["TAX"] = 8
            PRODUCT_ORG["QUANTITY"] = random.randint(0, 200)
            cursor.execute("DELETE FROM PRODUCT WHERE ID ='" + PRODUCT_ORG["ID"]  + "' ")

            cursor.execute("insert into PRODUCT (" + ", ".join([str(k) for k in PRODUCT_ORG.keys()]) + ") VALUES (" + ", ".join(["'"+ str(v) +  "'"  for v   in PRODUCT_ORG.values()]) + ")")
            connection.commit()
            pass
#            cursor.execute("INSERT INTO sample VALUES (2, %s)", ('鈴木',))
        #print(row)


except MySQLdb.Error as e:
    print('MySQLdb.Error: ', e)

# 保存を実行（忘れると保存されないので注意）
connection.commit()

# 接続を閉じる
connection.close()




