#!/usr/bin/env python
#！-*-coding:utf-8 -*-
#!@Date    : 2019/3/6 0006 下午 15:21
#!@Author : Damon.guo
#!@File   : callRemote.py
"""该脚本用于远程调用不同环境下的swarm 集群manger主机下的主脚本。用于执行相关操作，如果只有单一环境，jenkins打包服务
与manger 服务器在同一主机，该脚本可以省略，直接调用主脚本即可。
通过结合ansible hosts 文件中的分组来区分 ，参数env env参数直接传入到 ansibel 环境 在主脚本用于jar镜像构建打包
"""
import sys
import os
import control

def remoteAction(serverName,action, env,branchName,version):
    # 作为远程调用远端的本脚本 执行不同swarm 集群的服务更新 等操作,t
    remoteActionCmd = "ansible {env} -i {ansiblehost} -m shell -a " \
                      "'{python} {remotePy} -a {action} -n {serverName} -e {env} -b {branchName} -v {version}'".format(
        env=env,
        ansiblehost=ansibleHost,
        python=python,
        remotePy=remote_py,
        action=action,
        version=version,
        serverName=serverName,
        branchName=branchName)
    stdout, stderr = control.execsh(remoteActionCmd)
    if control.printOutErr(stdout, stderr):
        print("remote action %s service sucess :%s " % (action, serverName))
    else:
        print("remote action %s fail :%s " % (action, serverName))
        sys.exit()

def main():

    if not os.path.exists(serverConf):
        print ("serverconf:%s is not exists" % serverConf)
        sys.exit(1)
    if not os.path.exists(startConf):
        print ("startconf：%s is not exists" % startConf)
        sys.exit(1)

    serverDict = control.Conf(serverConf).getconf()
    options, args = control.getOptions()
    action = options.action
    version = options.versionId

    serverName = options.serverName
    branchName = options.branchName
    envName = options.envName
    if not action:
        print ('参数执行操作 -a action ["update", "rollback","recreate","remove","check","create"]')
        sys.exit(1)
    elif not serverName:
        print ("参数服务名 -n servername ")
        control.printServerName(serverDict)
        sys.exit(1)
    elif not envName:
        print ("参数执行操作 -e envName [dev,test,pro]")
        sys.exit(1)
    else:
        if action in["update", "rollback","recreate","remove","check","create"]:
            remoteAction(serverName, action, envName, branchName, version)
        else:
            print('参数执行操作 -a action ["update", "rollback","recreate","remove","check","create"]')
            sys.exit(1)
if __name__ == "__main__":
    serverConf = "/docker_springcloud/server.conf"
    startConf = "/docker_springcloud/start.conf"
    ansibleHost = "/etc/ansible/hosts"
    python = "/usr/local/bin/python3.7"
    # 定义远端swarm manger 主机脚本路径
    remote_py = "/docker_springcloud/control.py"
    main()
