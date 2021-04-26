# -*- coding: utf-8 -*-
import urllib.request
import json
from collections import OrderedDict
import csv
import codecs
import time

#郵便番号は飛番
urlOrg = 'https://zipcloud.ibsnet.co.jp/api/search'
urlOrg2 = 'http://127.0.0.1:8090/api/search'
method = "GET"
headers = {'User-Agent':'Mozilla/5.0'
           ,"Content-Type" : "application/json"}
params = {'zipcode': ''}

trade_org = json.load(open('../data/zip_cd.json', 'r'), object_pairs_hook=OrderedDict)
trade_org_val =  trade_org["data"]
fw = codecs.open('../data/zip_cd.csv', "wb","utf-8")
writer = csv.writer(fw, lineterminator=u'\n')

row = trade_org_val[0].values()
writer.writerow(row)

try:
    for i in range(1000001,1001000):
        ZIP_CD ='{0:07d}'.format(i)
        params['zipcode']= ZIP_CD
        params['aaaa']= ZIP_CD
        # クエリストリング
        req = "{}?{}".format(urlOrg, urllib.parse.urlencode(params))
        # URL OPEN
        time.sleep(1)
        print (req)

        request = urllib.request.Request(url=req, headers=headers, method=method)
        response = urllib.request.urlopen(url=request,timeout=3600)
        print(response.headers)
        httpResopnse = json.loads(response.read(), object_pairs_hook=OrderedDict)
        if httpResopnse["status"]==200:
            if httpResopnse["results"] is not None:
                ## JAVAにリクセスト送信（お試し）
                ##headers['content-length']=0
                json_data=json.dumps(httpResopnse).encode("utf-8")
                request2 = urllib.request.Request(url=urlOrg2, data=json_data,headers=headers, method="POST")
                response2=urllib.request.urlopen(url=request2)

                target_dicts = httpResopnse['results']
                json_string = json.dumps(target_dicts, indent=2,ensure_ascii=False)
                row=list()
                for infos in httpResopnse["results"]:
                    for key in trade_org_val[0].keys():
                        if key in infos :
                            row.append(infos.get(key))
                        else:
                            row.append(None)
                    writer.writerow(row)
                    row.clear()
                    fw.flush()

                #request2 = urllib.request.Request(url=urlOrg2, data=json_data,headers=headers, method="DELETE")
                #response2=urllib.request.urlopen(url=request2)

            else:
                print(ZIP_CD + ":該当なし")
        else:
            print(httpResopnse["message"])

    fw.close()
    fr=open("../data/zip_cd.csv", "r")
    datalist = fr.readlines()
    for data in datalist:
        print(data)
    fr.close()
except urllib.error.HTTPError as e:
    print (e.reason)
    None
except :
    print (e)
    None
   #print e.code

