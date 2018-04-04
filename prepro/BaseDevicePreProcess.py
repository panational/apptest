#!usr/bin/python
# -*- coding:utf-8 -*-

from common.DataProvider import *
from common.Log import *
import threading
import traceback
from common.DriverManager import *
from appium.webdriver.common.touch_action import TouchAction
import time
from appium.webdriver.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from model.Tester import *
from common.ApkBase import ApkInfo
import subprocess


class BaseDevicePreProcess(object):

    def __init__(self, tester):
        self.tester = tester
        self.driver = self.tester.driver
        self.action = TouchAction(self.driver)
        self.user = self.tester.user
        self.apk_name = ApkInfo().get_apk_pkg()
        self.apk_version_name = ApkInfo().get_apk_version_name()

    # 开始预处理流程
    def pre_process(self):
        #获取安装包信息：


        Log.logger.info(u"设备：%s 开始预处理流程..." % self.tester.device.devicename)
        driver = self.tester.driver
        try:
            if driver.is_app_installed(self.apk_name) and not self.is_app_versioname(self.apk_version_name):
                Log.logger.info(u"设备：%s 卸载旧版本的apk包" % self.tester.device.devicename)
                driver.remove_app(self.apk_name)
                Log.logger.info(u"设备：%s 开始安装测试的apk包" % self.tester.device.devicename)
                thread = threading.Thread(target=self.install_process)
                thread.start()
                self.install_app()
                thread.join()
            if not driver.is_app_installed(self.apk_name) :
                Log.logger.info(u"设备：%s 开始安装测试的apk包" % self.tester.device.devicename)
                thread = threading.Thread(target=self.install_process)
                thread.start()
                self.install_app()
                thread.join()
            Log.logger.info(u"设备：%s 启动成功" % self.tester.device.devicename)
            self.login_process()
            Log.logger.info(u"设备：%s 登录成功" % self.tester.device.devicename)
            # self.login_success_process()
            # time.sleep(10)
            # self.get_permission_process()
            # time.sleep(3)
            # self.tester.clean_mp4_file()     #预处理时清除sd的mp4文件
            Log.logger.info(u"设备：%s 预处理成功，开始执行测试用例" % self.tester.device.devicename)
        except  Exception, e:
            Log.logger.info(u"设备：%s 出现异常!" % self.tester.device.devicename)
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)
            return False
        return True

#获取已安装apk版本
    def is_app_versioname(self,apkversioname):
        cmd = "adb shell dumpsys package %s | findstr versionName" % self.apk_name
        result = ""
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if output != "":
            result = output.strip('\r\n')
            result = result.decode()[16:]
            if result==apkversioname:
                return True
            else:
                return False
        else:
            return False


    # 安装流程
    def install_app(self):
        self.driver.install_app(DataProvider.testapk)

    # 版本升级
    def upgrade_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid, DataProvider.latestapk)
        subprocess.call(cmd, shell=True)

        time.sleep(5)
        self.driver.launch_app()

        self.tester.start_screen_record(u'直播礼物开屏')
        time.sleep(10)
        self.tester.stop_screen_record(u'直播礼物开屏')

    # 该流程包括处理安装及启动过程中的各种弹窗，一直到可以点击login按钮
    def install_process(self):
        pass

    # 该流程包括点击login按钮到达登录页面，并登录
    def login_process(self):
        Log.logger.info(u"设备：%s 开始登录，使用账号:%s" % (self.tester.device.devicename, self.tester.user.username))
        try:
            # 账号登录
            self.tester.find_element_by_xpath_and_tap("//android.view.View[@content-desc='收不到验证码？使用账号密码登录']")

            self.tester.switchUrl("loginstaticHtml.html")
            time.sleep(2)
            element = self.driver.find_element_by_xpath("(//input[@placeholder='报名时登记的手机号'])[2]")
            self.driver.execute_script("arguments[0].setAttribute('value', arguments[1])", element, self.tester.user.username)
            element.click()
            element = self.driver.find_element_by_xpath("//input[@placeholder='请输入密码']")
            self.driver.execute_script("arguments[0].setAttribute('value', arguments[1])", element, self.tester.user.password)
            element.click()
            element=self.driver.find_element_by_xpath("//button[@class='mint-button mint-button--primary mint-button--large']")
            self.driver.execute_script("arguments[0].removeAttribute('disabled')",element)
            time.sleep(2)
            element.click()
            self.driver.switch_to.context(u'NATIVE_APP')

            # self.tester.find_element_by_xpath_and_send_keys("//android.widget.EditText[@index='6']",self.tester.user.username)
            #
            # self.tester.find_element_by_xpath_and_send_keys("//android.widget.EditText[@index='7']", self.tester.user.password)
            #
            # self.tester.find_element_by_xpath_and_tap("//android.widget.Button[@index='8']")

            self.tester.screenshot(u"登录成功")
        except Exception,e:
            raise

    # 该流程包括登录成功后，对各种自动弹出对话框进行处理
    def login_success_process(self):
        pass

    # 对所有需要的权限进行处理，例如：相机、录音
    def get_permission_process(self):
        pass

    def check_user_profile_pic(self):
        self.tester.find_element_by_id_and_tap(self.apk_name + ':id/btnTabProfile')
        self.tester.find_element_by_id_and_tap(self.apk_name + ':id/img_profile_avatar')
        time.sleep(3)
        if self.tester.is_element_exist('编辑头像'):
            print '该用户未添加头像'
            self.tester.find_element_by_id_and_tap(self.apk_name + ':id/img_publish_photo')
            time.sleep(3)
            if self.tester.is_element_exist(self.apk_name + ':id/image'):
                self.tester.find_element_by_uiautomator_and_tap('new UiSelector().resourceId(\"self.apk_name + :id/image\").index(0)')
                self.tester.find_element_by_id_and_tap(self.apk_name + ':id/titlebar_action_btn')
                self.tester.find_element_by_id_and_tap(self.apk_name + ':id/titlebar_action_btn')
                time.sleep(5)  # 上传头像到【我】页面
            else:
                Log.logger.info(u'上传头像失败')
                self.tester.find_element_by_id_and_tap(self.apk_name + ':id/titlebar_return')
                self.tester.find_element_by_id_and_tap(self.apk_name + ':id/titlebar_return')
        else:
            print '该用户已添加头像'
            self.tester.find_element_by_id_and_tap(self.apk_name + ':id/profile_black')

    # 创建autotest文件夹并生成测试图片
    def data_prepare(self):
        Log.logger.info(u"设备：%s 检查文件开始" % self.tester.device.devicename)
        if self.tester.is_autotest_exit():
            time.sleep(1)
        else:
            Log.logger.info(u"设备：%s 写入测试文件" % self.tester.device.devicename)
            self.tester.pull_file_to_device()
            time.sleep(10)
            self.tester.refresh_test_pic()









