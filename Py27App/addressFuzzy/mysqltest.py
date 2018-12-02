#--encoding:utf-8
#
from MySQLHelper import *
 
helper=MySQLHelper("localhost","root","001230")
helper.setDB("lost_and_found")
sql="select * from sys_user"
#rows=helper.queryAll(sql)
rows=helper.executequery(sql)
for row in rows:
    print row['user_id'],str(row['user_username']).decode("utf-8"),row['user_birthday']
 
# dataSource={"name":"汤姆克路斯".decode("gbk").encode("utf-8"),"birthday":"1992-03-12"}
# helper.insert("users", dataSource)
# print helper.getLastInsertRowId()
 
 
# pData={"birthday":"2005-05-05 18:32:23"}
# whereData={"name":"Jack Tang"}
# helper.update("users", pData, whereData)
