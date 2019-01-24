#!/usr/bin/env python
#！-*-coding:utf-8 -*-
#!@Date    : 2019/1/24 0024 下午 16:40
#!@Author : Damon.guo
#!@File   : control.py.py

class Docker():
    def __init__(self, serverName):
        self.severName = serverName
    def build(self):
        print ("%s building" % self.severName)

        pass
    def pull(self):
        print("%s pull" % self.severName)
        pass
    def push(self):
        print("%s push" % self.severName)
        pass
    def createServer(self):
        print("%s createServer" % self.severName)
        pass

D = Docker("SS")
D.build()
D.pull()
D.push()
D.createServer()