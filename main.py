# -*- coding:utf-8 -*-
import block7stats
import pandas as pd
from datetime import timedelta, date

cfg = block7stats.loadConfig('./cfg/config.yaml')
stats = block7stats.getStats(cfg)

print('uid is in range({}, {})'.format(cfg['startUID'], stats['user']['latestuserid']))

lstui, lststages, lstdaystats, lsthomescene = block7stats.analyzeUserStats(cfg, cfg['startUID'], stats['user']['latestuserid'], None)
# for uid in range(cfg['startUID'], stats['user']['latestuserid']):
#     ustats = block7stats.getUserStats(cfg, uid)
#     print('{} is ok.'.format(uid))

df = pd.DataFrame(lstui)
df['createTime'] = pd.to_datetime(df['createTime'])

df1 = pd.DataFrame(lststages)

block7stats.genStagesStats(df1, './output/stagestats.html')

curday = cfg['startDay']
while curday <= date.today():
    curdaystr = curday.strftime('%Y-%m-%d')
    print('curday is {}'.format(curdaystr))

    lstui, lststages, lstdaystats, lsthomescene = block7stats.analyzeUserStats(cfg, cfg['startUID'], stats['user']['latestuserid'], curdaystr)

    df = pd.DataFrame(lstui)
    df['createTime'] = pd.to_datetime(df['createTime'])

    df1 = pd.DataFrame(lststages)

    block7stats.genStagesStats(df1, './output/stagestats.{}.html'.format(curdaystr))

    curday = curday + timedelta(days=1)
