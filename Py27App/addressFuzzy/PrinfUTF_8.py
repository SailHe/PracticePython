#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys_encoding = sys.getfilesystemencoding()
def printcn(msg):
    print(msg.decode('utf-8').encode(sys_encoding))


if __name__ == "__main__":
    #兼容中文字符打印
    reload(sys)
    sys.setdefaultencoding("utf-8")
    print("测试一下")
    printcn("测试一下")
