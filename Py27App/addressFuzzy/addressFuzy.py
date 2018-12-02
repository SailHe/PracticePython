# --encoding:utf-8--

from MySQLHelper import *
import re
import sys
import itertools
import time
import logging as logging
import loggingSetting  # 导入自定义的logging配置
logger = logging.getLogger(__name__)  # 生成logger实例


def setLogger():
    loggingSetting.load_my_logging_cfg('all.log')  # 在你程序文件的入口加载自定义logging配置
    # logging.basicConfig(level=logging.DEBUG,
    #                     format='%(asctime)s [%(levelname)s] [%(filename)s] [%(threadName)s] [line:%(lineno)d] %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S')


def get_list_dict(mysqldb):

    results = mysqldb.executequery("select namedict_name from namedict")

    list_dict = []

    for row in results:
        # list_dict.append(row[0].decode("utf8"))
        list_dict.append(str(row).decode("utf8"))

    list_dict.sort(cmp=None, key=None, reverse=False)

    return list_dict


def get_dic(list_dict):
    dic = {}

    for item in list_dict:
        dic[item] = 1

    return dic


def index_range(list, item):
    #     list要求是已排序的
    length = len(list)
    result = {}
    if item < list[0] or item > list[len(list)-1]:
        result["error"] = True
    else:
        for i in range(length/1000, -1, -1):
            if item >= list[i*1000]:
                branch = i*1000
                # logging.debug("branch="+str(branch))
                break

        for i in range(branch, length):
            if list[i] >= item:
                result["begin"] = i
                result["end"] = i
                # logging.debug("result[\"begin\"]="+str(result["begin"]))
                break

        for i in range(result["begin"], length):
            if item < list[i]:
                result["end"] = i
                # logging.debug("result[\"end\"]="+str(result["end"]))
    return result


def isexist(name, dic, list_dict):
    pass

    result = []

    if dic.get(name):
        result.append(name)
    else:
        pass

        range_result = index_range(list_dict, name)

        if range_result.get("error"):
            pass
        else:
            for i in range(range_result["begin"], range_result["end"]+1):
                #                 logging.debug("name="+name)
                #                 logging.debug("listname="+list_dict[i][0])
                if re.match(name+".*", list_dict[i]):
                    #                     logging.debug("name="+name)
                    #                     logging.debug("listname="+list_dict[i][0])
                    result.append(list_dict[i])

    return result


def div_word(name, dic, list_dict):
    divlist = []

    while len(name) >= 2:
        match_flag = 0
        # logging.debug("name:"+name)
        for i in range(2, len(name)+1):
            result = []
            result = isexist(name[0:i], dic, list_dict)
        # logging.debug("test name:"+name[0:i])
            if len(result) > 0:
                pass
                match_flag = 1
                previous = result
            else:
                if match_flag == 1:
                    # logging.debug("div name1:"+name[0:i-1])
                    divlist.append(previous)
                    # logging.debug(previous)
                    name = name[i-1:]
                    # logging.debug("new name:"+name)
                    break

            if i == len(name) and len(result) > 0:
                # logging.debug("div name2:"+name[0:i])
                divlist.append(result)
                name = name[i:]
            elif i == len(name):
                name = name[1:]
    return divlist


def get_fullname_list(mysqldb):
    strsql = "select village_name from new_village;"

    results = mysqldb.executequery(strsql)

    fullname_list = []

    for row in results:
        # fullname_list.append(row[0].decode("utf8"))
        fullname_list.append(str(row).decode("utf8"))

    return fullname_list


def get_fullindex(fullname_list):
    fullindex = {}

    for i in range(0, len(fullname_list)):
        split_list = fullname_list[i].split("-")
        for item in split_list:
            if fullindex.get(item):
                fullindex[item].add(i)
            else:
                fullindex[item] = set()
                fullindex[item].add(i)

    return fullindex


def main():

    begin = time.time()

    # mysqldb=MySQLHelper("dbaadmin","123456","172.16.2.7","3306","spider")
    # mysqldb.connect()
    mysqldb = MySQLHelper("localhost", "root", "001230")
    mysqldb.setDB("address_test")

    list_dict = get_list_dict(mysqldb)
    dic = get_dic(list_dict)

    fullname_list = get_fullname_list(mysqldb)
    fullindex = get_fullindex(fullname_list)

    load_data_time = round((time.time()-begin), 2)
    #加载数据耗时
    logger.info("Loading data takes time: "+str(load_data_time))
    logger.info("==============================================")

    name = u"无极县东侯坊乡南池阳村助农点"
    divlist = div_word(name, dic, list_dict)

    for x in itertools.product(*divlist):
        result = fullindex[x[0]]
#         logging.debug(x[0])
#         logging.debug(fullindex[x[0]])

        for i in range(1, len(x)):
            #             logging.info(x[i])
            #             logging.info(fullindex[x[i]])
            result = result & fullindex[x[i]]

        if len(result) > 0:
            for item in result:
                #                 logging.debug(item)
                logger.info("match name:"+fullname_list[item])

    match_time = round((time.time()-begin-load_data_time), 2)
    logger.info("名称匹配耗时"+str(match_time))

    logger.info("==============================================")
    logger.info("list_dict getsizeof:"+str(sys.getsizeof(list_dict)))
    logger.info("dic getsizeof:"+str(sys.getsizeof(dic)))
    logger.info("fullname_list getsizeof:"+str(sys.getsizeof(fullname_list)))
    logger.info("fullindex getsizeof:"+str(sys.getsizeof(fullindex)))

    mysqldb.close()


if __name__ == '__main__':
    pass

    setLogger()

    main()
