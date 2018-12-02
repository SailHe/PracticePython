import requests
import re
import time
# 当前时间
local = time.strftime("%Y.%m.%d")
url = 'http://cn.bing.com/'
# 连接url
con = requests.get(url)
# 得到的网页
content = con.text
# 用于查询网页中的图片url的筛选正则表达式
reg = r"(az/hprichbg/rb/.*?.jpg)"
# 匹配正则表达式 得到图片url
a = re.findall(reg, content, re.S)[0]
print(a)
picUrl = url + a
# 获取图片内容
read = requests.get(picUrl)
# 打开一个格式化名称的文件流
f = open('%s.jpg' % local, 'wb')
# 写入图片文件
f.write(read.content)
# 关闭文件流
f.close()