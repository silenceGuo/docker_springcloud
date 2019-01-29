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
import configparser
#reload(sys)
# sys.setdefaultencoding('utf-8')
# sys.set

class service():
    def __init__(self, serverName, env, conf):
        self.severName = serverName
        # self.env = env
        self.conf = conf
        self.serverDict = self.getconf()
        print(self.serverDict)

    def execsh(self, cmd):
        try:
            print ("exec ssh command: %s" % cmd)
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except Exception as e:
           print(e)
           sys.exit(1)
        return p.communicate()

    def confCheck(self, cf, section, option):
        if not cf.options(section):
            print("no section: %s in conf file" % section)
            sys.exit()
        try:
            options = cf.get(section, option)
        except configparser.NoOptionError:
            print("no option in conf %s " % option)
            sys.exit()
        if not options:
            print ("options:%s is null in section:%s" % (option, section))
            return False
        else:
            return True

    def getconf(self):
        if not os.path.exists(self.conf):
            sys.exit(1)
        cf = configparser.ConfigParser()
        try:
            cf.read(self.conf)
        except configparser.ParsingError as e:
            print (e)
            print ("请检查服务配置文件： %s" % self.conf)
            sys.exit(1)
        serverNameDict = {}
        optinsDict = {}
        for serverName in cf.sections():
            # print 'serverName:%s' % serverName
            for optins in cf.options(serverName):
                # 取服务名下的对应的配置和参数
                if not self.confCheck(cf, serverName, optins):
                    sys.exit(1)
                value = cf.get(serverName, optins)
                optinsDict[optins] = value
            serverNameDict[serverName] = optinsDict
            optinsDict = {}
        return serverNameDict

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
            sys.exit(1)

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
        createService = "docker service create " \
                        "--replicas 1 " \
                        "--update-delay 10s " \
                        "--update-failure-action continue " \
                        "--network tomcat_net " \
                        "--constraint node.hostname!=centos1 " \
                        "--name %s  " \
                        "-p %s:8080 %s" % (self.serverName, port, imagesName)

    def updataServer(self):
        print("%s updataServer" % self.severName)

    def startServer(self,env):
        print("%s startServer on %s" % (self.severName,env))


    def stopServer(self):
        print("%s stopServer" % self.severName)

    def restartServer(self):
        print ("%s restart" % self.severName)

    def rollBackServer(self):
        print ("%s rollback" % self.severName)

class projet():
    def __init__(self, serverName):
        self.serverName = serverName



if __name__ == "__main__":

    # D = Docker("tomcat")
    D = Docker("springcloud", "es", "server.conf")
    # s = D.readconf()
    # s = D.startServer("ss")

    # print (s)
    # D.build()
    # D.tag()
    # print (D.execsh("docker build -t tt ."))
    # D.pull()
    # D.push()
    # D.createServer()