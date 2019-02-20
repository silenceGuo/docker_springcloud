#!/usr/bin/env python
#！-*-coding:utf-8 -*-
#!@Date    : 2019/2/18 0018 上午 11:53
#!@Author : Damon.guo
#!@File   : logrun.py
"""
使用阿里云开源日志采集工具，采集每个节点的所以容器日志发送到redis
"""
import os
from optparse import OptionParser
import sys
import subprocess
from subprocess import PIPE, Popen

def execsh(cmd):
    try:
        print("exec ssh command: %s" % cmd)
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

def getOptions():
    parser = OptionParser()
    parser.add_option("-n", "--serverName", action="store",
                      dest="serverName",
                      default=False,
                      help="serverName to do")
    parser.add_option("-a", "--action", action="store",
                      dest="action",
                      default="status",
                      help="action -a [checkout,pull,push,master,install]")

    # jar 服务启动区分环境 读取的配置不一样
    parser.add_option("-e", "--envName", action="store",
                      dest="envName",
                      default="test",
                      help="-e envName")

    options, args = parser.parse_args()
    return options, args

def logpilot(env,action):
    serverName = "log-poilt"

    startcmd = """docker run -d --rm -it \
    --name {serverName} \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /etc/localtime:/etc/localtime \
    -v /:/host:ro \
    --memory {xmx} \
    --cap-add SYS_ADMIN \
    -e LOGGING_OUTPUT=redis \
    -e REDIS_HOST={REDIS_HOST} \
    -e REDIS_PORT={REDIS_PORT} \
    registry.cn-hangzhou.aliyuncs.com/acs/log-pilot:0.9.5-filebeat""".format(REDIS_HOST=REDIS_HOST,
                                                                             REDIS_PORT=REDIS_PORT,
                                                                             serverName=serverName,
                                                                             xmx=xmx
                                                                             )
    "停止容器会自动清理容器，因为启动容器 参数 --rm"
    stopcmd="""docker stop %s""" % serverName


    cmd = "docker service create " \
          "--mode global " \
          "--mount type=bind,src=/,dst=/host " \
          "--mount type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock " \
          "--mount type=bind,src=/etc/localtime,dst=/etc/localtime " \
          "--network {network} " \
          "-e LOGGING_OUTPUT=redis " \
          "-e REDIS_HOST={REDIS_HOST} " \
          "-e REDIS_PORT={REDIS_PORT} " \
          "--name log-pilot " \
          "--limit-memory {xmx} " \
          "10.0.1.133:5000/log-poilt:v1".format(
        network="test",
        REDIS_HOST="10.0.1.133",
        REDIS_PORT="6379",
        xmx="512m")

    ansiblestartcmd = "ansible %s -i %s -m shell -a '%s'" % (env, ansibleHost, startcmd)
    ansiblestopcmd = "ansible %s -i %s -m shell -a '%s'" % (env, ansibleHost, stopcmd)

    if action == "start":

        stdout, stderr = execsh(ansiblestartcmd)
        # printOutErr(stdout, stderr)

    elif action == "stop":
        stdout, stderr = execsh(ansiblestopcmd)
        # printOutErr(stdout, stderr)
    elif action == "restart":
        stdout, stderr = execsh(ansiblestopcmd)
        printOutErr(stdout, stderr)
        stdout, stderr = execsh(ansiblestartcmd)
        # printOutErr(stdout, stderr)
    else:
        print ("action is restart,start, stop")
        sys.exit(1)

    if "FAILED" in stdout:
        print("stdout:%s" % stdout)
        print("stderr:%s" % stderr)
        print("%s %s False on %s " % (serverName, action, env))
        return False
    elif "FAILED" in stderr:
        print("stdout:%s" % stdout)
        print("stderr:%s" % stderr)
        print("%s %s False on %s " % (serverName, action, env))
        return False
    else:
        print("stdout:%s" % stdout)
        print("stderr:%s" % stderr)
        print("%s %s True on %s " % (serverName, action, env))
        return True

def main():
    options, args = getOptions()
    action = options.action
    envName = options.envName
    if not action:
        print ("参数执行操作 -a action [install,init,back,rollback，getback，start,stop,restart]")
        sys.exit(1)
    elif not envName:
        print ("参数执行操作 -e hostName [dev,test,pro]")
        sys.exit(1)
    else:
        logpilot(envName, action)

if __name__ == "__main__":
    ansibleHost = "/etc/ansible/hosts"
    REDIS_HOST = "10.0.1.133"
    REDIS_PORT = "6379"
    xmx = "512m"
    main()

    # logpilot(env="dev", action="restart")
    # main()
