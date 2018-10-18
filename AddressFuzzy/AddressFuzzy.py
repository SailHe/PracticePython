
#!/usr/local/bin/python
# -*- coding: utf8 -*-
 
'''
Created on 2016年6月12日
@author: PaoloLiu
'''
 
from mysqlhelper import *
import logging,re,sys,itertools,time
 
def logger():
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] [%(filename)s] [%(threadName)s] [line:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
 
def get_list_dict(mysqldb):
    
    results=mysqldb.executequery("select name from namedict")
    
    list_dict=[]
    
    for row in results:
        list_dict.append(row[0].decode("utf8"))
    
    list_dict.sort(cmp=None, key=None, reverse=False)
    
    return list_dict
 
def get_dic(list_dict):
    dic={}
    
    for item in list_dict:
        dic[item]=1
    
    return dic
 
def index_range(list,item):
    
#     list要求是已排序的
    
    length=len(list)
    
    result={}
    
    if item<list[0] or item>list[len(list)-1]:
        result["error"]=True
    
    else:
      
        for i in range(length/1000,-1,-1):
            if item>=list[i*1000]:                
                branch=i*1000
#                 logging.debug("branch="+str(branch))                
                break
        
        for i in range(branch,length):
            if list[i]>=item:
                result["begin"]=i
                result["end"]=i
#                 logging.debug("result[\"begin\"]="+str(result["begin"]))
                break
        
        for i in range(result["begin"],length):
            if item<list[i]:
                result["end"]=i
#                 logging.debug("result[\"end\"]="+str(result["end"]))
    
    return result
 
def isexist(name,dic,list_dict):
    pass
 
    result=[]
    
    if dic.get(name):
        result.append(name)  
    else:
        pass
        
        range_result=index_range(list_dict,name)
        
        if range_result.get("error"):
            pass
        else:
            for i in range(range_result["begin"],range_result["end"]+1):
#                 logging.debug("name="+name)
#                 logging.debug("listname="+list_dict[i][0])
                if re.match(name+".*",list_dict[i]):
#                     logging.debug("name="+name)
#                     logging.debug("listname="+list_dict[i][0])
                    result.append(list_dict[i])
    
    return result
 
def div_word(name,dic,list_dict):
    divlist=[]
    
    while len(name)>=2:
        match_flag=0
#         logging.debug("name:"+name)
        for i in range(2,len(name)+1):
            result=[]
            result=isexist(name[0:i],dic,list_dict)
#             logging.debug("test name:"+name[0:i])
            if len(result)>0:
                pass
                match_flag=1
                previous=result
            else:
                if match_flag==1:
#                     logging.debug("div name1:"+name[0:i-1]) 
                    divlist.append(previous)
#                     logging.debug(previous)
                    name=name[i-1:]
#                     logging.debug("new name:"+name)
                    break
            
            if i==len(name) and len(result)>0:
#                 logging.debug("div name2:"+name[0:i]) 
                divlist.append(result)
                name=name[i:]
            elif i==len(name):
                name=name[1:]
    
    return divlist
 
def get_fullname_list(mysqldb):
    strsql="select village_name from new_village;"
    
    results=mysqldb.executequery(strsql)
    
    fullname_list=[]
    
    for row in results:
        fullname_list.append(row[0].decode("utf8"))
    
    return fullname_list
 
def get_fullindex(fullname_list):
    fullindex={}
    
    for i in range (0,len(fullname_list)):
        split_list=fullname_list[i].split("-")
        for item in split_list:
            if fullindex.get(item):
                fullindex[item].add(i)
            else:
                fullindex[item]=set()
                fullindex[item].add(i)
    
    return fullindex
        
def main():
    
    begin=time.time()
    
    mysqldb=mysqlhelper("dbaadmin","123456","172.16.2.7","3306","spider")
    mysqldb.connect()
    
    list_dict=get_list_dict(mysqldb)    
    dic=get_dic(list_dict)
        
    fullname_list=get_fullname_list(mysqldb)     
    fullindex=get_fullindex(fullname_list)
    
    load_data_time=round((time.time()-begin),2)
    logging.info("加载数据耗时"+str(load_data_time))
    logging.info("==============================================")
    
    name=u"无极县东侯坊乡南池阳村助农点"
    divlist=div_word(name, dic, list_dict)   
     
    for x in itertools.product(*divlist):
        result=fullindex[x[0]]
#         logging.debug(x[0])
#         logging.debug(fullindex[x[0]])
        
        for i in range(1,len(x)):
#             logging.info(x[i])
#             logging.info(fullindex[x[i]])
            result=result&fullindex[x[i]]
        
        if len(result)>0:
            for item in result:
#                 logging.debug(item)
                logging.info("match name:"+fullname_list[item])
    
    match_time=round((time.time()-begin-load_data_time),2)
    logging.info("名称匹配耗时"+str(match_time))
              
    logging.info("==============================================")
    logging.info("list_dict getsizeof:"+str(sys.getsizeof(list_dict)))
    logging.info("dic getsizeof:"+str(sys.getsizeof(dic)))
    logging.info("fullname_list getsizeof:"+str(sys.getsizeof(fullname_list)))
    logging.info("fullindex getsizeof:"+str(sys.getsizeof(fullindex)))
    
    mysqldb.close()
if __name__ == '__main__':
    pass
    
    logger()
    
    main()
