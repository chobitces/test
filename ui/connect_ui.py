import tkinter as tk
from  tkinter  import ttk


class Ui_ConnectSetWindows():
    def __init__(self,ui):
        self.typevalue = tk.StringVar()
        self.root = ui
        self.setupUi()
    def setupUi(self):
        self.ConnectUi = tk.Toplevel(self.root)
        self.ConnectUi.title("连接设置") # 修改框体的名字,也可在创建时使用className参数来命名；
        width = 350
        height = 50
        screenwidth = self.ConnectUi.winfo_screenwidth()
        screenheight = self.ConnectUi.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.ConnectUi.geometry(alignstr)
        # 设置窗口是否可变长、宽，True：可变，False：不可变

        tk.Label(self.ConnectUi, text="连接方式").grid(row=0,ipadx = 20,ipady = 20)


        self.ConnectUi.resizable(width=True, height=True)
        self.combox_connecttype = ttk.Combobox(self.ConnectUi, textvariable=self.typevalue)
        self.combox_connecttype["values"]=("serial","SSH","telnet")
        self.combox_connecttype.current(0)
        self.combox_connecttype.grid(row=0, column=1)
class Ui_SerialSetWindows():
    def __init__(self,ui,portlist):
        self.portvalue = tk.StringVar()
        self.baudratevalue = tk.StringVar()
        self.databitvalue = tk.StringVar()
        self.parityvalue = tk.StringVar()
        self.stopbitsvalue = tk.StringVar()
        self.root = ui
        self.portlist = portlist
        self.setupUi()
    def setupUi(self):
        self.ConnectUi = tk.Toplevel(self.root)
        self.ConnectUi.title("连接设置") # 修改框体的名字,也可在创建时使用className参数来命名；
        width = 350
        height = 400
        screenwidth = self.ConnectUi.winfo_screenwidth()
        screenheight = self.ConnectUi.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.ConnectUi.geometry(alignstr)
        # 设置窗口是否可变长、宽，True：可变，False：不可变
        self.ConnectUi.resizable(width=True, height=True)

        tk.Label(self.ConnectUi, text="端口").grid(row=0,ipadx = 20,ipady = 20)
        self.combox_port = ttk.Combobox(self.ConnectUi, textvariable=self.portvalue)
        self.combox_port["values"]=self.portlist
        self.combox_port.current(0)
        self.combox_port.grid(row=0, column=1)

        tk.Label(self.ConnectUi, text="波特率").grid(row=1,ipadx = 20,ipady = 20)
        self.combox_baudrate = ttk.Combobox(self.ConnectUi, textvariable=self.baudratevalue)
        self.combox_baudrate["values"]= ("9600", "19200", "115200")
        self.combox_baudrate.current(2)
        self.combox_baudrate.grid(row=1, column=1)

        tk.Label(self.ConnectUi, text="数据位").grid(row=2,ipadx = 20,ipady = 20)
        self.combox_databit = ttk.Combobox(self.ConnectUi, textvariable=self.databitvalue)
        self.combox_databit["values"]= ("5", "6", "7", "8")
        self.combox_databit.current(3)
        self.combox_databit.grid(row=2, column=1)

        tk.Label(self.ConnectUi, text="奇偶校验").grid(row=3,ipadx = 20,ipady = 20)
        self.combox_parity = ttk.Combobox(self.ConnectUi, textvariable=self.parityvalue)
        self.combox_parity["values"]= ("None", "Odd", "Even", "Mark", "Space")
        self.combox_parity.current(0)
        self.combox_parity.grid(row=3, column=1)

        tk.Label(self.ConnectUi, text="停止位").grid(row=4,ipadx = 20,ipady = 20)
        self.ConnectUi.resizable(width=True, height=True)
        self.combox_stopbits = ttk.Combobox(self.ConnectUi, textvariable=self.stopbitsvalue)
        self.combox_stopbits["values"]= ("1", "1.5", "2")
        self.combox_stopbits.current(0)
        self.combox_stopbits.grid(row=4, column=1)
class Ui_SshSetWindows():
    def __init__(self,ui):
        self.typevalue = tk.StringVar()
        self.root = ui
        self.hostipvalue = tk.StringVar()
        self.portvalue = tk.StringVar()
        self.usernamevalue = tk.StringVar()
        self.passwordvalue = tk.StringVar()
        self.namevalue = tk.StringVar()
        self.setupUi()
    def setupUi(self):
        self.ConnectUi = tk.Toplevel(self.root)
        self.ConnectUi.title("连接设置") # 修改框体的名字,也可在创建时使用className参数来命名；
        width = 350
        height = 400
        screenwidth = self.ConnectUi.winfo_screenwidth()
        screenheight = self.ConnectUi.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.ConnectUi.geometry(alignstr)
        # 设置窗口是否可变长、宽，True：可变，False：不可变
        self.ConnectUi.resizable(width=True, height=True)

        tk.Label(self.ConnectUi, text="主机地址").grid(row=0, ipadx=20, ipady=20)
        self.Entry_hostip = tk.Entry(self.ConnectUi, textvariable=self.hostipvalue)
        self.Entry_hostip.grid(row=0, column=1)
        self.hostipvalue.set("10.26.0.250")

        tk.Label(self.ConnectUi, text="端口").grid(row=1, ipadx=20, ipady=20)
        self.Entry_port = tk.Entry(self.ConnectUi, textvariable=self.portvalue)
        self.Entry_port.grid(row=1, column=1)
        self.portvalue.set("22")

        tk.Label(self.ConnectUi, text="用户名").grid(row=2, ipadx=20, ipady=20)
        self.Entry_username = tk.Entry(self.ConnectUi, textvariable=self.usernamevalue)
        self.Entry_username.grid(row=2, column=1)
        self.usernamevalue.set("root")

        tk.Label(self.ConnectUi, text="密码").grid(row=3, ipadx=20, ipady=20)
        self.Entry_password = tk.Entry(self.ConnectUi, textvariable=self.passwordvalue)
        self.Entry_password.grid(row=3, column=1)
        self.passwordvalue.set("root")

        tk.Label(self.ConnectUi, text="会话名称").grid(row=4, ipadx=20, ipady=20)
        self.Entry_name = tk.Entry(self.ConnectUi, textvariable=self.namevalue)
        self.Entry_name.grid(row=4, column=1)
