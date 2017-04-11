import uuid
sessionMap={}

def connect(userid):
    if not sessionMap[userid]:
        sessionMap[userid]=uuid.uuid4()
        return sessionMap[userid]

def replaceSessionHandle(str,sessionHandle):
    import re
    return re.subn(pattern='sessionHandle=.*&',
                   repl='sessionHandle='+sessionHandle+'&',
                   string=str)