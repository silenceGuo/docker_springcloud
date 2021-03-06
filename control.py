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
# import OptionParser
from optparse import OptionParser
import shutil
import datetime
#reload(sys)
# # sys.setdefaultencoding('utf-8')
# # sys.set

class service( ):
    def __init__(self, serverName, brancheName, env, version, serverDict):
        self.serverName = serverName
        self.env = env
        self.version = version
        self.brancheName = brancheName
        self.serverDict = serverDict

    def execsh(self, cmd):
        try:
            print ("exec ssh command: %s" % cmd)
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except Exception as e:
           print(e)
           sys.exit(1)
        stdout, stderr = p.communicate()
        # 需要转换byte to str
        stdout = stdout.decode()
        stderr = stderr.decode()
        return (stdout, stderr)

    def init(self):
        # 初始化 本地打包构建git仓库
        serverNameDict = self.serverDict[self.serverName]
        print("master install:%s" % self.serverName)
        builddir = serverNameDict["builddir"]
        if not os.path.exists(builddir):
            os.makedirs(builddir)
        try:
            gitUrl = serverNameDict["giturl"]
        except:
            return False

        if not os.path.exists(builddir):
            os.mkdir(builddir)
        os.chdir(builddir)
        print ("部署路径：", os.getcwd())
        stdout, stderr = self.execsh("git status .")
        if stdout:
            print("out：\n%s" % stdout)
            print("当前目录：%s,已经存在git仓库请检查!" % builddir)
            return True
        if stderr:
            print("没有git仓库，下一步")
            print("out：%s" % stderr)

        print("初始化本地仓库")
        self.ReturnExec("git init")

        print("本地git仓库当前项目认证")
        config_cmd = "git config --local credential.helper store"
        self.ReturnExec(config_cmd)

        print("拉取代码")
        pull_cmd = "git pull %s" % gitUrl
        self.ReturnExec(pull_cmd)

        print("添加远程仓库地址")
        add_remote_cmd = "git remote add origin %s" % gitUrl
        self.ReturnExec(add_remote_cmd)

        print("获取分支")
        fetch_cmd = "git fetch"
        self.ReturnExec(fetch_cmd)

        print("关联本地master分支与远程master")
        upstream_cmd = "git branch --set-upstream-to=origin/master master"
        self.ReturnExec(upstream_cmd)

        print("获取 最新master分支")
        pull_m_cmd = "git pull"
        self.ReturnExec(pull_m_cmd)

    def gitupdate(self):
        serverNameDict = self.serverDict[self.serverName]

        buildDir = serverNameDict["builddir"]
        os.chdir(buildDir)
        pull_m_cmd = "sudo git pull"
        stdout, stderr = self.execsh(pull_m_cmd)
        print (stdout)
        print (stderr)
        os.chdir(buildDir)
        if not self.checkMaster():
            checkout_m_cmd = "git checkout %s" % self.brancheName
            print("切换至%s分支" % self.brancheName)
            self.ReturnExec(checkout_m_cmd)

        print("获取 最新%s分支" % self.brancheName)
        pull_m_cmd = "git pull"
        stdout, stderr = self.execsh(pull_m_cmd)
        # 判断是否有git 执行错误
        return self.isNoErr(stdout, stderr)

    # jar 文件mavn构建
    def buildMaven(self):

        serverNameDict = self.serverDict[self.serverName]
        buildDir = serverNameDict["builddir"]

        if not self.gitupdate():
            print("git update is err")
            sys.exit(1)

        os.chdir(buildDir)
        print("workdir : %s" % os.getcwd())

        cmd = "%(mvn)s clean && %(mvn)s install -Dmaven.test.skip=true -P dev" % {"mvn": mvn}
        print("构建服务：%s" % self.serverName)
        stdout, stderr = self.execsh(cmd)

        if "BUILD FAILURE" in stdout:
            print("stdout:%s" % stdout)
            return False
        elif "BUILD FAILURE" in stderr:
            print("stderr:%s" % stderr)
            return False
        else:
            if stdout:
                print(stdout)
            if stderr:
                print(stderr)
            return True

    def ReturnExec(self,cmd):
        stdout, stderr = self.execsh(cmd)
        if stdout:
            print (80 * "#")
            print ("out:%s " % stdout)
        if stderr:
            print(80 * "#")
            print("err:%s" % stderr)

    def checkMaster(self):
        # 获取项目分支是否为master
        cmd = "git branch"
        stdout, stderr = self.execsh(cmd)
        print("out:", stdout)

        branch_list = [i.strip() for i in stdout.split("\n") if i]
        branchName_str = "* %s" % self.brancheName
        if branchName_str in branch_list:
            print("%s 分支" % self.brancheName)
            return True
        print("err", stderr)
        return False

    def isNoErr(self,stdout, stderr):
        # 有错误返回false
        errlist = ["error", "fatal", "error"]
        if not "error" or "fatal" in stdout:
            print("stdout:%s" % stdout)
            return False
        elif not "error" or "fatal" in stderr:
            print("stderr:%s" % stderr)
            return False
        else:
            print("stdout:%s" % stdout)
            print("stderr:%s" % stderr)
            return True

    def copyFile(self):
        serverNameDict = self.serverDict[self.serverName]
        deploydir = serverNameDict["deploydir"]
        jar = serverNameDict["jar"]
        jarName = jar.split("/")[-1]
        if not os.path.exists(jar):
            print ("%s is not exists" % jar)
            sys.exit(1)
        destjar = os.path.join(deploydir, jarName)
        try:
            print("copy %s to %s " % (jar, destjar))
            shutil.copyfile(jar,os.path.join(deploydir,jarName))
        except Exception as e:
            print (e)
            print ("copy %s to %s fail" %(jar,destjar))
            sys.exit(1)
        if not os.path.exists(destjar):
            print("copy %s to %s fail" % (jar, destjar))
        print("copy %s to %s sucess " % (jar, destjar))

    def buildImage(self):
        serverNameDict = self.serverDict[self.serverName]
        deploydir = serverNameDict["deploydir"]
        jar = serverNameDict["jar"]
        dockerport = serverNameDict["dockerport"]
        jarName = jar.split("/")[-1]

        # 拷贝 构建好的jar 包 到部署目录用于 构建镜像
        self.copyFile()
        # 切换工作目录
        os.chdir(deploydir)
        buildImage = "docker build -t {repositoryUrl}/{serverName}-{env}:{version} " \
                      "--build-arg envName={env} " \
                      "--build-arg dockerport={dockerport} " \
                      "--build-arg jarName={jarName} .".format(repositoryUrl=repositoryUrl,
                                                         serverName=self.serverName,
                                                         env=self.env,
                                                         version=self.version,
                                                         dockerport=dockerport,
                                                         jarName=jarName)

        stdout, stderr = self.execsh(buildImage)

        if stdout:
            print ("build images sucess:%s " % self.serverName)
            print (stdout)
            return True
        else:
            print (stderr)
            print ("build images fail:%s " % self.serverName)
            return False
            sys.exit(1)

    def pullimage(self):
        imagename = "{0}/{1}-{2}:{3}".format(repositoryUrl, self.serverName, self.env, self.version)
        print("%s pull" % imagename)

        pushImage = "docker pull {0}".format(imagename)
        stdout, stderr = self.execsh(pushImage)
        if stdout:
            print ("pull images sucess:%s " % imagename)
            print (stdout)
            return True
        else:
            print (stderr)
            print ("pull images fail:%s " % imagename)
            return False
            sys.exit(1)

    def tag(self):
        print("%s tag" % self.serverName)
        tagcmd = "docker tag {0} {1}/{0}".format(self.serverName, repositoryUrl)
        print (tagcmd)
        stdout, stderr = self.execsh(tagcmd)
        print (stdout)
        print (stderr)
        if stdout:
            print("tag images sucess:%s " % self.serverName)
            print(stdout)
            return True
        else:
            print(stderr)
            print("tag images fail:%s " % self.serverName)
            # return False
            # sys.exit()

    def pushimage(self):
        imagename = "{0}/{1}-{2}:{3}".format(repositoryUrl, self.serverName, self.env, self.version)
        print("%s pull" % imagename)

        pushImage = "docker push {0}".format(imagename)
        stdout, stderr = self.execsh(pushImage)
        if stdout:
            print("push images sucess:%s " % imagename)
            print(stdout)
            return True
        else:
            print(stderr)
            print("push images fail:%s " % imagename)
            return False
            sys.exit(1)


    def checkService(self):
        checkServiceCMD = "docker service inspect %s" % self.serverName
        checkStdout, checkStderr = self.execsh(checkServiceCMD)
        print (checkStdout)
        print (checkStderr)
        if checkStdout:
            return True
        else:
            return False

    def printOutErr(self,stdout, stderr):
        if stdout and len(stdout) > 3:
            print("stdout >>>%s" % stdout)
            return True
        if stderr:
            print("stderr >>>%s " % stderr)
            return False

    # 检查 覆盖网络，创建覆盖网络
    def createNetwork(self,networkName):
        creatNetworkCmd = "docker network create -d overlay %s" % networkName
        checkNetworkCmd = "docker network inspect %s " % networkName
        checkNetworkStdout, checkNetworkStderr = self.execsh(checkNetworkCmd)

        if self.printOutErr(checkNetworkStdout, checkNetworkStderr):
            return True
        else:
            checkStdout, checkStderr = self.execsh(creatNetworkCmd)
            print ("create network;%s" % networkName)
            if self.printOutErr(checkStdout, checkStderr):
                return True
            else:
                return False

    def createServer(self):
        if not self.checkService():
            print ("service:%s is exists" % self.serverName)
            sys.exit(1)
        imagename = "{0}/{1}-{2}:{3}".format(repositoryUrl, self.serverName, self.env, self.version)
        serverNameDict = self.serverDict[self.serverName]
        hostport = serverNameDict["hostport"]

        dockerport = serverNameDict["dockerport"]
        replicas = serverNameDict["replicas"]
        network = serverNameDict["network"]
        if not self.createNetwork(network):
            print ("create network %s" % network)
        try:
            xmx = serverNameDict["xmx"]
        except:
            print("配置文件中为配置容器内存限制参数参数默认512m ")
            xmx = "512m"

        # if self.env == "":
        #     hostport = serverNameDict["hostport"]
        #     dockerport = serverNameDict["dockerport"]
        #     network = serverNameDict["network"]
        # elif self.env == "":
        #     hostport = serverNameDict["hostport"]
        #     dockerport = serverNameDict["dockerport"]
        #     network = serverNameDict["network"]
        # elif self.env == "test":
        #     pass
        # else:
        #     pass

        # 暂时未用，
        # if self.env == "test":
        #     nodelabel = serverNameDict["testlabel"]
        # if self.env == "dev":
        #     nodelabel = serverNameDict["devlabel"]
        # if self.env == "pro":
        #     nodelabel = serverNameDict["prolabel"]

        print("%s createServer" % self.serverName)
        createService = "docker service create " \
                        "--replicas {replicas} " \
                        "--mount type=volume,dst=/root/logger/{serverName} " \
                        "--update-delay 10s " \
                        "--update-failure-action continue " \
                        "--network {network} " \
                        "--container-label aliyun.logs.{serverName}=/root/logger/{serverName}/*.log " \
                        "--name {serverName} " \
                        "--limit-memory {xmx} " \
                        "-p {hostport}:{dockerport} {imagename} ".format(serverName=self.serverName,
                                                        network=network,
                                                        imagename=imagename,
                                                        dockerport=dockerport,
                                                        hostport=hostport,
                                                        replicas=replicas,
                                                        xmx=xmx)
        "--constraint node.labels.type=={label} "
        stdout, stderr = self.execsh(createService)
        print (stdout)
        print (stderr)

    def updataServer(self):

        print("%s updataServer" % self.serverName)
        imagename = "{0}/{1}-{2}:{3}".format(repositoryUrl, self.serverName, self.env, self.version)
        serverNameDict = self.serverDict[self.serverName]
        hostport = serverNameDict["hostport"]
        dockerport = serverNameDict["dockerport"]
        replicas = serverNameDict["replicas"]
        network = serverNameDict["network"]
        if not self.createNetwork(network):
            print("create network %s" % network)
        try:
            xmx = serverNameDict["xmx"]
        except:
            print("配置文件中为配置内存参数参数默认512m ")
            xmx = "512m"
        updateService = "docker service update " \
                        "--replicas {replicas} " \
                        "--limit-memory {xmx} " \
                        "--image {imagename} {serverName}".format(serverName=self.serverName,
                                               imagename=imagename,
                                               replicas=replicas,
                                               xmx=xmx)

        print("update service:%s" % self.serverName)
        updateStdout, updateStderr = self.execsh(updateService)
        if self.printOutErr(updateStdout, updateStderr):
            print("update service sucess:%s" % self.serverName)
            return True
        else:
            print("update service fail:%s" % self.serverName)
            return False

    def reomveServer(self):
        print("%s remove Server" % self.serverName)
        cmd = "docker service rm %s" % self.serverName
        removeStdout, removeStderr = self.execsh(cmd)
        if self.printOutErr(removeStdout, removeStderr):
            print("remove service sucess:%s" % self.serverName)
            return True
        else:
            print("remove service fail:%s" % self.serverName)
            return False

    def rollBackServer(self):
        print ("%s rollback 上个版本" % self.serverName)
        rollbackService = "docker service update --rollback %s" % self.serverName
        print("rollback service:%s" % self.serverName)
        rollbackupdateStdout, rollbackStderr = self.execsh(rollbackService)
        if self.printOutErr(rollbackupdateStdout, rollbackStderr):
            print("rollback service sucess :%s " % self.serverName)
        else:
            print("rollback service fail :%s " % self.serverName)
            sys.exit()

class Conf():
    def __init__(self, conf):
        self.conf = conf
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
            for optins in cf.options(serverName):
                # 取服务名下的对应的配置和参数
                if not self.confCheck(cf, serverName, optins):
                    sys.exit(1)
                value = cf.get(serverName, optins)
                optinsDict[optins] = value
            serverNameDict[serverName] = optinsDict
            optinsDict = {}
        return serverNameDict

def getOptions():
    # 作为镜像tag的以时间戳作为默认值
    date_now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    parser = OptionParser()
    parser.add_option("-n", "--serverName", action="store",
                      dest="serverName",
                      default=False,
                      help="serverName to do")
    parser.add_option("-a", "--action", action="store",
                      dest="action",
                      default="status",
                      help="action -a [checkout,pull,push,master,install]")
    parser.add_option("-v", "--versionId", action="store",
                      dest="versionId",
                      default=date_now,
                      help="-v versionId defalut datetime [%Y-%m-%d-%H-%M:2019-03-06-16-05] ")

    parser.add_option("-b", "--branchName", action="store",
                      dest="branchName",
                      default="master",
                      help="-b branchName")

    # jar 服务启动区分环境,作为参数传入镜像中作为启动参数
    parser.add_option("-e", "--envName", action="store",
                      dest="envName",
                      default="test",
                      help="-e envName")

    options, args = parser.parse_args()
    return options, args

def _init():

    if not os.path.exists(serverConf):
        print ("serverconf:%s is not exists" % serverConf)
        sys.exit(1)
    if not os.path.exists(startConf):
        print ("startconf：%s is not exists" % startConf)
        sys.exit(1)

    serverDict = Conf(serverConf).getconf()
    options, args = getOptions()
    action = options.action
    version = options.versionId
    serverName = options.serverName
    branchName = options.branchName
    envName = options.envName
    if not action:
        print ("参数执行操作 -a action [install,init,back,rollback，getback，start,stop,restart]")
        sys.exit(1)
    elif not serverName:
        print ("参数服务名 -n servername ")
        printServerName(serverDict)
        sys.exit(1)
    elif not envName:
        print ("参数执行操作 -e envName [dev,test,pro]")
        sys.exit(1)
    else:
        if serverName == "all":
            if readfile(startConf):
                serName, point = readfile(startConf)
            else:
                point = 0
            # 进行升序排列
            serverlist = sorted(serverDict.keys())
            # 从上次执行失败的位置开始执行
            for serName in serverlist[int(point):]:
                ser_index = serverlist.index(serName)
                info = "%s:%s" % (ser_index, serName)
                writefile(startConf, info)
                main(serName, branchName, action, envName, version, serverDict)
            cleanfile(startConf)
        else:
            if serverName not in serverDict:
                print ("没有服务名：%s" % serverName)
                printServerName(serverDict)
                sys.exit(1)
            main(serverName, branchName, action, envName, version, serverDict)

def printServerName(Dict):
    serverlist = sorted(Dict.keys())
    for serverName in serverlist:
        print ("可执行服务名：%s" % serverName)
    return serverlist

# 读取启动服务顺序文件
def readfile(file):
    if not os.path.exists(file):
        return False
    with open(file) as fd:
        for i in fd.readlines():
            if i:
                return [i.strip().split(":")[1], i.strip().split(":")[0]]
            return False

# 写启动服务顺序文件
def writefile(file,info):
    if not os.path.exists(file):
        print (file)
        with open(file, 'w+') as fd:
            fd.write(info)
    else:
        with open(file, 'w+')as fd:
            fd.write(info)

# 清理启动服务顺序文件
def cleanfile(file):
    with open(file, 'w+') as fd:
        fd.write("")

def execsh(cmd):
        try:
            print ("exec ssh command: %s" % cmd)
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except Exception as e:
           print(e)
           sys.exit(1)
        stdout, stderr = p.communicate()
        # 需要转换byte to str
        stdout = stdout.decode()
        stderr = stderr.decode()
        return (stdout, stderr)

def printOutErr(stdout, stderr):
    if stdout and len(stdout) > 3:
        print("stdout >>>%s" % stdout)
        return True
    if stderr:
        print("stderr >>>%s " % stderr)
        return False

def main(serverName, branchName, action, envName, version, serverDict):
    servicer = service(serverName, branchName, envName, version, serverDict)
    if action == "build":
        servicer.buildMaven()
        servicer.buildImage()
        servicer.pushimage()
    elif action == "init":
        servicer.init()
    elif action == "push":
        servicer.pushimage()
    elif action == "create":
        servicer.createServer()
    elif action == "check":
        servicer.checkService()
    elif action == "remove":
        servicer.reomveServer()
    elif action == "recreate":
        servicer.reomveServer()
        servicer.createServer()
    elif action == "update":
        servicer.buildMaven()
        servicer.buildImage()
        servicer.pushimage()
        servicer.updataServer()
    elif action == "rollback":
        servicer.rollBackServer()
    elif action == "none":
        # servicer.createNetwork("")
        servicer.buildMaven()
        servicer.buildImage()
        servicer.pushimage()
        # print (servicer.checkService())

        # servicer.reomveServer()
        # servicer.createServer()

        # servicer.rollBackServer()
        servicer.updataServer()

    else:
       print("action check")

if __name__ == "__main__":
    mvn = "/app/apache-maven-3.5.0/bin/mvn"
    serverConf = "/docker_springcloud/server.conf"
    startConf = "/docker_springcloud/start.conf"

    # 设置默认上次镜像地址
    repositoryUrl = "10.0.1.133:5000"
    # service.execsh('s','sss')
    # logpilot()
    # main()
    _init()
