# -*- coding: utf-8 -*-

from common.Log import *
import os


def stopAppium():
    r = os.popen("ps -ef | grep appium")
    info = r.readlines()
    for line in info:  # 按行遍历
        eachline = line.split()
        appium_pid = eachline[1]
        action = os.popen("kill " + appium_pid)
        print("kill" + appium_pid)

def kill_server(port):
    cmd = "netstat -ano |findstr %s" % port
    line = os.popen(cmd).readline()
    if line != '':
        #Log.logger.info(u"端口被占用，结束端口进程\n%s" % line)
        aList = line.split()
        cmd = "taskkill /F /T /PID %s" % aList[4]
        os.popen(cmd).read()

stopAppium()
kill_server(8886)

