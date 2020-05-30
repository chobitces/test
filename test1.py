import threading
import time
import re
import os

from ui.main_windows import Ui_MainWindows
from ui.connect_ui import Ui_ConnectSetWindows, Ui_SerialSetWindows, Ui_SshSetWindows
from app.serialInterface import SerialInterface
import tkinter as tk
from  tkinter  import ttk
import tkinter.messagebox as messagebox
from  app.connection import Connection
import app.tool as tl
import app.config as cfg

class Application():
    def __init__(self,ui):
        self.root = ui
        self.senddataVar = tk.StringVar()
        self.MainWindow = Ui_MainWindows(self.root)
        self.serialtype = SerialInterface()
        self.ConnectApi = Connection()
        self.mainUiWidget()
        self.initValue()
        self.configInit()
        # 建脚本运行的线程，传入的参数为脚本的路径
        self.OneSecPrcocess = threading.Thread(target=self.oneSecProcess)
        self.OneSecPrcocess.setDaemon(True)
        self.OneSecPrcocess.start()
    def initValue(self):
        self.connectuiopenflag = 0  # 连接方式选择的那个界面是否打开的标志
        self.connectedFlag = 0      # 是否连接的标志位
        self.openConfgUiFlag = 0
        self.sendHistoryBuff = []
        self.sendHistoryBuffCnt = 0
    def configInit(self):
        self.Config = cfg.Config(os.getcwd()) # 配置文件放在当前目前下
        self.displayConfgUi()
    def displayConfgUi(self):
        if(self.openConfgUiFlag == 0):
            self.sections = self.Config.read_section()   # 读取配置文件
            if self.sections:  # 如果有配置文件  则显示选取配置文件的界面
                self.sections_ui = tk.Toplevel(self.root)
                self.sections_ui.title("连接") # 修改框体的名字,也可在创建时使用className参数来命名；
                width = 250
                height = 350
                screenwidth = self.sections_ui.winfo_screenwidth()
                screenheight = self.sections_ui.winfo_screenheight()
                alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
                self.sections_ui.geometry(alignstr)
                self.sections_ui.resizable(width=True, height=True)
                self.sections_ui.attributes("-topmost", 1)
                self.openConfgUiFlag = 1
                self.Treeview_Config = ttk.Treeview(self.sections_ui,show = "tree")
                self.Treeview_Config.pack()
                id = self.Treeview_Config.insert("",0,"Session",text="Session",values=("1"))  # ""表示父节点是根
                for tp in range(len(self.sections)):
                    self.Treeview_Config.insert(id, tp, self.sections[tp], text= self.sections[tp], values=(str(tp + 2)))  # ""表示父节点是根
                self.Treeview_Config.bind("<Double-1>",self.treeviewClick)
                btn1 = tk.Button(self.sections_ui,width = 5,text = "新建",
                                                command = self.openConnectUi)
                btn1.pack()
                btn2 = tk.Button(self.sections_ui,width = 5,text = "清除",
                                                command = self.Config.del_section)
                btn2.pack()
            else:
                self.openConnectUi()
        else:
            messagebox.showerror(title='警告！', message='界面已打开')
    def treeviewClick(self,event):
        print("双击")
        item_text = 0
        for item in self.Treeview_Config.selection():
            item_text = int(self.Treeview_Config.item(item, "values")[0])
        print(item_text,type(item_text))
        if(item_text > 1):
            self.sections_connect(item_text - 2)
    def sections_connect(self,SectionId):
        # 通过当前选择，在配置文件中查找，找到它的所有配置
        try:
            # 获取当前选择
            currentSection = self.sections[SectionId]
            print(currentSection)
        except Exception as E:
            messagebox.showerror(title='警告！', message = str(E))
            return -1

        tpdict = self.Config.load(currentSection)



        self.sections_ui.destroy()
        self.openConfgUiFlag = 0

        # 登陆
        if(self.connectedFlag == 0):
            result = self.ConnectApi.apiLogin(tpdict)
            if result == -1:
                messagebox.showerror(title='警告！', message = "连接失败")
            else:
                self.connectedFlag = 1
                self.MainWindow.frame_revaera.config(bg = "green")
                self.receiveProcess = threading.Thread(target=self.revDataDiaplayProcess)
                self.receiveProcess.setDaemon(True)
                self.receiveProcess.start()
        else:
            messagebox.showerror(title='警告！', message = "已连接")
    def mainUiWidget(self):
        # 添加菜单栏
        self.menu1 = tk.Menu(self.root, tearoff=0)  # 1的话多了一个虚线，如果点击的话就会发现，这个菜单框可以独立出来显示
        self.menu1.add_command(label="连接",command = self.openConnectUi)
        self.menubar = tk.Menu(self.root)
        self.menubar.add_cascade(label="文件", menu = self.menu1)
        self.root.config(menu = self.menubar)

        self.Button_OpenSessionsUi = tk.Button(self.MainWindow.frame_memu,width = 5,text = "打开",
                                                command = self.displayConfgUi)
        self.Button_OpenSessionsUi.grid(row=0)
        self.Button_CreatConfigUi = tk.Button(self.MainWindow.frame_memu,width = 5,text = "打开",
                                                command = self.displayConfgUi)
        self.Button_CreatConfigUi.grid(row=0,column = 1)


        self.entry_sendaera = tk.Entry(self.MainWindow.frame_sendaera, textvariable = self.senddataVar)
        self.entry_sendaera.place(relx = 0.02, rely = 0.08, relheight = 0.45, relwidth = 0.96)
        self.entry_sendaera.bind("<Return>", self.sendDataFormSendArea)
        self.entry_sendaera.bind("<KeyPress-Up>", self.senddatakeyup)
        self.entry_sendaera.bind("<KeyPress-Down>", self.senddatakeydown)

        self.MainWindow.text_rev.bind("<Button-3>",self.rightMouseEvent)
    def rightMouseEvent(self,event):
        self.rmMenu = tk.Menu(self.root,tearoff=False)
        self.rmMenu.add_command(label = "清除",command=lambda:self.MainWindow.clearRevArea())
        self.rmMenu.add_command(label = "断开连接",command=lambda:self.closeConnect())
        self.rmMenu.post(event.x_root,event.y_root)
    def closeConnect(self):
        if(self.connectedFlag == 1):
            state  = self.ConnectApi.apiLogout()
            if(state == 0):
                self.connectedFlag = 0
                tl.stop_thread(self.receiveProcess)
                self.MainWindow.frame_revaera.config(bg = "red")
        else:
            messagebox.showerror(title='警告！', message='未连接')
    def openConnectUi(self):
        if(self.connectuiopenflag == 0):
            if(self.connectedFlag == 0):
                try:
                    self.sections_ui.state()  # 检测这个界面是否打开 如果是打开的  就关掉
                    self.sections_ui.destroy()
                    self.openConfgUiFlag = 0
                except:
                    pass


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
            # 登陆成功后，将登陆方式及登陆的一些参数存储到配置文件中
            # 如果配置文件中有一样名字的配置，就将这个配置名字加1放在（）中
            while 1:
                section = self.Config.read_section()
                if tpdict["name"] in section:
                    if "(" in tpdict["name"]:
                        tpdict["name"] = tpdict["name"].split("(")[0] + "(cnt)".replace("cnt", str(cnt))
                    else:
                        tpdict["name"] = tpdict["name"] + "(cnt)".replace("cnt", str(cnt))
                else:
                    break
                cnt = cnt + 1
            # 保存这个配置
            self.Config.save(tpdict)
            self.connectedFlag = 1
            self.MainWindow.frame_revaera.config(bg = "green")
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
            # print("1s")
            # 下面是判断是否关闭连接设置的窗口
            if(self.connectuiopenflag == 1):
                try:
                    self.ConnectUi.ConnectUi.state()
                except:
                    try:
                        self.ConnectSetUi.ConnectUi.state()
                    except:
                        self.connectuiopenflag = 0
            if(self.openConfgUiFlag == 1):
                try:
                    self.ConnectUi.ConnectUi.state()
                except:
                    self.openConfgUiFlag = 0
    def sendDataFormSendArea(self,ev = None):
        if(self.connectedFlag == 1):
            data = self.senddataVar.get()
            data = data.replace("\n","") + "\n"
            if (data != "\n" or (data in self.sendHistoryBuff)):
                self.sendHistoryBuff.append(data)
                print(self.sendHistoryBuff)
            # print("print_window send:", data)
            self.ConnectApi.write(data)
            self.senddataVar.set("")
            #self.receiveUpdateSignal.emit("")
        else:
            messagebox.showerror(title='警告！', message='未连接')
    def senddatakeyup(self,ev = None):
        tplen = len(self.sendHistoryBuff)
        print(tplen,self.sendHistoryBuffCnt)
        if (tplen > 0):
            if (self.sendHistoryBuffCnt < tplen):
                currentcmd = self.sendHistoryBuff[tplen - self.sendHistoryBuffCnt - 1]
            else:
                currentcmd = ""
            if self.sendHistoryBuffCnt < (tplen - 1):
                self.sendHistoryBuffCnt = self.sendHistoryBuffCnt + 1
            self.senddataVar.set(currentcmd)
    def senddatakeydown(self,ev = None):
        tplen = len(self.sendHistoryBuff)
        print(tplen,self.sendHistoryBuffCnt)
        if(tplen > 0):
            if(self.sendHistoryBuffCnt > 0):
                currentcmd = self.sendHistoryBuff[tplen - self.sendHistoryBuffCnt]
                self.sendHistoryBuffCnt = self.sendHistoryBuffCnt - 1
            else:
                currentcmd = ""


            self.senddataVar.set(currentcmd)


def main():
    ui = tk.Tk()
    app = Application(ui)
    ui.mainloop()

if __name__ == '__main__':
    main()