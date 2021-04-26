import urllib.request,urllib.error
import json
from collections import OrderedDict
import csv
import codecs

url = 'http://apiactress.appspot.com/api/1/getdata/'
method = "GET"
headers = {'User-Agent':'Mozilla/5.0'}

trade_org = json.load(open('../data/dmm.json', 'r'), object_pairs_hook=OrderedDict)
trade_org_val =  trade_org["Actresses"]

fw = codecs.open('../data/trade.csv', "wb","utf-8")
writer = csv.writer(fw, lineterminator=u'\n')
row = trade_org_val[0].values()
writer.writerow(row)

def function(arg1,arg2):
    #siin + boinで始まる女優の一覧ページ
    req=url + arg1 + arg2
    request = urllib.request.Request(url=req, headers=headers, method=method)
    response = urllib.request.urlopen(url=request)    #ページ数を取得
    httpResopnse = json.loads(response.read(), object_pairs_hook=OrderedDict)
    json_string = json.dumps(httpResopnse, indent=2,ensure_ascii=False)
#    print (json_string)
    target_dicts = httpResopnse['Actresses']
    json_string = json.dumps(target_dicts, indent=2,ensure_ascii=False)
    row=list()
    for infos in httpResopnse["Actresses"]:
        for key in trade_org_val[0].keys():
            if key in infos :
                row.append(infos.get(key))
            else:
                row.append(None)
        writer.writerow(row)
        row.clear()
        fw.flush()
        #print (infos["thumb"])
        try :
            urllib.request.urlretrieve(infos["thumb"].replace(' ', '_'),"{0}".format("../data/jpg/"+infos["oto"].replace(' ', '_')+".jpg"))
        except urllib.error.URLError as e:
            None
    return

if __name__ == '__main__':
    boins=['a', 'i', 'u', 'e', 'o']
    siins=['','k','s','t','n','h','m','y', 'r', 'w']

    for siin in siins:
        if siin == 'y':
            for boin in boins[::2]:
                df=function(siin,boin)
        elif siin == 'w':
            for boin in boins[0]:
                df=function(siin,boin)
        else:
            for boin in boins:
                df=function(siin,boin)

