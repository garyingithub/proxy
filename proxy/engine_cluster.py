import threading

from kazoo.client import KazooClient
import logging

path="/engine"
zk_address='127.0.0.1:2181'
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
    engineMap=newMap
    print engineMap


zk.start()


class Engine(object):

    def __init__(self,engineId,engineAddress):
        self.engineId=engineId
        self.engineAddress=engineAddress


def getEngineAddress(engineId):

    engine = engineMap[engineId]

    if engine:
        return engine.engineAddress
    return engine




