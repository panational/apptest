#!usr/bin/python
# -*- coding:utf-8 -*-
import os
import subprocess
from math import floor
from common.DataProvider import DataProvider


class ApkInfo():

    def __init__(self):
        apkpath = DataProvider.testapk
        self.apkpath = apkpath

    def get_apk_size(self):
        """
        获取包的大小
        """
        size = floor(os.path.getsize(self.apkpath) / (1024 * 1000))
        return str(size) + "M"

    def get_apk_version_name(self):
        """
        获取版本 package: name='gaosi.com.learn' versionCode='10' versionName='1.6.0'
        """
        cmd = "aapt dump badging " + self.apkpath + " | findstr versionName"
        result = ""
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if output != "":
            result = output.strip('\r\n')
            result = result.split()[3].decode()[13:-1]
        return result

    def get_apk_name(self):
        """
        获取应用名 application-label:'鐖卞涔犲鐢熺'
        """
        cmd = "aapt dump badging " + self.apkpath + " | findstr application-label: "
        result = ""
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if output != "":
            result = output.split()[0].decode()[18:]
        return result

    def get_apk_pkg(self):
        """
        获取包名 package: name='gaosi.com.learn' versionCode='10' versionName='1.6.0'
        """
        cmd = "aapt dump badging " + self.apkpath + " | findstr package:"
        result = ""
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if output != "":
            result = output.split()[1].decode()[6:-1]
        return result

    def get_apk_version_code(self):
        """
        获取version code
        """
        cmd = "aapt dump badging " + self.apkpath + " | grep package | awk '{print $3}'"
        result = ""
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if output != "":
            result = output.strip('\r\n')
        return result


