#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *

class ONEPlusXPreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(ONEPlusXPreProcess, self).__init__(tester)


    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 启动app并处理GPS弹窗" % self.tester.device.devicename)

            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)

            self.driver.launch_app()
        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def login_success_process(self):
        pass

    def get_permission_process(self):
        Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
        try:
            #打开取景框
            self.tester.find_element_by_id_and_tap('com.nice.main:id/btnCamera')
            self.tester.find_element_by_id_and_tap('com.nice.main:id/camera_tv')

            # 退出取景框，回到发现页面
            self.tester.find_element_by_id_and_tap('com.nice.main:id/titlebar_return')
        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)