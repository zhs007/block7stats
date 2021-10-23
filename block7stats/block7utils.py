# -*- coding:utf-8 -*-
from block7stats.http import getUserStats
from block7stats.utils import parseTime, getTimeOffsetHours, fromTimestamp
from datetime import datetime

# 计算平均关卡星星，需要跳过5的倍数的关卡
def countAvgUserStageStars(levelArr):
    if levelArr == None:
        return 0
    
    totalstars = 0
    stagenums = 0
    
    for key in levelArr.keys():
        if int(key) % 5 != 0:
            totalstars = totalstars + int(levelArr[key])
            stagenums = stagenums + 1
    
    if stagenums > 0:
        return totalstars / stagenums
    
    return 0

# 计算平均关卡星星，需要跳过5的倍数的关卡
def analyzeAvgStageStars(lststages, levelArr):
    if levelArr == None:
        return 
    
    for key in levelArr.keys():
        if int(key) % 5 != 0:
            addStageStar(lststages, int(key), int(levelArr[key]))

            
# 计算下一关的流失率
def countNextStage(lststages, stage, curnums):
    if curnums > 0:
        for s in lststages:
            if s['stage'] == stage + 1:
                s['lostper'] = (curnums - s['totalusers']) / curnums
                
                if s['lostper'] < 0:
                    s['lostper'] = 0

                return
    else:
        s['lostper'] = 0
        
# 获取前一关的游戏人数       
def getPreStageTotalUsers(lststages, stage):
    for s in lststages:
        if s['stage'] == stage - 1:
            return s['totalusers']
            
    return 0

# new stage stats data
def newStageData(stage):
    ss = {
        'stage': stage,
        'totalwinper': 0,
        'totalusers': 0,
        'winper': 0,
        'totalClickNums': 0,
        'avgClickNums': 0,
        'totalAvgClickTime': 0,
        'avgClickTime': 0,
        'totalnums': 0,
        'totalWinClickNums': 0,
        'avgWinClickNums': 0,
        'totalWinAvgClickTime': 0,
        'avgWinClickTime': 0,
        'totalWinNums': 0,
        'totalLoseClickNums': 0,
        'avgLoseClickNums': 0,
        'totalLoseAvgClickTime': 0,
        'avgLoseClickTime': 0,
        'totalLoseNums': 0,
        'stayUsers': 0,
        'stayUsersPer': 0,    
        'avgLoseProgress': 0,
        'totalGameNums': 0,
        'totalGameWinNums': 0,
        'gameWinPer': 0,
        'totalStars': 0,
        'totalStarUserNums': 0,
        'avgStars': 0,
    }
    
    return ss


# 新增加一个玩家关卡统计
def addStageStar(lststages, stage, stars):
    for s in lststages:
        if s['stage'] == stage:
            s['totalStars'] = s['totalStars'] + stars
            s['totalStarUserNums'] = s['totalStarUserNums'] + 1
            s['avgStars'] = s['totalStars'] / s['totalStarUserNums']
            
            return
    
    ss = newStageData(stage)
    
    ss['totalStars'] = ss['totalStars'] + stars
    ss['totalStarUserNums'] = ss['totalStarUserNums'] + 1
    ss['avgStars'] = ss['totalStars'] / ss['totalStarUserNums']
    
    lststages.append(ss)


# 新增加一个玩家关卡统计
def addUserStages(lststages, stage, winper, winnums, totalnums):
    for s in lststages:
        if s['stage'] == stage:
            s['totalGameWinNums'] = s['totalGameWinNums'] + winnums
            s['totalGameNums'] = s['totalGameNums'] + totalnums
            if s['totalGameNums'] > 0:
                s['gameWinPer'] = s['totalGameWinNums'] / s['totalGameNums']
            
            s['totalwinper'] = s['totalwinper'] + winper
            s['totalusers'] = s['totalusers'] + 1
            s['winper'] = s['totalwinper'] / s['totalusers']
            
            ptnums = getPreStageTotalUsers(lststages, stage)
            if ptnums != 0:
                s['lostper'] = (ptnums - s['totalusers'])  / ptnums
                
                if s['lostper'] < 0:
                    s['lostper'] = 0
            else:
                s['lostper'] = 0
            
            countNextStage(lststages, stage, s['totalusers'])
            
            return
    
    ss = newStageData(stage)
    
    ss['totalwinper'] = winper
    ss['totalusers'] = 1
    ss['winper'] = winper
    
    ss['totalGameWinNums'] = ss['totalGameWinNums'] + winnums
    ss['totalGameNums'] = ss['totalGameNums'] + totalnums
    if ss['totalGameNums'] > 0:
        ss['gameWinPer'] = ss['totalGameWinNums'] / ss['totalGameNums']    
    
    lststages.append(ss)
    
    ss['lostper'] = (getPreStageTotalUsers(lststages, stage) - ss['totalusers']) / ss['totalusers']        
    countNextStage(lststages, stage, ss['totalusers'])
    
    
def procUserStayStage(lststages, us):
    for s in lststages:
        if s['stage'] == int(us['user']['level']):
            s['stayUsers'] = s['stayUsers'] + 1
            
            if s['totalusers'] > 0:
                s['stayUsersPer'] = s['stayUsers'] / s['totalusers']
            
            return


# 分析玩家历史数据
def analyzeUserStageHistory(ui, lststages, stage, stageHistory):
    for s in lststages:
        if s['stage'] == stage:
            s['totalnums'] = s['totalnums'] + 1
            
            s['totalClickNums'] = s['totalClickNums'] + stageHistory['clickNums']
            s['avgClickNums'] = s['totalClickNums'] / s['totalnums'] 
            
            s['totalAvgClickTime'] = s['totalAvgClickTime'] + stageHistory['avgClickTime']
            s['avgClickTime'] = s['totalAvgClickTime'] / s['totalnums']
            
            ui['totalHistoryNums'] = ui['totalHistoryNums'] + 1
            ui['totalAvgClickTime'] = ui['totalAvgClickTime'] + stageHistory['avgClickTime']
            ui['avgClickTime'] = ui['totalAvgClickTime'] / ui['totalHistoryNums']
            
            if stageHistory['gamestate'] == 1:
                s['totalWinNums'] = s['totalWinNums'] + 1

                s['totalWinClickNums'] = s['totalWinClickNums'] + stageHistory['clickNums']
                s['avgWinClickNums'] = s['totalWinClickNums'] / s['totalWinNums'] 

                s['totalWinAvgClickTime'] = s['totalWinAvgClickTime'] + stageHistory['avgClickTime']
                s['avgWinClickTime'] = s['totalWinAvgClickTime'] / s['totalWinNums']                
            else:
                s['totalLoseNums'] = s['totalLoseNums'] + 1

                s['totalLoseClickNums'] = s['totalLoseClickNums'] + stageHistory['clickNums']
                s['avgLoseClickNums'] = s['totalLoseClickNums'] / s['totalLoseNums'] 

                s['totalLoseAvgClickTime'] = s['totalLoseAvgClickTime'] + stageHistory['avgClickTime']
                s['avgLoseClickTime'] = s['totalLoseAvgClickTime'] / s['totalLoseNums']
                
            if s['avgWinClickNums'] > 0:
                s['avgLoseProgress'] = s['avgLoseClickNums'] / s['avgWinClickNums']
                
            return
            
    
# 分析玩家关卡数据    
def analyzeUserStages(ui, lststages, lstdaystats, stages):
    if stages == None:
        ui['stagenums'] = 0
        
        return 
    
    nums = 0
    for key in stages.keys():
        if len(stages[key]['historys']) > 0:
            addUserStages(lststages, int(key), stages[key]['winnums'] / len(stages[key]['historys']), 
                          stages[key]['winnums'], len(stages[key]['historys']))
            nums = nums + len(stages[key]['historys'])
            
            for sh in stages[key]['historys']:
                analyzeUserStageHistory(ui, lststages, int(key), sh)
                onUserStage(lstdaystats, ui['uid'], ui['createTime'], fromTimestamp(sh['ts']))
                
            
    ui['stagenums'] = nums
        
    return

# 是否是一个有效的用户
def isValidUserStatsData(usret, regDay):
    if usret == None:
        return False
    
    if usret['user'] == None:
        return False
    
    # if g_isLevel8:
    #     if usret['user']['level'] != 8:
    #         return False
        
    # if g_isLevel8Ex:
    #     if usret['user']['level'] != 8 and usret['user']['level'] != 9:
    #         return False
        
    # if g_isLevel9:
    #     if usret['user']['level'] != 9:
    #         return False   
        
    # if g_isLevel25More:
    #     if usret['user']['level'] < 25:
    #         return False           
        
    # if g_isRegDay:
    #     if usret['user']['createTime'].find(g_regDay) != 0:
    #         return False
    if regDay != None:
        if usret['user']['createTime'].find(regDay) != 0:
            return False
    
    if usret['user']['stages'] == None:
        return False
    
    for key in usret['user']['stages'].keys():
        return True
    
    return False

def newDayStats(dt):
    ds = {
        'date': dt,
        'title': '{}-{}-{}'.format(dt.year, dt.month, dt.day),
        'uids': [],
        'newusers': 0,
        'dates': [],
        'days': [],
        'aliveusers': [],
        'aliveuids': [],        
    }
    
    return ds

# 新增一天
def addDayInDayStats(lstdaystats, uid, dt):
    for ds in lstdaystats:
        if ds['date'].year == dt.year and ds['date'].month == dt.month and ds['date'].day == dt.day:
            ds['uids'].append(uid)
            ds['newusers'] = len(ds['uids'])
            
            return 
    
    ds = newDayStats(dt)
    
    ds['uids'].append(uid)
    ds['newusers'] = len(ds['uids'])
    
    lstdaystats.append(ds)
    

def onUserStageDS(ds, uid, gamedt):
    for i in range(len(ds['days'])):
        if ds['dates'][i].year == gamedt.year and ds['dates'][i].month == gamedt.month and ds['dates'][i].day == gamedt.day:
            for cuid in ds['aliveuids'][i]:
                if cuid == uid:
                    return
            
            ds['aliveuids'][i].append(uid)
            ds['aliveusers'][i] = len(ds['aliveuids'][i])
            
            return 
        
    ds['dates'].append(gamedt)
    ds['days'].append('{}-{}-{}'.format(gamedt.year, gamedt.month, gamedt.day))
    ds['aliveuids'].append([uid])
    ds['aliveusers'].append(1)   
    
    return
    
def onUserStage(lstdaystats, uid, newdt, gamedt):
    if newdt.timestamp() < gamedt.timestamp():
        for ds in lstdaystats:
            if ds['date'].year == newdt.year and ds['date'].month == newdt.month and ds['date'].day == newdt.day:
                
                onUserStageDS(ds, uid, gamedt)
                
                return
    

def addHomeScene(lsthomescene, itemid):
    for v in lsthomescene:
        if v['id'] == itemid:
            v['nums'] = v['nums'] + 1
            
            return
        
    vv = {
        'id': itemid,
        'nums': 1,
    }
    
    lsthomescene.append(vv)
    
    
def analyzeHomeScene(lsthomescene, homescene):
    if homescene == None:
        return 
    
    for v in homescene:
        addHomeScene(lsthomescene, v)
    
# 分析用户数据
def analyzeUserStats(cfg, startUID, endUID, regDay):
    lstui = []
    lststages = []
    lstdaystats = []
    lsthomescene = []
    timeNow = datetime.now()
    
    for uid in range(startUID, endUID):
        print('cur uid is {}'.format(uid))

        cui = getUserStats(cfg, uid)
        if isValidUserStatsData(cui, regDay):
            ui = {
                'uid': uid, 
                'coin': int(cui['user']['coin']),
                'level': int(cui['user']['level']),
                'createTime': parseTime(cui['user']['createTime']),
                'lastTime': parseTime(cui['user']['lastLoginTime']),
                'avgStars': countAvgUserStageStars(cui['user']['levelarr']),
                'ip': cui['user']['ip'],
                'totalAvgClickTime': 0,
                'avgClickTime': 0,
                'totalHistoryNums': 0,
            }
            
            addDayInDayStats(lstdaystats, uid, ui['createTime'])

            if ui['lastTime'] == None:
                ui['lastTime'] = ui['createTime']

            ui['offlineHours'] = getTimeOffsetHours(timeNow, ui['lastTime'])
            ui['aliveHours'] = getTimeOffsetHours(ui['lastTime'], ui['createTime'])

            analyzeUserStages(ui, lststages, lstdaystats, cui['user']['stages'])

            procUserStayStage(lststages, cui)
            
            analyzeAvgStageStars(lststages, cui['user']['levelarr'])
            
            analyzeHomeScene(lsthomescene, cui['user']['homeScene'])

            lstui.append(ui)
    
    return lstui, lststages, lstdaystats, lsthomescene