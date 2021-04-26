# Python 3.5.2 にて動作を確認
# MySQLdb をインポート
import MySQLdb
import csv
import codecs
import json
import pprint

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

logger.info("メッセージです。")
logger.error("エラーです。")

# データベース接続とカーソル生成
# 接続情報はダミーです。お手元の環境にあわせてください。
connection = MySQLdb.connect(
    host='localhost', user='root', passwd='20067655h', db='app', charset='utf8')
cursor = connection.cursor(MySQLdb.cursors.DictCursor)

# エラー処理（例外処理）
try:
    ########################################################
    ##  DB
    ########################################################
    # CREATE
    # id, name だけのシンプルなテーブルを作成。id を主キーに設定。
    cursor.execute("DROP TABLE IF EXISTS `sample`")
    cursor.execute("""CREATE TABLE IF NOT EXISTS `sample` (
    `id` int(11) NOT NULL,
    `name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
    PRIMARY KEY (id)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""")

    # INSERT
    cursor.execute("INSERT INTO sample VALUES (1, '佐藤')")

    # プレースホルダの使用例
    # 1つの場合には最後に , がないとエラー。('鈴木') ではなく ('鈴木',)
    cursor.execute("INSERT INTO sample VALUES (2, %s)", ('鈴木',))
    connection.commit()
    cursor.execute("INSERT INTO sample VALUES (%s, %s)", (3, '高橋'))
    cursor.execute("INSERT INTO sample VALUES (%(id)s, %(name)s)", {'id': 4, 'name': '田中'})

    # 複数レコードを一度に挿入 executemany メソッドを使用
    persons = [
        (5, '伊藤'),
        (6, '渡辺'),
    ]
    cursor.executemany("INSERT INTO sample VALUES (%s, %s)", persons)

    cursor.execute("SELECT * FROM PRODUCT_CATEGORY")
    rows = cursor.fetchall()
    print(rows)
    for row in rows :
        print(row)


    # わざと主キー重複エラーを起こして例外を発生させてみる
    cursor.execute("INSERT INTO sample VALUES (1, '中村')")
except MySQLdb.Error as e:
    print('MySQLdb.Error: ', e)

# 保存を実行（忘れると保存されないので注意）
connection.commit()

# 接続を閉じる
connection.close()

    ########################################################
    ##  CSV
    ########################################################
connection = MySQLdb.connect(
    host='localhost', user='root', passwd='20067655h', db='app', charset='utf8')
cursor = connection.cursor(MySQLdb.cursors.DictCursor)
try:
    # DBテーブルを辞書に読み込み
    cursor.execute("SELECT * FROM sample")
    rows = cursor.fetchall()
    csvdata=dict()
    csvdata["USER"]=list(dict())
    for row in rows:
        csvdata["USER"].append(row)
    for row in csvdata["USER"]:
        print ("D")
        print (row)

    pprint.pprint(csvdata)
    print ( json.dumps(csvdata, indent=2, ensure_ascii=False))

    # 辞書をCSVファイルに書き込み
    csv.register_dialect('pipes', delimiter=',', doublequote=True)
    with open('../data/user.csv', 'w',newline='') as csvfile:
        fieldnames = ['id', 'name']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames,dialect='pipes')
        writer.writeheader()
        for data in csvdata["USER"]:
            writer.writerow(data)

    # CSVファイルを辞書に読み込み
    rcsvdata=dict()
    rcsvdata["USER"]=list(dict())
    with open('../data/user.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile,dialect='pipes')
        print ("R")
        for row in reader:
            print( row)
            rcsvdata["USER"].append(row)
    pprint.pprint(rcsvdata)
    print ( json.dumps(rcsvdata, indent=2, ensure_ascii=False))
except MySQLdb.Error as e:
    print('MySQLdb.Error: ', e)

