# -*- coding: utf-8 -*-
import urllib.request,urllib.error
import json

from collections import OrderedDict
import csv
import codecs

#https://www.land.mlit.go.jp/webland/api.html
#不動産取引価格情報取得API
#都道府県内市区町村一覧取得API
urlOrg = 'https://www.land.mlit.go.jp/webland/api/CitySearch'
params = {'area': ''}
urlOrg2 = 'https://www.land.mlit.go.jp/webland/api/TradeListSearch'
params2 = {'from': '20151','to':'20152','city':''}

trade_org = json.load(open('../data/trade_org.json', 'r'), object_pairs_hook=OrderedDict)
trade_org_val =  trade_org["data"]

fw = codecs.open('../data/trade.csv', "wb","utf-8")
writer = csv.writer(fw, lineterminator=u'\n')
row = trade_org_val[0].values()
writer.writerow(row)


#trade_data_org =json.loads()
try:
    st=1
    ed=st +1
    for i in range(st,ed):
        # URL パラメタ組み立て
        AREA_CD ='{0:02d}'.format(i)
        params['area']= AREA_CD
        url = "{}?{}".format(urlOrg, urllib.parse.urlencode(params))
        print (url)
        response = urllib.request.urlopen(url=url)

        httpResopnse = json.loads(response.read(), object_pairs_hook=OrderedDict)
        if httpResopnse["status"]=="OK":
            if httpResopnse["data"] is not None:
                target_dicts = httpResopnse['data']
                #json_string = json.dumps(target_dicts, indent=2, encoding='utf_8').decode('unicode-escape')
                infos = httpResopnse["data"]
                for info in infos:
                    # URL パラメタ組み立て
                    params2["city"]=info["id"]
                    url2 = "{}?{}".format(urlOrg2, urllib.parse.urlencode(params2))
                    print (url2)
                    # URL OPEN
                    response2 = urllib.request.urlopen(url=url2)
                    httpResopnse2 = json.loads(response2.read(), object_pairs_hook=OrderedDict)
                    json_string = json.dumps(httpResopnse2['data'], indent=2, encoding='utf_8').decode('unicode-escape')
                    infos2 = httpResopnse2["data"]
                    row=list()
                    for info2 in infos2:
                        for key in trade_org_val[0].keys():
                            if key in info2 :
                                row.append(info2.get(key))
                            else:
                                row.append(None)
                        writer.writerow(row)
                        row.clear()
                        fw.flush()
            else:
                print(AREA_CD + ":該当なし")
        else:
            print(httpResopnse["message"])
except urllib.error.HTTPError as e:
    None
fw.close()
fr=open("../data/trade.csv", "r")
datalist = fr.readlines()
for data in datalist:
    print(data)
fr.close()

