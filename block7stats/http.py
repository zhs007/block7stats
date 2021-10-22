import requests

# getUserStats
def getUserStats(cfg, uid):
    r = requests.get('{}/userstats?token={}&uid={}'.format(cfg['urlroot'], cfg['token'], uid))
    return r.json()

# getStats
def getStats(cfg):
    r = requests.get('{}/stats?token={}'.format(cfg['urlroot'], cfg['token']))
    return r.json()    