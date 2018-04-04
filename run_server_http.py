#!usr/bin/python
# -*- coding:utf-8 -*-

from common.HttpServerHandler import *
from SocketServer import ThreadingTCPServer
from common.Log import *
from Server.Server import *

def kill_server(port):
    cmd = "netstat -ano |findstr %s" % port
    line = os.popen(cmd).readline()
    if line != '':
        Log.logger.info(u"端口被占用，结束端口进程\n%s" % line )
        aList = line.split()
        cmd = "taskkill /F /T /PID %s" % aList[4]
        os.popen(cmd).read()


def start_server():
    myport = 8886
    kill_server(myport)
    host = "127.0.0.1"
    port = myport
    addr = (host, port)
    Log.logger.debug('Start Server...')
    server = ThreadingTCPServer(addr, HttpServerHandler)
    server.serve_forever()


def main(args=None):
    # 初始化日志配置
    Log.create_log_file()

    Log.logger.info(u"加载设备及用户配置信息")
    DataProvider.init_data()

    Log.logger.info(u"获得服务器上待测试的设备")
    DeviceManager.get_server_test_device()

    if len(DeviceManager.serverdevices) == 0:
        Log.logger.info(u"服务器上没有可以测试的设备")
        sys.exit()
    else:
        for deviceid, device in DeviceManager.serverdevices.items():
            server = Server(device)
            server.list_connect_devices()

    start_server()

if __name__ == '__main__':
    main()
