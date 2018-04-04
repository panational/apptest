#!usr/bin/python
# -*- coding:utf-8 -*-
import subprocess
from common.ApkBase import ApkInfo

from BaseDevicePreProcess import *

class VivoX7ProPreProcess(BaseDevicePreProcess):

    def __init__(self, tester):
        super(VivoX7ProPreProcess, self).__init__(tester)
        self.apk_name = ApkInfo().get_apk_pkg()


    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid, DataProvider.testapk)
        subprocess.call(cmd, shell=True)
        time.sleep(3)

    def install_process(self):
        Log.logger.info(u"设备：%s 处理安装中各种弹窗" % self.tester.device.devicename)

        try:
            Log.logger.info(u"设备：%s 启动app并处理安装弹窗" % self.tester.device.devicename)
            time.sleep(7)
            self.tester.tap_screen(500, 1900)

            time.sleep(7)
            self.tester.tap_screen(260, 1855)


            while self.driver.is_app_installed(self.apk_name) == False:
                time.sleep(2)

            # 启动APP
            self.driver.launch_app()

            # GPS权限
            time.sleep(7)
            self.tester.tap_screen(550, 1350)

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

            # 该流程包括点击login按钮到达登录页面，并登录

    def login_success_process(self):
        Log.logger.info(u"设备：%s 登录成功后，处理各种自动弹窗" % self.tester.device.devicename)
        try:
            # 联系人权限
            time.sleep(7)
            self.tester.tap_screen(316, 1315)

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
        try:
            # 打开取景框
            self.tester.find_element_by_id_and_tap(self.apk_name + ':id/btnCamera')

            # 切换到拍摄tab
            self.tester.find_element_by_id_and_tap(self.apk_name + ':id/camera_tv')

            #摄像机权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

            #录音权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

            #关闭取景框
            self.tester.find_element_by_id_and_tap(self.apk_name + ':id/titlebar_return')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)



