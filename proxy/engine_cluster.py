import threading

from kazoo.client import KazooClient
import tornado.httpclient as httpclient
import urllib

import logging
class Engine(object):

    def __init__(self,engineId,engineAddress):
        self.engineId=engineId
        self.engineAddress=engineAddress
        #self.sessionHandle=self.loadSessionHandle()

    post_data=urllib.urlencode({
                'action':'connect',
                'userID':'admin',
                'password':'Se4tMaQCi9gr0Q2usp7P56Sk5vM='
               })

    #def getSessionHandle(self):
    #    return self.sessionHandle

    #def loadSessionHandle(self):
    ##    request=httpclient.HTTPRequest(url="http://"+self.engineAddress+"/yawl/ib",
      #                                 method="POST",
      #                                 body=self.post_data,
        #                               )
       # client=httpclient.HTTPClient()

        #response=client.fetch(request)
        #return response.body




path="/engine"
zk_address='192.168.239.128:2181'
zk = KazooClient(zk_address)



engineMap={}

@zk.ChildrenWatch(path+"/")
def watch_children(engines):
    newMap={}
    for engine in engines:
        prefix=path+"/"
        if zk.exists(prefix+engine):
            data,stat=zk.get(prefix+engine)
            newMap[engine]=Engine(engine,data)
    global engineMap
    engineMap=newMap
    print engineMap


zk.start()
if not zk.exists(path):
    zk.create(path,'0',makepath=True)
#watch_children(zk.get_children(path))


def getEngineAddress(engineId):

    engine = engineMap[engineId]

    if engine:
        return engine.engineAddress
    return engine

def getEngineSessionHandle(engineId):

    engine=engineMap[engineId]

    return engine.getSessionHandle()




