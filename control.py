#!/usr/bin/env python
#！-*-coding:utf-8 -*-
#!@Date    : 2019/1/24 0024 下午 16:40
#!@Author : Damon.guo
#!@File   : control.py
# -*- coding:utf-8 -*-
# coding=utf-8
# encoding: utf-8

import sys
import os
from subprocess import PIPE, Popen
#reload(sys)
# sys.setdefaultencoding('utf-8')
# sys.set

class Docker():
    def __init__(self, serverName):
        self.severName = serverName

    def execsh(self,cmd):
        try:
            print ("exec ssh command: %s" % cmd)
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except Exception as e:
           print(e)
           sys.exit()
        return p.communicate()

    def build(self):
        print("%s building" % self.severName)
        os.chdir(self.severName)  # 根据服务名切换工作目录
        buildImages = "docker build -t 10.0.0.133:5000/%s ." % (self.severName)
        stdout, stderr = self.execsh(buildImages)

        if stdout:
            print ("build images sucess:%s " % self.severName)
            print (stdout)
            return True
        else:
            print (stderr)
            print ("build images fail:%s " % self.severName)
            return False
            sys.exit()


    def pull(self):
        print("%s pull" % self.severName)

    def tag(self):
        print("%s tag" % self.severName)
        tagcmd = "docker tag {0} 10.0.1.133:50001/{0}".format(self.severName)
        stdout, stderr = self.execsh(tagcmd)
        print (stdout)
        print (stderr)
        if stdout:
            print("tag images sucess:%s " % self.severName)
            print(stdout)
            return True
        else:
            print(stderr)
            print("tag images fail:%s " % self.severName)
            # return False
            # sys.exit()
    def push(self):
        print("%s push" % self.severName)

    def checkService(self):
        checkServiceCMD = "docker service inspect %s" % self.serverName
        checkStdout, checkStderr = self.execsh(checkServiceCMD)

        if (checkStdout, checkStderr):
            return True
        else:
            return False

    def createServer(self):
        print("%s createServer" % self.severName)

    def updataServer(self):
        print("%s updataServer" % self.severName)

    def startServer(self):
        print("%s startServer" % self.severName)

    def stopServer(self):
        print("%s stopServer" % self.severName)

    def restartServer(self):
        print ("%s restart" % self.severName)

    def rollBackServer(self):
        print ("%s rollback" % self.severName)


if __name__ == "__main__":

    # D = Docker("tomcat")
    D = Docker("springcloud")

    D.build()
    # D.tag()
    # print (D.execsh("docker build -t tt ."))
    # D.pull()
    # D.push()
    # D.createServer()