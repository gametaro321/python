import json
import random
import string
from collections import OrderedDict
import copy

ATTR_DIC={"abc"    :["NUM" , "required",None ,10    ,0   ,"fromat"]
         ,"def_abc":["STR" , None,None ,10    ,None,""]
         ,"def_def":["DIC" , "required","L1" ,None  ,None,""]
         ,"ghi"    :["STR" , "required",None ,5     ,None,"fromat"]
         ,"ghi_abc":["DIC" , "required","L2" ,None  ,None,"fromat"]
         ,None     :None
}
L={ "L1":["A","B","C","D"]
  , "L2":["AA","AB","AC","AD"]
  , None:None
}
#random.seed("20210101")
def randomitem(obj):
    if obj in ATTR_DIC :
        ATTR_LIST = (ATTR_DIC[obj])
    else:
        return None
    att = ATTR_LIST[0]
    format = ATTR_LIST[5]

    flag = False
    if ATTR_LIST[1]=="required" or flag == True :
        if att == "DIC":
            Result = None
            CLIST = L[ATTR_LIST[2]]
            Result=  random.choice(CLIST)
            return Result
        elif att == "STR":
            Result = None
            CLEN = ATTR_LIST[3]
            Result = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(CLEN)])
            return Result
        elif att == "NUM":
            Result = None
            CLEN = ATTR_LIST[3]
            Result = ''.join([random.choice(string.digits) for _ in range(CLEN)])
            return Result
        elif att == "DATE":
            Result = None
            return Result
    else:
        return None


def jsonloop(obj):
    for k, v in obj.items():
        if isinstance(v,dict):
            jsonloop(v)
        elif isinstance(v, list):
            i=0
            for item in v:
                if isinstance(item,dict):
                    jsonloop(item)
                elif isinstance(item,list):
                    None
                else:
                    v[i] = randomitem(k)
                i= i+1
        else:
            obj[k]=randomitem(k)
            None

if __name__ == '__main__':
    json_obj = json.load(open('../data/sample.json', 'r'), object_pairs_hook=OrderedDict)
    json_objl=list()
    for i in range(10):
        jsonloop(json_obj)
        print(json.dumps(json_obj, indent=2, ensure_ascii=False))
        #json_objl.append(copy.deepcopy(json_obj))

