import threading
import time
import re

from ui.main_windows import Ui_MainWindows
from ui.connect_ui import Ui_ConnectSetWindows, Ui_SerialSetWindows, Ui_SshSetWindows
from app.serialInterface import SerialInterface
import tkinter as tk
import tkinter.messagebox as messagebox
from  app.connection import Connection

class Application():
    def __init__(self,ui):
        self.root = ui
        self.senddataVar = tk.StringVar()
        self.MainWindow = Ui_MainWindows(self.root)
        self.serialtype = SerialInterface()
        self.ConnectApi = Connection()
        self.mainUiWidget()
        self.initValue()
        # 建脚本运行的线程，传入的参数为脚本的路径
        self.OneSecPrcocess = threading.Thread(target=self.oneSecProcess)
        self.OneSecPrcocess.setDaemon(True)
        self.OneSecPrcocess.start()
    def initValue(self):
        self.connectuiopenflag = 0  # 连接方式选择的那个界面是否打开的标志
        self.connectedFlag = 0      # 是否连接的标志位
    def mainUiWidget(self):
        # 添加菜单栏
        self.menu1 = tk.Menu(self.root, tearoff=0)  # 1的话多了一个虚线，如果点击的话就会发现，这个菜单框可以独立出来显示
        self.menu1.add_command(label="连接",command = self.openConnectUi)
        self.menubar = tk.Menu(self.root)
        self.menubar.add_cascade(label="文件", menu = self.menu1)
        self.root.config(menu = self.menubar)



        self.entry_sendaera = tk.Entry(self.MainWindow.frame_sendaera, textvariable = self.senddataVar)
        self.entry_sendaera.place(relx = 0.02, rely = 0.08, relheight = 0.45, relwidth = 0.96)
        self.entry_sendaera.bind("<Return>", self.sendDataFormSendArea)

        self.root.bind("<Button-3>",self.rightMouseEvent)
    def rightMouseEvent(self,event):
        self.rmEvent = tk.Toplevel(self.root)
        # event.x 鼠标左键的横坐标
        # event.y 鼠标左键的纵坐标
        print(event.x,event.y)
        print(self.root.winfo_x(),self.root.winfo_y())
        self.rmEvent.geometry('%dx%d+%d+%d' % (50, 200, self.root.winfo_x() + event.x,
                                               self.root.winfo_y() + event.y))

    def openConnectUi(self):
        if(self.connectuiopenflag == 0):
            if(self.connectedFlag == 0):
                self.ConnectUi = Ui_ConnectSetWindows(self.root)
                self.ConnectUi_Connect = tk.Button(self.ConnectUi.ConnectUi,width = 10,text = "确定",
                                                command = self.get_connect_type_param)
                self.ConnectUi_Connect.grid(row=0, column=2)
                self.connectuiopenflag = 1
            else:
                messagebox.showerror(title='警告！', message='已连接')
        else:
            messagebox.showerror(title='警告！', message='界面已打开')


    def get_connect_type_param(self):
        showStr = []
        self.connect_type = self.ConnectUi.combox_connecttype.get() # 获取链接方式
        self.ConnectUi.ConnectUi.destroy()
        print(self.connect_type)
        if(self.connect_type == "serial"):
            # 自动获取当前可用的串口号
            portList = self.serialtype.findSerialPort()
            if len(portList) > 0:
                for i in portList:
                    showStr.append(str(i[1]))
            self.ConnectSetUi = Ui_SerialSetWindows(self.root,tuple(showStr))
            self.Button_Connect = tk.Button(self.ConnectSetUi.ConnectUi,width = 20,text = "连接",
                                            command = self.connection_connect)
            self.Button_Connect.grid(row=5, column=1)
        elif(self.connect_type == "SSH"):
            self.ConnectSetUi = Ui_SshSetWindows(self.root)
            self.Button_Connect = tk.Button(self.ConnectSetUi.ConnectUi,width = 20,text = "连接",
                                            command = self.connection_connect)
            self.Button_Connect.grid(row=5, column=1)
        else:
            messagebox.showerror(title='警告！', message='连接类型错误')
    def connection_connect(self):
        """
        链接处理函数，根据get_connect_type_param打开的窗口中的信息来进行连接，
        也是get_connect_type_param窗口 链接按钮的服务函数
        :return:
        """
        tpdict = {}  # 用来存放链接信息的字典
        cnt = 0
        tpdict["conntype"] = self.connect_type
        if self.connect_type == "serial":
            # 正则表达式获取，实际的串口号
            resultlist = re.findall(r'[(](.*?)[)]',self.ConnectSetUi.combox_port.get(),re.S)
            tpdict["comport"] = resultlist[0]
            tpdict["baudrate"] = self.ConnectSetUi.combox_baudrate.get()
            tpdict["databit"] = self.ConnectSetUi.combox_databit.get()
            tpdict["parity"] = self.ConnectSetUi.combox_parity.get()
            tpdict["stopbits"] = self.ConnectSetUi.combox_stopbits.get()
            tpdict["name"] = tpdict["comport"]
            print(tpdict)
        elif self.connect_type == "SSH":
            tpdict["host_ip"] = self.ConnectSetUi.Entry_hostip.get()
            tpdict["ssh_port"] = self.ConnectSetUi.Entry_port.get()
            tpdict["username"] = self.ConnectSetUi.Entry_username.get()
            tpdict["userpassword"] = self.ConnectSetUi.Entry_password.get()
            tpdict["name"] = self.ConnectSetUi.Entry_name.get()

            # 如果没有输入名字，那么名字就设置为链接方式
            if tpdict["name"] == "":
                tpdict["name"] = tpdict["host_ip"]
        else:
            messagebox.showerror(title='警告！', message='连接类型错误')
            return -1

        #关闭界面
        self.ConnectSetUi.ConnectUi.destroy()
        result = self.ConnectApi.apiLogin(tpdict)
        if result == -1:
            messagebox.showerror(title='警告！', message='连接失败')
        else:
            self.connectedFlag = 1
            self.receiveProcess = threading.Thread(target=self.revDataDiaplayProcess)
            self.receiveProcess.setDaemon(True)
            self.receiveProcess.start()
    def revDataDiaplayProcess(self):
        while 1:
            if(self.connectedFlag == 1): #如果已经链接
                s = self.ConnectApi.data_queue.get()  # 通过ConnectApi中的信号，将ConnectApi中获取的返回数据传到main中
                self.MainWindow.print_inrevarea(s)      # 触发信号：触发信息上传，上传到接收显示区域

            # time.sleep(0.01)
    def oneSecProcess(self):
        while(1):
            time.sleep(1.0)

            # 下面是判断是否关闭连接设置的窗口
            if(self.connectuiopenflag == 1):
                try:
                    self.ConnectUi.ConnectUi.state()
                except:
                    try:
                        self.ConnectSetUi.ConnectUi.state()
                    except:
                        self.connectuiopenflag = 0
    def sendDataFormSendArea(self,ev = None):
        if(self.connectedFlag == 1):
            data = self.senddataVar.get()
            data = data.replace("\n","") + "\n"
            # print("print_window send:", data)
            self.ConnectApi.write(data)
            self.senddataVar.set("")
            #self.receiveUpdateSignal.emit("")
        else:
            messagebox.showerror(title='警告！', message='未连接')



def main():
    ui = tk.Tk()
    app = Application(ui)
    ui.mainloop()

if __name__ == '__main__':
    main()