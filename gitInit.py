#!/usr/bin/env python
#！-*-coding:utf-8 -*-
#!@Date    : 2019/4/27 0027 下午 15:24
#!@Author : Damon.guo
#!@File   : gitInit.py.py

import os
from optparse import OptionParser
import shutil
import datetime
import sys
from subprocess import PIPE, Popen
"""批量初始化项目的git仓库，会删除git仓库目录重新初始化"""

def getOptions():
    # date_now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    parser = OptionParser()
    parser.add_option("-d", "--Dir", action="store",
                      dest="Dir",
                      default=False,
                      help="-d dir to do")
    parser.add_option("-u", "--gitUrl", action="store",
                      dest="gitUrl",
                      default=False,
                      help="-u giturl init dir")
    parser.add_option("-f", "--force", action="store",
                      dest="force",
                      default=False,
                      help="-f force to init ")
    parser.add_option("-t", "--gitType", action="store",
                      dest="gitType",
                      default="ssh",
                      help="-t ssh,http")

    options, args = parser.parse_args()
    return options, args

def execsh(cmd):
    try:
        print("exec ssh command: %s" % cmd)
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    except Exception as e:
        print(e)
        sys.exit(1)
    stdout, stderr = p.communicate()
    # 需要转换byte to str
    #stdout = stdout.decode()
    #stderr = stderr.decode()
    return (stdout, stderr)

def ReturnExec(cmd):
    stdout, stderr = execsh(cmd)
    if stdout:
        print (80 * "#")
        print ("out:%s " % stdout)
    if stderr:
        print(80 * "#")
        print("err:%s" % stderr)

def init(Dir,gitUrl,gitType,force):
    # 初始化 本地打包构建git仓库
    print("git:%s init:%s" % (Dir, gitUrl))
    if not os.path.exists(Dir):
        os.makedirs(Dir)
    if not os.path.exists(Dir):
        os.mkdir(Dir)
    os.chdir(Dir)
    print("部署路径：", os.getcwd())
    stdout, stderr = execsh("git status .")
    if stdout:
        print("out：\n%s" % stdout)
        print("当前目录：%s,已经存在git仓库请检查!" % Dir)
        if not force:
            print ("强制重新初始化 使用 -f force")
            return False
        else:
            print ("切换工作目录至：'/' ")
            os.chdir("/")
            print("清理历史目录：%s" % Dir)
            shutil.rmtree(Dir)
            print ("重新建立目录：%s" % Dir)
            if not os.path.exists(Dir):
                os.mkdir(Dir)
            print("切换工作目录至：%s" % Dir)
            os.chdir(Dir)
            print("执行强制初始化")

    if stderr:
        print("没有git仓库，下一步")

    print("初始化本地仓库")
    ReturnExec("git init")

    # git url 使用http 协议的时候使用该命令 避免输入用户名密码
    # 用 ssh协议 请注释该代码
    if gitType == "http":
        print("本地git仓库当前项目认证")
        config_cmd = "git config --local credential.helper store"
        ReturnExec(config_cmd)


    print("拉取代码")
    pull_cmd = "git pull %s" % gitUrl
    ReturnExec(pull_cmd)

    print("添加远程仓库地址")
    add_remote_cmd = "git remote add origin %s" % gitUrl
    ReturnExec(add_remote_cmd)

    print("获取分支")
    fetch_cmd = "git fetch"
    ReturnExec(fetch_cmd)

    print("关联本地master分支与远程master")
    upstream_cmd = "git branch --set-upstream-to=origin/master master"
    ReturnExec(upstream_cmd)

    # CMD = "chown -R ec2-user.ec2-user %s" % Dir
    # ReturnExec(CMD)

def main():
    options, args = getOptions()
    Dir = options.Dir
    gitUrl = options.gitUrl
    force = options.force
    gitType = options.gitType
    # print (options, args)
    if not Dir:
        print("-d git init dir path")
        return False
    if not gitUrl:
        print ('-u git url')
        return False
    init(Dir, gitUrl, gitType, force)


if __name__ == "__main__":

    main()

