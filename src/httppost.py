# -*- coding: utf-8 -*-
import urllib.request,urllib.error
import json
from collections import OrderedDict
import csv
import codecs

urlOrg = 'https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search'
urlOrg = 'http://127.0.0.1:8090/api/search'
headers = {'User-Agent':'Mozilla/5.0'}
method = "GET"

# trade_org = json.load(open('../data/zip_cd.json', 'r'), object_pairs_hook=OrderedDict)
# trade_org_val =  trade_org["data"]
# #urlOrg = 'http://localhost:8000/?zipcode='
# fw = codecs.open('../data/zip_cd.csv', "wb","utf-8")
# writer = csv.writer(fw, lineterminator=u'\n')
#
# row = trade_org_val[0].values()
# writer.writerow(row)

try:
    for i in range(5960801,5960805):
        #params="q=&targets=title&fields=contentId,title,viewCounter&filters[viewCounter][gte]=10000&_sort=-viewCounter&_offset=0&_limit=3&_context=apiguide"

        params = {
            "q" : "あいか",
            "targets" : "title",
            "fields" : "contentId,title,description,lengthSeconds,thumbnailUrl,viewCounter",
            "filters[viewCounter][gte]":10000,
            "_sort" : "-viewCounter",
            "_offset" : "0",
            "_limit" : "50",
            "_context" : "apiguide",
        }
        # json_data = json.dumps(params, indent=2,ensure_ascii=False).encode("utf-8")
        req = "{}?{}".format(urlOrg, urllib.parse.urlencode(params))
        print (req)
        request = urllib.request.Request(url=req, headers=headers, method=method)
        # URL OPEN
        response = urllib.request.urlopen(url=request)
        print(response.headers)
        httpResopnse = json.loads(response.read(), object_pairs_hook=OrderedDict)


        if httpResopnse["data"] is not None:
            target_dicts = httpResopnse['data']
            json_string = json.dumps(target_dicts, indent=2,ensure_ascii=False)
            print(json_string)
            #print ("https://nico.ms/"+target_dicts[0]["contentId"])
            #row=list()
            # for infos in httpResopnse["results"]:
                # for key in trade_org_val[0].keys():
                    # if key in infos :
                        # row.append(infos.get(key))
                    # else:
                        # row.append(None)
                # writer.writerow(row)
                # row.clear()
                # fw.flush()

        # else:
            # print(ZIP_CD + ":該当なし")

except urllib.error.HTTPError as e:
    None
    #print e.code
# fw.close()
# fr=open("../data/zip_cd.csv", "r")
# datalist = fr.readlines()
# for data in datalist:
    # print(data)
# fr.close()

