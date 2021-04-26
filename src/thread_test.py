from multiprocessing import Process, Queue
from multiprocessing import Lock
import logging
import os
import sys
import MySQLdb
import time
import datetime

formats="%(asctime)s [%(filename)s:%(lineno)d] %(levelname)-8s %(processName)s %(message)s"
logging.basicConfig(level=logging.DEBUG, format=formats)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
logger = logging.getLogger(__name__)

def SenderTask(lqueue,queueCnt,taskCnt):
    connection = MySQLdb.connect(
        host='localhost', user='root', passwd='20067655h', db='app', charset='utf8')
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    # 商品グループ作成用list
    LISA = [[0 for _ in range(2)] for i in range(queueCnt)]
    for i in range(queueCnt):
        LISA[i][0]=i

    cursor.execute("SELECT ID,CNT FROM PRODUCT_CATEGORY ORDER BY CNT DESC")
    rows = cursor.fetchall()
    print (rows)
    DICA=dict()
    for row in rows :
        LISA.sort(key=lambda x: x[1])
        LISA[0][1]=LISA[0][1] + row["CNT"]
        DICA[row["ID"]]=LISA[0][0]
        #print (DICA)

    print (LISA)
    print (DICA)

    cursor.execute("SELECT PRODUCTID FROM PRODUCT ORDER BY RAND()")
    rows = cursor.fetchall()
    cnt = 0
    for row in rows :
        cnt = cnt + 1
        PRODUCTID = int(row["PRODUCTID"])
        lqueue[DICA[row["PRODUCTID"]]].put(row)
#        lqueue[PRODUCTID % queueCnt].put(row)
#        lqueue[cnt % queueCnt].put(row)

    cursor.close()
    connection.close()
    logger.info("送信完了:" + str(cnt))
    for _ in range(taskCnt):
        for num2 in range(queueCnt):
            lqueue[num2].put(None)
            lqueue[num2].put(None)
            lqueue[num2].put(None)


def ReceiverTask(queue,l):
    cnt = 0
    startTime = datetime.datetime.now()
    connection = MySQLdb.connect(
        host='localhost', user='root', passwd='20067655h', db='app', charset='utf8')
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    sql ="SELECT * FROM PRODUCT WHERE ID ='%s' FOR UPDATE"
    while True:
#        l.acquire()
        try:
            if (row:=queue.get())!=None :
                cnt = cnt + 1
                cursor.execute("SELECT * FROM Product_Category WHERE ID ='" + row["PRODUCTID"] + "' FOR UPDATE")
                if cnt % 10000 == 0 :
                    logger.info("件数:" + str(cnt))
                time.sleep(0.009)
                connection.commit()
            else :
                break
        finally:
            pass
#            l.release()
    endTime = datetime.datetime.now()
    logger.info("終了: 件数:" + str(cnt) )
    logger.info((abs(startTime - endTime)))

if __name__ == '__main__':
    queue = list()
    queueCnt = 10
    taskCnt = 10
    for num in range(queueCnt):
        queue.append(Queue())
    lock = Lock()
    # SenderTask
    p1 = Process(target=SenderTask, args=(queue,queueCnt,taskCnt))
    # ReceiverTask
    for num in range(taskCnt):
        p2 = Process(target=ReceiverTask, args=(queue[num],lock)).start()

    p1.start()
    p1.join()

