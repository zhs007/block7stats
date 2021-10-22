# -*- coding:utf-8 -*-
from datetime import datetime

# 解析时间字符串，2021-10-13_10:01:48
def parseTime(str):
    if str == '':
        return None
    
    return datetime.strptime(str, '%Y-%m-%d_%H:%M:%S')

# 计算时间差，返回整数小时差
def getTimeOffsetHours(timeNow, timeStart):
    if timeStart == None:
        return -1
    
    return int((timeNow.timestamp() - timeStart.timestamp()) / 60 / 60)


# form timestamp
def fromTimestamp(ts):
    return datetime.fromtimestamp(ts)