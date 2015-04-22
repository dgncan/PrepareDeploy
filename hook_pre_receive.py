#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ************************************************************************
# Bu script istediginiz bare git reposunun hookuna linklecek
#
# optimum/deney adlı repo için örnek kullanım:
# 2. chmod 755 /deploy-worktree/DIGER/COZUM-optimum/PrepareDeploy/hook_pre_receive.py
# 1. ln -s /deploy-worktree/DIGER/COZUM-optimum/PrepareDeploy/hook_pre_receive.py /home/git/repositories/optimum/deney.git/hooks/pre-receive
# 3. chown git:git /deploy-worktree/DIGER/COZUM-optimum/PrepareDeploy/hook_pre_receive.py  (bu srcpitte değişiklik yapınca bu değişiyor, o yüzden unutmamak lazım)
# 4. rm /deploy-worktree/DIGER/COZUM-optimum/PrepareDeploy/hook_pre_receive.pyc
# not:
#   Appearance & Behaviour / System Settings ten use "safe write" işaretini kaldır ki, yazma izni sorunu oluyor.
# ************************************************************************

import sys
import fileinput
import os
from ConsoleCommandRunner import ConsoleCommandRunner


ROOT_GIT_REPO_DIR = "/home/git/repositories/" # example format: /home/git/repositories/
reject_branch = ["master-release","test-release"]
allow_branch = ["master","test"]
allow_committer = ["Dogan CAN"]

for line in fileinput.input():
    old_rev = line.split("\n",1)[0].split(" ")[0]
    new_rev = line.split("\n",1)[0].split(" ")[1]
    branch  = line.split("\n",1)[0].split(" ")[2].split("/")[2]

repo_dir_name = ROOT_GIT_REPO_DIR.split("/")[len(ROOT_GIT_REPO_DIR.split("/"))-2]
user = os.getcwd().split(repo_dir_name + "/", 1)[1].split("/")[0]
repo = os.getcwd().split(repo_dir_name + "/", 1)[1].split("/")[1].split(".")[0]

# change directory
os.chdir(ROOT_GIT_REPO_DIR + user + "/" + repo + ".git")

cmd = ['git show ' + new_rev + ' --pretty=oneline --pretty=format:%an | head -n1']
CCR = ConsoleCommandRunner()
(out, error) = CCR.command_run(cmd)
if error!="":
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "ERROR : " + out
    print "******************************************************************************"
    sys.exit(1)
else:
    committer_name = out

# Abort the push
if committer_name in allow_committer:
    # private user allow
    print
    print "******************************************************************************"
    print "PUSH EDILECEK, LUTFEN PUSH SONRASI GITLAB'DAN MERGE-REQUEST OLUSTURUN YA DA OLUSMUS MERGE-REQUESTINI ONAYLAYIN "
    print "ADMIN : (",committer_name,") "
    print "******************************************************************************"
    print
else:
    if branch in allow_branch:
        print
        print "******************************************************************************"
        print "PUSH EDILECEK, LUTFEN PUSH SONRASI GITLAB'DAN MERGE-REQUEST OLUSTURUN YA DA OLUSMUS MERGE-REQUESTINI ONAYLAYIN "
        print "COMMITTER: '"+committer_name+"',  BRANCH: '"+branch+"'"
        print "******************************************************************************"
        print
    else:
        print
        print "******************************************************************************"
        print "BU BRANCH PUSH ALMAZ!"
        print "Lütfen sadece ",allow_branch," branchlerini kullanın"
        print "Bu branch icin izinli kullanicilar : ", allow_committer, " (GITLAB ile Merge Request kullanabilir)"
        print "branch :" + branch
        print "committer :" + committer_name
        print "******************************************************************************"
        print
        sys.exit(1)
