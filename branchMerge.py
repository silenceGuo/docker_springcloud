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
"""git分支合并新建推送"""

def getOptions():
    # date_now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    parser = OptionParser()
    parser.add_option("-d", "--Dir", action="store",
                      dest="Dir",
                      default=False,
                      help="-d dir to do")
    parser.add_option("-a", "--action", action="store",
                      dest="action",
                      default=False,
                      help="-a action  dir")
    parser.add_option("-b", "--branch", action="store",
                      dest="branch",
                      default=False,
                      help="-b branch to checkout or merge ")
    parser.add_option("-m", "--mbranch", action="store",
                      dest="mbranch",
                      default=False,
                      help="-m master branch for merge")

    options, args = parser.parse_args()
    return options, args

def execsh( cmd):
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

def ReturnExec(cmd):
    print(80 * "#")
    stdout, stderr = execsh(cmd)

    if stdout:
        print ("out:%s " % stdout)
        if "fatal"in stdout:
            print ("出现错误，请检查" )
            return False
            # sys.exit(1)
        if "CONFLICT" in stdout:
            print("出现错误，请检查")
            return False

    if stderr:
        print("err:%s" % stderr)
        if "fatal"in stderr:
            print ("出现错误，请检查" )
            return False
        if "CONFLICT" in stderr:
            print("出现错误，请检查")
            return False
    # print(80 * "#")
    return True

def merge(Dir,branch, mbranch):
    os.chdir(Dir)
    print ('拉取需要远端的分支')
    fetch_branch_cmd = "sudo git fetch"
    ReturnExec(fetch_branch_cmd)

    print ("chenckout分支 %s 并更新" % branch)
    checkout_branch_cmd = "sudo git checkout %s" % branch
    ReturnExec(checkout_branch_cmd)

    pull_cmd = "sudo git pull"
    ReturnExec(pull_cmd)

    checkout_mbranch_cmd = "sudo git checkout %s" % mbranch
    ReturnExec(checkout_mbranch_cmd)

    ReturnExec(pull_cmd)

    print ('合并%s 分支到 %s'%(branch, mbranch))
    merge_cmd = "sudo git merge %s" % mbranch

    reset_cmd = "sudo git reset --hard origin/%s" % mbranch

    if not ReturnExec(merge_cmd):
        print("合并失败，回退分支%s" % mbranch)
        ReturnExec(reset_cmd)
        sys.exit(1)

    # print ('推送到远端分支%s'% mbranch)
    # push_cmd = "sudo git push origin %s" % mbranch
    # ReturnExec(push_cmd)

def checkout(Dir,branch):
    print ("切换工作目录%s"% Dir)
    os.chdir(Dir)

    print("切换工作分支，并更新")
    checkout_cmd = "sudo git checkout %s" % branch
    ReturnExec(checkout_cmd)

    pull_cmd = "sudo git pull"
    ReturnExec(pull_cmd)

def push(Dir,mbranch):
    print ("切换工作目录%s"% Dir)
    os.chdir(Dir)
    print('推送到远端分支%s' % mbranch)
    push_cmd = "sudo git push origin %s" % mbranch
    ReturnExec(push_cmd)

def createBranch(Dir,branch):
    print("切换工作目录%s" % Dir)
    os.chdir(Dir)
    print("切换工作分支，并更新")
    checkout_cmd = "sudo git checkout -b %s" % branch
    ReturnExec(checkout_cmd)
    print('推送到远端分支%s'% branch)
    push_cmd = "sudo git push origin %s" % branch
    ReturnExec(push_cmd)

    print("关联本地{branch} 分支与远程{branch}".format(branch=branch))
    upstream_cmd = "sudo git branch --set-upstream-to=origin/{branch} {branch}".format(branch=branch)
    ReturnExec(upstream_cmd)

    pull_cmd = "sudo git pull"
    ReturnExec(pull_cmd)

def pull(Dir,Env,branch):
    #还要调试
    remoteActionCmd = "ansible {Env} -i {ansiblehost} -m shell -a 'cd {Dir};sudo git checkout {branch};sudo git pull'".format(
        Env=Env,
        Dir=Dir,
        ansiblehost="ansibleHost",
        branchName=branch)
    ReturnExec(remoteActionCmd)

def main():
    options, args = getOptions()
    Dir = options.Dir
    branch = options.branch
    mbranch = options.mbranch
    action = options.action
    if not Dir:
        print("-d git work DIR")
        sys.exit(1)
    if action == "merge":
        if not branch:
            print("-b branch to merge")
            sys.exit(1)
        if not mbranch:
            print("-m master branch for merge")
            sys.exit(1)
        merge(Dir, branch, mbranch)
    elif action == "checkout":
        if not branch:
            print("-b branch to checkout")
            sys.exit(1)
        checkout(Dir, branch)
    elif action == "create":
        if not branch:
            print("-b branch to create branch checkout")
            sys.exit(1)
        createBranch(Dir, branch)
    elif action == "push":
        if not mbranch:
            print("-m mbranch to push branch ")
        push(Dir, mbranch)
    else:
        print ("-a aciton merge, checkout, create")
        sys.exit()

if __name__ == "__main__":

    main()

