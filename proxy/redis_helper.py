import redis

host='192.168.239.128'
port=6379
caseEnginePrefix="caseEngine:"



r = redis.StrictRedis(host,port,db=0)

def getEngineIdByCaseId(caseId):
    key=caseEnginePrefix+caseId
    return r.get(key)



