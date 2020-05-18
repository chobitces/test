import threading
import time
import queue
from app.serialInterface import SerialInterface
from app.app_ssh import SSH_Client
import tkinter.messagebox as messagebox
import app.tool as tl

class Connection():
    connect_type = ""
    def __init__(self):
        self.data_queue = queue.Queue(maxsize=1000)
        self.__clsInit()
        self.ConnectedFlag = 0
        self.RevFlag = 0
        self.readbuff = ""
    def __clsInit(self):
        """
        类实例化
        链接的三种方式
        :return:
        """
        self.com = SerialInterface()
        self.ssh = SSH_Client()
    def apiLogin(self, paradict):
        """
        通过对应的方式登陆，并注册读写函数，及登出函数
        :param paradict:
        :return:
        """
        result = 0
        print(paradict)
        self.connect_type = paradict["conntype"]
        if paradict["conntype"] =="serial":
            result = self.com.open(baudrate=paradict["baudrate"], port=paradict["comport"])
            self.logout = self.com.closeCom
            self.read = self.com.readLineData
            self.write = self.com.writedata
        elif paradict["conntype"] =="SSH":
            result = self.ssh.sshclient_connect(hostip = paradict["host_ip"],
                                                username = paradict["username"],
                                                password = paradict["userpassword"],
                                                port = int(paradict["ssh_port"]))
            self.logout = self.ssh.closeConnection
            self.read = self.ssh.sshclient_rev
            self.write = self.ssh.sshclient_send
        else:
            messagebox.showerror(title='错误！', message='选择连接方式失败')
            
            
        if (0 == result):
            self.ConnectedFlag = 1
            print("connect success")
            self.receiveProcess = threading.Thread(target=self.__revDataProcess)
            self.receiveProcess.setDaemon(True)
            self.receiveProcess.start()


        return result


    def apiLogout(self):
        if(self.ConnectedFlag == 1):
            self.logout()
            self.ConnectedFlag = 0
            tl.stop_thread(self.receiveProcess)
            return 0
        else:
            messagebox.showerror(title='警告！', message='未连接')
            return -1


    def __revDataProcess(self):
        '''
        函数名称：
        功    能：接收数据，并触发数据上传，登录后创创建此线程
        输    入：无
        输    出：无
        说    明：
        :return:无
        '''
        while (self.ConnectedFlag == 1):
            try:
                bytes = self.read()
                if bytes != "" and bytes != None:
                    self.data_queue.put(bytes)
                    # print("R:",bytes.encode('ascii'),len(bytes)),
                    if self.RevFlag == 1:
                        self.readbuff = self.readbuff + bytes
                time.sleep(0.01)
            except Exception as E:
                print(E)
                time.sleep(0.1)
                if(self.ConnectedFlag == 1):
                    messagebox.showerror(title='警告！', message='读取数据失败')
                else:
                    print("已退出")


